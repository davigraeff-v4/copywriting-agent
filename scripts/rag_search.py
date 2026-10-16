"""BM25 + local cosine + document-level RRF; scope filters precede ranking."""
from __future__ import annotations
import bisect,json,math,re
from collections import Counter
from pathlib import Path
from rag_config import MODEL,FASTEMBED_VERSION,DIMENSION,SCHEMA_VERSION,INDEX_REL,SEMANTIC_FLOOR,RRF_K,LEXICAL_WEIGHT,SEMANTIC_WEIGHT,MAX_TOKENS
from rag_corpus import ROOT,public_entries,public_path,source_fingerprint,make_chunks,digest_bytes,prefix,tokens,document_data
from rag_model import load_model,model_signature
from build_rag_index import pipeline_hash
from rag_ranking import rank_tokens,metadata_penalty,relevance_prior,section_key,META_WEIGHT,SEMANTIC_DOCUMENT_FLOOR,SEMANTIC_CANDIDATE_FLOOR,BODY_BLEND_CURATED,BODY_BLEND_ORIGINAL,RRF_DOCUMENT_K,RRF_PASSAGE_K,SEMANTIC_WEIGHT_CURATED,SEMANTIC_WEIGHT_ORIGINAL,RANKING_VERSION

class BM25:
    def __init__(self,texts,tokenize=tokens,minimum_overlap=2):
        self.tokenize=tokenize
        self.minimum_overlap=minimum_overlap
        self.counts=[Counter(tokenize(t)) for t in texts];self.lengths=[sum(c.values()) for c in self.counts]
        self.average=sum(self.lengths)/max(1,len(texts));self.df=Counter()
        for count in self.counts:self.df.update(count.keys())
        self.scope_statistics={}
    def scores(self,query,allowed):
        query=set(self.tokenize(query));result={};key=tuple(allowed)
        # Ineligible books must not change the frequency statistics of a query
        # restricted to curated examples, a route, or a particular source.
        if key not in self.scope_statistics:
            if len(self.scope_statistics)>=32:self.scope_statistics.clear()
            df=Counter()
            for i in allowed:df.update(self.counts[i].keys())
            self.scope_statistics[key]=(len(allowed),sum(self.lengths[i] for i in allowed)/max(1,len(allowed)),df)
        n,average,df=self.scope_statistics[key]
        for i in allowed:
            count=self.counts[i];score=0.0
            # Long questions with a single coincidental term should abstain.
            if len(query)>=4 and len(query & count.keys())<self.minimum_overlap:continue
            for term in query:
                frequency=count.get(term,0)
                if not frequency:continue
                idf=math.log(1+(n-df[term]+.5)/(df[term]+.5))
                denominator=frequency+1.2*(.25+.75*self.lengths[i]/max(1,average))
                score+=idf*frequency*2.2/denominator
            if score>0:result[i]=score
        return result

class Retriever:
    def __init__(self,root=ROOT,index_dir=None,cache_dir=None):
        self.root=Path(root).resolve();self.index_dir=Path(index_dir) if index_dir else self.root/INDEX_REL
        self.cache_dir=cache_dir;self.vectors=None;self.generation=None;self.fingerprint=None;self.query_vectors={};self._refresh(force=True)
    def _artifact_stamp(self,pointer):
        try:
            data=json.loads(pointer.read_text())
            if not isinstance(data,dict) or not re.fullmatch(r'[0-9a-f]{16}-[0-9a-f]{8}',data.get('generation','')):return None
            folder=(self.index_dir/data['generation']).resolve()
            if not folder.is_relative_to(self.index_dir.resolve()):return None
            return tuple((name,(folder/name).stat().st_mtime_ns,(folder/name).stat().st_size) for name in ['manifest.json','chunks.json','vectors.npz'])
        except (OSError,ValueError,TypeError):return None
    def _refresh(self,force=False):
        entries=public_entries(self.root);fingerprint=source_fingerprint(entries,self.root)
        pointer=self.index_dir/'current.json';pointer_hash=digest_bytes(pointer.read_bytes()) if pointer.is_file() else None
        artifact_stamp=self._artifact_stamp(pointer)
        if not force and (fingerprint,pointer_hash,artifact_stamp)==(self.fingerprint,self.pointer_hash,self.artifact_stamp):return
        self.entries=entries;self.docs={e['id']:e for e in entries};self.fingerprint=fingerprint;self.pointer_hash=pointer_hash
        self.artifact_stamp=artifact_stamp
        self.vectors=None;self.generation=None;self.manifest=None;self.index_error=None;self.query_vectors={};self.document_data={};parent_maps={};line_maps={}
        try:
            if not pointer.is_file():raise ValueError('index_missing')
            pointer_data=json.loads(pointer.read_text())
            if not isinstance(pointer_data,dict):raise ValueError('invalid_index_pointer')
            generation=pointer_data.get('generation','')
            if not re.fullmatch(r'[0-9a-f]{16}-[0-9a-f]{8}',generation):raise ValueError('invalid_index_pointer')
            folder=(self.index_dir/generation).resolve()
            if not folder.is_relative_to(self.index_dir.resolve()):raise ValueError('index_path_escape')
            manifest=json.loads((folder/'manifest.json').read_text())
            if not isinstance(manifest,dict):raise ValueError('invalid_index_manifest')
            if manifest.get('source_fingerprint')!=fingerprint or manifest.get('pipeline_hash')!=pipeline_hash(self.root):raise ValueError('index_stale')
            if manifest.get('schema_version')!=SCHEMA_VERSION or manifest.get('model')!=MODEL or manifest.get('fastembed_version')!=FASTEMBED_VERSION or manifest.get('embedding_dim')!=DIMENSION or manifest.get('token_limit')!=MAX_TOKENS or manifest.get('public_only') is not True or manifest.get('private_documents')!=0:
                raise ValueError('index_configuration_mismatch')
            for name in ['chunks.json','vectors.npz']:
                p=folder/name
                if not p.resolve().is_relative_to(folder) or digest_bytes(p.read_bytes())!=manifest.get('files',{}).get(name):raise ValueError('index_artifact_corrupt')
            payload=json.loads((folder/'chunks.json').read_text())
            if not isinstance(payload,dict) or not isinstance(payload.get('chunks'),list):raise ValueError('invalid_chunk_payload')
            chunks=payload['chunks']
            if payload['documents']!=entries or len(chunks)!=manifest['chunk_count'] or len(entries)!=manifest['document_count']:raise ValueError('index_alignment_mismatch')
            ids=set()
            for chunk in chunks:
                if not isinstance(chunk,dict):raise ValueError('invalid_chunk_record')
                doc=self.docs.get(chunk.get('document_id'))
                if not doc or chunk.get('path')!=doc['path'] or chunk.get('id') in ids:raise ValueError('index_scope_mismatch')
                ids.add(chunk['id'])
                if doc['id'] not in self.document_data:
                    self.document_data[doc['id']]=document_data(doc,self.root)
                    parent_maps[doc['id']]={s['id']:s for s in self.document_data[doc['id']]['segments']}
                    line_maps[doc['id']]=[m.start() for m in re.finditer('\n',self.document_data[doc['id']]['text'])]
                raw=self.document_data[doc['id']]['text'];a=chunk['start_char'];b=chunk['end_char']
                if not isinstance(a,int) or not isinstance(b,int) or not 0<=a<b<=len(raw) or raw[a:b]!=chunk['body'] or prefix(doc,chunk['section'])+chunk['body']!=chunk['text'] or not 0<chunk.get('token_count',0)<=MAX_TOKENS:
                    raise ValueError('index_chunk_locator_mismatch')
                parent=parent_maps[doc['id']].get(chunk.get('parent_id'))
                if not parent or not parent['start_char']<=a<b<=parent['end_char'] or chunk.get('page')!=parent.get('page') or chunk.get('chapter_number')!=parent.get('chapter_number') or chunk['section']!=parent['section'] or chunk['line_start']!=bisect.bisect_left(line_maps[doc['id']],a)+1 or chunk['line_end']!=bisect.bisect_left(line_maps[doc['id']],b)+1:
                    raise ValueError('index_chunk_parent_mismatch')
            self.chunks=chunks;self.generation=folder;self.manifest=manifest
        except (OSError,ValueError,KeyError,TypeError) as exc:
            self.index_error=str(exc);self.chunks=make_chunks(entries,self.root)
        # Metadata is useful for terms; never supplies facts or factual confidence.
        self.bm25=BM25([c['body'] for c in self.chunks],rank_tokens,1)
        self.bm25_meta=BM25([self.docs[c['document_id']]['title']+' '+c['section']+' '+' '.join(self.docs[c['document_id']].get('tags',[])) for c in self.chunks],rank_tokens,1)
        self.section_groups={}
        for i,c in enumerate(self.chunks):self.section_groups.setdefault((c['document_id'],section_key(c)),[]).append(i)
        self.section_keys=list(self.section_groups);section_texts=[]
        for did,key in self.section_keys:
            if did not in self.document_data:self.document_data[did]=document_data(self.docs[did],self.root)
            segments=self.document_data[did]['segments']
            section_texts.append('\n\n'.join(s['text'] for s in segments if (s.get('chapter_number')==key[1] if key[0]=='chapter' else s['id']==key[1])))
        self.section_bm25=BM25(section_texts,rank_tokens)
        self.body_vectors=None;self.body_channel_stamp=None;self.body_channel_error=None
    def _semantic(self,query,allowed):
        import fastembed,numpy as np
        if fastembed.__version__!=self.manifest['fastembed_version']:raise ValueError('embedding_engine_version_mismatch')
        if self.vectors is None:
            with np.load(self.generation/'vectors.npz',allow_pickle=False) as raw:vectors=raw['vectors'].copy()
            if vectors.shape!=(len(self.chunks),DIMENSION) or vectors.dtype!=np.float32 or not np.isfinite(vectors).all():raise ValueError('invalid_vector_shape_or_values')
            norms=np.linalg.norm(vectors,axis=1,keepdims=True)
            if (norms<=0).any():raise ValueError('zero_vector')
            self.vectors=vectors/norms
        if query not in self.query_vectors:
            model=load_model(self.cache_dir)
            if model_signature(model)!=self.manifest.get('model_files_sha256'):raise ValueError('embedding_model_files_mismatch')
            if len(query.split())>180:raise ValueError('query_too_long')
            # Query truncation is refused, not hidden.
            from rag_model import counting_tokenizer
            if len(counting_tokenizer(model).encode(query).ids)>MAX_TOKENS:raise ValueError('query_token_limit_exceeded')
            vector=np.asarray(next(iter(model.embed([query]))),dtype=np.float32)
            if vector.shape!=(DIMENSION,) or not np.isfinite(vector).all() or np.linalg.norm(vector)<=0:raise ValueError('invalid_query_vector')
            self.query_vectors[query]=vector/np.linalg.norm(vector)
        # Cosine is computed only over rows of route/use-eligible public documents.
        similarities=self.vectors[allowed]@self.query_vectors[query]
        from rag_semantic_channel import load_channel,channel_stamp
        stamp=channel_stamp(self.root)
        if stamp!=self.body_channel_stamp or (self.body_vectors is None and self.body_channel_error is None):
            self.body_channel_stamp=stamp;self.body_vectors=None;self.body_channel_error=None
            try:self.body_vectors,_=load_channel(self.root,self.fingerprint,self.chunks,self.manifest['model_files_sha256'],self.manifest['files']['chunks.json'])
            except (OSError,ValueError,KeyError,TypeError) as exc:self.body_channel_error=type(exc).__name__+': '+str(exc)
        if self.body_vectors is not None:
            content=self.body_vectors[allowed]@self.query_vectors[query]
            mix=np.asarray([BODY_BLEND_ORIGINAL if self.docs[self.chunks[i]['document_id']]['use']=='original' else BODY_BLEND_CURATED for i in allowed],dtype=np.float32)
            similarities=mix*content+(1-mix)*similarities
        return {i:float(s)-metadata_penalty(self.docs[self.chunks[i]['document_id']],self.chunks[i],query) for i,s in zip(allowed,similarities) if float(s)>=SEMANTIC_CANDIDATE_FLOOR}
    def search(self,query,route,client,use=None,limit=4,engine='auto',source_ids=None,page=None,section=None):
        if route not in {'ads','lp','social','direct'} or use not in {None,'guidance','positive','negative','structure','original'}:raise ValueError('invalid retrieval filters')
        if not isinstance(client,str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',client):raise ValueError('invalid client slug')
        if engine not in {'auto','lexical','semantic','hybrid'}:raise ValueError('invalid retrieval engine')
        if not 1<=limit<=20:raise ValueError('limit must be 1..20')
        if page is not None and (type(page) is not int or page<1):raise ValueError('invalid page filter')
        if section is not None and (not isinstance(section,str) or not section.strip()):raise ValueError('invalid section filter')
        self._refresh()
        if source_ids and not set(source_ids)<=set(self.docs):raise ValueError('unknown source filter')
        eligible={d['id'] for d in self.entries if d['status']=='active' and d['client']=='*' and route in d['routes'] and (use is None or d['use']==use) and (not source_ids or d['id'] in source_ids)}
        allowed=[i for i,c in enumerate(self.chunks) if c['document_id'] in eligible and (page is None or c.get('page')==page) and (section is None or section.casefold() in c['section'].casefold())]
        lexical=self.bm25.scores(query,allowed)
        for i,score in self.bm25_meta.scores(query,allowed).items():lexical[i]=lexical.get(i,0)+META_WEIGHT*score
        query_terms=set(rank_tokens(query))
        if len(query_terms)>=4:lexical={i:s for i,s in lexical.items() if len(query_terms&(self.bm25.counts[i].keys()|self.bm25_meta.counts[i].keys()))>=2}
        lexical={i:s*(.4 if metadata_penalty(self.docs[self.chunks[i]['document_id']],self.chunks[i],query) else 1) for i,s in lexical.items() if s>0}
        semantic={};fallback=None
        mode='hybrid' if engine=='auto' else engine
        if mode in {'semantic','hybrid'} and allowed and tokens(query):
            if not self.generation:fallback=self.index_error or 'index_unavailable'
            else:
                try:semantic=self._semantic(query,allowed)
                except Exception as exc:fallback=type(exc).__name__+': '+str(exc)
        if fallback:mode='lexical'
        def documents(scores,dense=False):
            result={}
            for i,score in scores.items():
                did=self.chunks[i]['document_id']
                if did not in result or score>result[did][1]:result[did]=(i,score)
            if dense:
                parents={}
                for i,score in scores.items():
                    c=self.chunks[i];values=parents.setdefault(c['document_id'],{});values[c['parent_id']]=max(values.get(c['parent_id'],0),score)
                for did in list(result):
                    values=sorted(parents[did].values(),reverse=True)[:3]
                    support=.5*values[0]+.5*sum(values)/len(values)
                    if support<SEMANTIC_DOCUMENT_FLOOR:del result[did]
                    else:result[did]=(result[did][0],support)
            return sorted(((d,(i,s*relevance_prior(self.docs[d],route))) for d,(i,s) in result.items()),key=lambda x:(-x[1][1],x[0]))
        lex=documents(lexical);sem=documents(semantic,True);rank={};best={}
        if mode in {'lexical','semantic'}:
            chosen=lex if mode=='lexical' else sem
            for did,(i,score) in chosen:rank[did]=score;best[did]=i
        else:
            dense_weight=SEMANTIC_WEIGHT_ORIGINAL if use=='original' else SEMANTIC_WEIGHT_CURATED
            for ranking,weight in [(lex,1.0),(sem,dense_weight)]:
                for position,(did,(i,score)) in enumerate(ranking,1):
                    rank[did]=rank.get(did,0)+weight/(RRF_DOCUMENT_K+position)
                    if did not in best:best[did]=i
        # Document fusion prevents a long book from occupying every result.
        # Passage fusion is separate: choosing the lexical peak unconditionally
        # could point to a different chapter from the semantically relevant one.
        passage_scores={}
        if mode=='hybrid':
            for scores,weight in [(lexical,1.0),(semantic,1.0)]:
                by_document={}
                for i,score in scores.items():by_document.setdefault(self.chunks[i]['document_id'],[]).append((i,score))
                for items in by_document.values():
                    for position,(i,_) in enumerate(sorted(items,key=lambda x:(-x[1],x[0])),1):
                        passage_scores[i]=passage_scores.get(i,0)+weight/(RRF_PASSAGE_K+position)
        else:passage_scores=lexical if mode=='lexical' else semantic
        passages={}
        for i,score in sorted(passage_scores.items(),key=lambda x:(-x[1],x[0])):
            did=self.chunks[i]['document_id'];parent=self.chunks[i]['parent_id']
            group=passages.setdefault(did,[])
            if len(group)<3 and all(self.chunks[j]['parent_id']!=parent for j in group):group.append(i)
        for did,items in passages.items():best[did]=items[0]
        # Locate the section/chapter before choosing its best page. A phrase can
        # span multiple short chunks; a chapter can span multiple PDF pages.
        allowed_set=set(allowed)
        permitted_sections=[j for j,key in enumerate(self.section_keys) if any(i in allowed_set for i in self.section_groups[key])]
        section_lex=self.section_bm25.scores(query,permitted_sections)
        for did in rank:
            lex_groups={};sem_groups={}
            for j,(document,key) in enumerate(self.section_keys):
                if document!=did:continue
                indices=[i for i in self.section_groups[(did,key)] if i in allowed_set]
                if section_lex.get(j,0)>0:lex_groups[key]=section_lex[j]
                values=sorted((semantic[i] for i in indices if i in semantic),reverse=True)[:3]
                if values:sem_groups[key]=.7*values[0]+.3*sum(values)/len(values)
            fused={}
            channels=[(lex_groups,1.0)] if mode=='lexical' else [(sem_groups,1.0)] if mode=='semantic' else [(lex_groups,1.0),(sem_groups,1.0)]
            for scores,weight in channels:
                for position,(key,_) in enumerate(sorted(scores.items(),key=lambda x:(-x[1],str(x[0]))),1):fused[key]=fused.get(key,0)+weight/(RRF_PASSAGE_K+position)
            chosen=[]
            for key in sorted(fused,key=lambda key:(-fused[key],-lex_groups.get(key,0),str(key))):
                indices=self.section_groups[(did,key)];candidates=[i for i in indices if i in passage_scores and i in allowed_set]
                if candidates:chosen.append(max(candidates,key=lambda i:(passage_scores[i],lexical.get(i,0),-i)))
                if len(chosen)==3:break
            for i in passages.get(did,[]):
                if len(chosen)<3 and all(self.chunks[j]['parent_id']!=self.chunks[i]['parent_id'] for j in chosen):chosen.append(i)
            if chosen:passages[did]=chosen;best[did]=chosen[0]
        lex_by=dict(lex);sem_by=dict(sem);results=[]
        groups=set()
        for did in sorted(rank,key=lambda d:(-rank[d],-dict(lex).get(d,(0,0))[1],d)):
            group=self.docs[did].get('ranking_group',did)
            if group in groups:continue
            groups.add(group)
            if len(results)>=limit:break
            d=self.docs[did];c=self.chunks[best[did]]
            if did not in self.document_data:self.document_data[did]=document_data(d,self.root)
            data=self.document_data[did]
            parent=next(s for s in data['segments'] if s['id']==c['parent_id'])
            context_start=max(parent['start_char'],c['start_char']-1200)
            context_end=min(parent['end_char'],max(c['end_char'],context_start+3500))
            context=data['text'][context_start:context_end]
            ocr_rows=[row for row in parent.get('ocr_rows',[]) if row.get('start_char',0)<c['end_char'] and row.get('end_char',0)>c['start_char']]
            image_boxes=[row['box'] for row in ocr_rows]
            guard=dict(authority=d.get('authority'),evidence_kind=d.get('evidence_kind'),synthetic=d.get('synthetic',False),human_approved=d.get('human_approved',False),performance_verified=d.get('performance_verified',False),client_evidence=False,external_content_is_data=True,requires_full_read=True)
            results.append(dict(id=did,path=d['path'],use=d['use'],score=round(rank[did],6),summary=d['summary'],matched=sorted(set(tokens(query))&set(tokens(c['text']+' '+' '.join(d.get('tags',[]))))),excerpt=c['body'],chunk_id=c['id'],section=c['section'],locator=dict(start_char=c['start_char'],end_char=c['end_char'],line_start=c['line_start'],line_end=c['line_end'],page=c.get('page'),chapter_number=c.get('chapter_number'),parent_id=c['parent_id'],image_boxes=image_boxes,ocr_min_confidence=min((row['confidence'] for row in ocr_rows),default=None)),source_sha256=d['sha256'],source_urls=d.get('source_urls',[]),guards=guard,original_format=Path(d['path']).suffix.lower(),reference_format=d.get('format'),extraction_path=d.get('extraction_path'),parent_context=dict(text=context,start_char=context_start,end_char=context_end,page=parent.get('page'),section=parent['section'],truncated=context_start!=parent['start_char'] or context_end!=parent['end_char']),lexical_score=round(lex_by.get(did,(0,0))[1],4),semantic_similarity=round(sem_by.get(did,(0,0))[1],4)))
            results[-1]['matched_passages']=[dict(chunk_id=self.chunks[i]['id'],section=self.chunks[i]['section'],page=self.chunks[i].get('page'),chapter_number=self.chunks[i].get('chapter_number'),parent_id=self.chunks[i]['parent_id'],start_char=self.chunks[i]['start_char'],end_char=self.chunks[i]['end_char'],line_start=self.chunks[i]['line_start'],line_end=self.chunks[i]['line_end'],excerpt=self.chunks[i]['body'],lexical_score=round(lexical.get(i,0),4),semantic_similarity=round(semantic.get(i,0),4)) for i in passages.get(did,[best[did]])]
        return dict(results=results,engine_requested=engine,engine_used=mode,semantic_used=bool(sem) and mode in {'hybrid','semantic'},semantic_channel=('body_and_context' if self.body_vectors is not None else 'context_only') if mode in {'semantic','hybrid'} else 'not_used',semantic_channel_warning=self.body_channel_error,ranking_version=RANKING_VERSION,fallback_reason=fallback,public_documents=len(self.entries),eligible_documents=len(eligible),eligible_chunks=len(allowed),note='Similarity is not factual validation. Read the full source and its limits. No client files in this index.')
