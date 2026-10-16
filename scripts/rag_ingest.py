#!/usr/bin/env python3
"""Local original adapters and immutable extraction registry. Never execute source content."""
from __future__ import annotations
import csv,hashlib,html,json,re,subprocess,uuid,zipfile
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
INGESTION='.local/rag/ingestion'
ALLOWED_SUFFIXES={'.pdf','.txt','.md','.json','.csv','.html','.htm','.docx','.pptx','.xlsx','.epub','.png','.jpg','.jpeg','.webp','.gif','.tiff','.tif'}
INJECTION=re.compile(r'ignore (?:all |any )?(?:previous|prior) instructions|reveal (?:your |the )?system prompt|<\|(?:system|im_start)\|>|execute this command',re.I)

def sha(raw):return hashlib.sha256(raw).hexdigest()
def normalized(raw):return raw.decode('utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def safe_original(root,relative):
    root=Path(root).resolve();rel=Path(relative)
    if rel.is_absolute() or '..' in rel.parts:raise ValueError('original path escape')
    allowed=(rel.parts[:1]==('BASE DE CONHECIMENTO',) or rel.parts[:3]==('.local','repertorio','originais') or rel.parts[:1]==('knowledge',))
    if not allowed or rel.suffix.lower() not in ALLOWED_SUFFIXES:raise ValueError('original outside approved collections')
    p=(root/rel).resolve()
    permitted=[root/'BASE DE CONHECIMENTO',root/'.local/repertorio/originais',root/'knowledge']
    if not any(p.is_relative_to(b) for b in permitted) or not p.is_file():raise ValueError('original symlink/outside collection')
    return p

def blocks(text,headings=None):
    text=text.replace('\r\n','\n').replace('\r','\n')
    headings=list(re.finditer(headings or r'(?m)^CHAPTER\s+[IVXLCDM]+\.?\s*$',text))
    starts=[0]+[m.start() for m in headings if m.start()>0]
    labels=['Preâmbulo']+[m.group().strip() for m in headings if m.start()>0]
    return [dict(text=text[a:b],section=labels[i],page=None) for i,(a,b) in enumerate(zip(starts,starts[1:]+[len(text)])) if text[a:b]]

def html_text(text):
    class Reader(HTMLParser):
        def __init__(self):super().__init__(convert_charrefs=True);self.skip=0;self.parts=[]
        def handle_starttag(self,tag,attrs):
            if tag in {'script','style','noscript'}:self.skip+=1
            if tag in {'p','div','h1','h2','h3','li','tr','br'}:self.parts.append('\n')
        def handle_endtag(self,tag):
            if tag in {'script','style','noscript'}:self.skip=max(0,self.skip-1)
        def handle_data(self,data):
            if not self.skip:self.parts.append(data)
    p=Reader();p.feed(text);return ''.join(p.parts)

def pdf_security(reader):
    from pypdf.generic import IndirectObject
    flags=set();visited=set()
    def walk(obj,depth=0):
        if depth>50:flags.add('object_graph_depth_limit');return
        if isinstance(obj,IndirectObject):
            key=(obj.idnum,obj.generation)
            if key in visited:return
            visited.add(key);obj=obj.get_object()
        if isinstance(obj,dict):
            for key,value in obj.items():
                if str(key) in {'/JS','/JavaScript','/Launch','/EmbeddedFiles','/RichMedia','/AA'}:flags.add(str(key))
                walk(value,depth+1)
        elif isinstance(obj,list):
            for v in obj:walk(v,depth+1)
        elif str(obj) in {'/JavaScript','/Launch','/RichMedia'}:flags.add(str(obj))
    walk(reader.trailer)
    return sorted(flags)

def extract_pdf(path):
    from pypdf import PdfReader
    reader=PdfReader(path);flags=pdf_security(reader)
    if flags:raise ValueError('active/embedded PDF feature quarantined: '+','.join(flags))
    pages=[];chapter='Capa e apresentação';chapter_number=None
    for number,page in enumerate(reader.pages,1):
        stream=page.get_contents()
        if stream and len(stream.get_data())>20_000_000:raise ValueError('PDF stream too large')
        text=(page.extract_text() or '').replace('\r\n','\n').replace('\r','\n')
        match=re.search(r'Chapter\s+(\d+)\s*\n([^\n]+)(?:\n([^\n]+))?',text)
        if match:
            chapter_number=int(match[1]);title=match[2].strip()
            if match[3] and (title.endswith(('Are','–','-'))):title+=' '+match[3].strip()
            chapter='Chapter '+match[1]+': '+title
            # Wrapped titles are retained in source text regardless of this label.
        if 'Products Currently Available' in text or (pages and pages[-1]['section']=='Apêndice da edição digital'):
            chapter='Apêndice da edição digital';chapter_number=None
        pages.append(dict(text=text,section=chapter,page=number,chapter_number=chapter_number,dimensions=[float(page.mediabox.width),float(page.mediabox.height)],visual_objects=bool(page.get('/Resources',{}).get('/XObject')),extraction_method='pypdf_text'))
    return pages,dict(page_count=len(reader.pages),pages_with_text=sum(bool(x['text'].strip()) for x in pages),empty_pages=[x['page'] for x in pages if not x['text'].strip()],security_flags=flags)

def extract_zip(path):
    suffix=path.suffix.lower();parts=[]
    with zipfile.ZipFile(path) as z:
        infos=z.infolist()
        if sum(x.file_size for x in infos)>100_000_000 or any(x.file_size/max(x.compress_size,1)>1000 for x in infos):raise ValueError('archive expansion limit')
        if any('vbaproject' in x.filename.lower() or x.filename.lower().endswith(('.exe','.dll','.js','.vbs')) for x in infos):raise ValueError('macro/executable in archive')
        if suffix=='.docx':names=['word/document.xml']+[x.filename for x in infos if re.fullmatch(r'word/(?:header|footer)\d+\.xml',x.filename)]
        elif suffix=='.pptx':names=sorted([x.filename for x in infos if re.fullmatch(r'ppt/slides/slide\d+\.xml',x.filename)],key=lambda s:int(re.search(r'(\d+)\.xml',s)[1]))
        elif suffix=='.xlsx':names=[x.filename for x in infos if x.filename=='xl/sharedStrings.xml' or re.fullmatch(r'xl/worksheets/sheet\d+\.xml',x.filename)]
        else:
            names=[x.filename for x in infos if x.filename.lower().endswith(('.xhtml','.html','.htm'))]
        for i,name in enumerate(names,1):
            raw=z.read(name)
            if len(raw)>10_000_000 or b'<!DOCTYPE' in raw or b'<!ENTITY' in raw:raise ValueError('unsafe/oversized XML')
            if suffix=='.epub':text=html_text(raw.decode('utf-8'))
            else:
                tree=ET.fromstring(raw)
                text='\n'.join(''.join(node.itertext()) for node in tree.iter() if node.tag.rsplit('}',1)[-1] in ({'p'} if suffix=='.docx' else {'t','v'}))
            parts.append(dict(text=text,section=name,page=i if suffix=='.pptx' else None,container_part=name))
    return parts,dict(parts=len(parts),page_count=len(parts) if suffix=='.pptx' else None,security_flags=[])

def assemble(segments):
    text='';result=[]
    for i,segment in enumerate(segments):
        if text:text+='\n\n'
        start=len(text);text+=segment['text']
        if segment.get('ocr_rows'):
            cursor=start
            for row in segment['ocr_rows']:
                row['start_char']=cursor;row['end_char']=cursor+len(row['text']);cursor=row['end_char']+1
        result.append({**segment,'id':f's{i:05d}','start_char':start,'end_char':len(text)})
    return text,result

def load_registry(root=ROOT):
    root=Path(root).resolve();pointer=root/INGESTION/'current.json'
    if not pointer.is_file():return [],None
    key=json.loads(pointer.read_text()).get('generation','')
    if not re.fullmatch(r'[0-9a-f]{16}',key):raise ValueError('invalid ingestion generation')
    folder=(root/INGESTION/key).resolve()
    if not folder.is_relative_to(root/INGESTION):raise ValueError('ingestion generation escape')
    manifest=json.loads((folder/'manifest.json').read_text());p=folder/'sources.json'
    if sha(p.read_bytes())!=manifest['files']['sources.json']:raise ValueError('ingestion registry corrupted')
    entries=json.loads(p.read_text())
    for d in entries:
        original=safe_original(root,d['path'])
        if sha(original.read_bytes())!=d['sha256']:raise ValueError('original changed since extraction')
        ep=(root/d['extraction_path']).resolve()
        if not ep.is_relative_to(folder) or sha(ep.read_bytes())!=d['extraction_sha256']:raise ValueError('extraction corrupted/escape')
        if d.get('client')!='*' or d.get('status')!='active' or d.get('use')!='original':raise ValueError('invalid original scope')
        for alias in d.get('aliases',[]):
            ap=safe_original(root,alias['path'])
            if sha(ap.read_bytes())!=alias['sha256']:raise ValueError('original alias changed')
    return entries,manifest

def extraction(entry,root=ROOT):
    root=Path(root).resolve();p=(root/entry['extraction_path']).resolve()
    if not p.is_relative_to(root/INGESTION) or sha(p.read_bytes())!=entry['extraction_sha256']:raise ValueError('invalid extracted document')
    data=json.loads(p.read_text());text=data['text']
    if data['source_sha256']!=entry['sha256']:raise ValueError('original/extraction identity mismatch')
    for s in data['segments']:
        if text[s['start_char']:s['end_char']]!=s['text']:raise ValueError('extraction segment mismatch')
    return data

def ingest(root=ROOT,work=None):
    root=Path(root).resolve();work=Path(work) if work else root/'.local/rag/full-ingestion'
    input_hashes=json.loads((work/'source-inputs.json').read_text())
    for relative,expected in input_hashes.items():
        if sha(safe_original(root,relative).read_bytes())!=expected:raise ValueError('OCR/extraction input changed; regenerate its extraction: '+relative)
    ocr={Path(x['path']).resolve():x for x in [json.loads(l) for l in (work/'ocr.jsonl').read_text().splitlines()]}
    tiled=work/'ocr-tiled.jsonl'
    if tiled.is_file():
        for x in [json.loads(l) for l in tiled.read_text().splitlines()]:
            original=ocr[Path(x['path']).resolve()]
            if len(x['rows'])>=len(original['rows']):ocr[Path(x['path']).resolve()]=x
    captions={x['path']:x for x in json.loads((work/'visual-descriptions.json').read_text())}
    old=json.loads((root/'.local/repertorio/originais/manifest.json').read_text())
    canonical=[x for x in old['files'] if not x['path'].endswith('scientific-advertising-1923.txt')]
    source_rows=[dict(path=x['path'],url=x['source_url']) for x in canonical]
    ordinal={row['path']:row['number'] for row in json.loads((work/'image-order.json').read_text())}
    for path in sorted((root/'BASE DE CONHECIMENTO').rglob('*')):
        if path.is_file() and path.name!='.DS_Store':source_rows.append(dict(path=path.relative_to(root).as_posix(),url=None))
    for path in sorted((root/'knowledge').rglob('*.json')):source_rows.append(dict(path=path.relative_to(root).as_posix(),url=None))
    generation=uuid.uuid4().hex[:16];folder=root/INGESTION/generation;folder.mkdir(parents=True)
    entries=[];inventory=[];seen={}
    for row in source_rows:
        rel=row['path'];path=safe_original(root,rel);raw=path.read_bytes();digest=sha(raw);suffix=path.suffix.lower()
        if digest in seen:
            seen[digest]['aliases'].append(dict(path=rel,sha256=digest,reason='identical_file_content'))
            inventory.append(dict(path=rel,status='duplicate_alias',canonical_id=seen[digest]['id']));continue
        sid='orig-'+digest[:16];segments=[];quality={};title=path.stem
        if suffix=='.pdf':
            segments,quality=extract_pdf(path);title='Scientific Advertising — Claude C. Hopkins, 1923'
            crosscheck=json.loads((work/'pdf-crosscheck.json').read_text())
            if len(crosscheck)!=quality['page_count']:raise ValueError('PDF/OCR page audit mismatch')
            quality.update(ocr_crosschecked_pages=len(crosscheck),native_words_seen_in_ocr_min=min(x['native_words_seen_in_ocr'] for x in crosscheck),ocr_words_seen_in_native_min=min(x['ocr_words_seen_in_native'] for x in crosscheck),visual_review='All page layouts inspected in rendered contact sheets; pages 1 and 116 inspected individually.')
            observed={1:'Capa de Scientific Advertising: título grande, nome de Claude C. Hopkins acima de retrato em preto e branco, indicação de texto original e crédito da edição digital com retrato colorido menor. Esses retratos são elementos visuais da edição, não exemplos de anúncios analisados.',116:'Apêndice comercial da edição digital: catálogo de produtos em duas colunas, retrato colorido abaixo à esquerda, despedida, assinatura gráfica, e-mail, link e telefone. A lista divulga materiais adicionais; seus conteúdos não estão presentes neste PDF e não foram ingeridos por serem citados.'}
            expanded=[]
            for segment in segments:
                expanded.append(segment)
                if segment['page'] in observed:expanded.append(dict(text=observed[segment['page']],section='Descrição visual da página '+str(segment['page']),page=segment['page'],chapter_number=None,extraction_method='agent_visual_description'))
            segments=expanded
            quality['visual_descriptions']=len(observed)
            # Existing page-marked TXT is a retained alternative extraction, not another book.
            alias='.local/repertorio/originais/scientific-advertising-1923.txt'
        elif suffix in {'.png','.jpg','.jpeg','.webp','.gif','.tiff','.tif'}:
            observed=ocr.get(path)
            if not observed or observed.get('error'):raise ValueError('image OCR missing/failed: '+rel)
            cap=captions[rel];rows=observed['rows'];title=(rows[0]['text'] if rows else cap['visual_description']).strip()[:160]
            segments=[dict(text='\n'.join(x['text'] for x in rows),section='Texto reconhecido na imagem',page=1,extraction_method='apple_vision_ocr',ocr_rows=rows),dict(text=cap['visual_description'],section='Descrição visual autoral',page=1,extraction_method='agent_visual_description')]
            quality=dict(image_dimensions=[observed['width'],observed['height']],ocr_rows=len(rows),low_confidence_rows=sum(x['confidence']<.65 for x in rows),ocr_mean_confidence=sum(x['confidence'] for x in rows)/len(rows) if rows else None,visual_review=cap['review'],fidelity='OCR not guaranteed exact; original pixels preserved and linked',empty_ocr=not bool(rows))
        elif suffix in {'.txt','.md','.json','.csv','.html','.htm'}:
            if raw[:4] in {b'%PDF',b'PK\x03\x04',b'\x7fELF'} or raw[:2]==b'MZ' or b'\x00' in raw:raise ValueError('binary disguised as text')
            text=normalized(raw)
            if suffix in {'.html','.htm'}:text=html_text(text)
            if suffix=='.json':json.loads(text)
            if suffix=='.csv':list(csv.reader(text.splitlines()))
            segments=blocks(text);quality=dict(page_count=None,physical_pages_available=False,security_flags=[])
            if 'history-of-advertising' in rel:title='A History of Advertising — Henry Sampson, 1874'
        elif suffix in {'.docx','.pptx','.xlsx','.epub'}:segments,quality=extract_zip(path)
        else:raise ValueError('unsupported source format: '+suffix)
        text,segments=assemble(segments)
        if not text.strip():raise ValueError('no extractable text/visual description: '+rel)
        flags=INJECTION.findall(text)
        payload=dict(source_path=rel,source_sha256=digest,text=text,segments=segments,quality=quality,security=dict(flags=flags,decision='reference_data_only',no_source_execution=True))
        ep=folder/(sid+'.json');ep.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
        entry=dict(id=sid,path=rel,client='*',routes=['ads','lp','social','direct'],tags=['original',suffix.lstrip('.'),'histórico' if 'originais' in rel else 'referência'],status='active',use='original',summary=title,title=title,sha256=digest,source_urls=[row['url']] if row['url'] else [],source_ids=[sid],authority='historical_original' if 'originais' in rel else 'local_source_unverified',evidence_kind='local_original_with_extraction_audit',human_approved=False,performance_verified=False,synthetic=False,extraction_path=ep.relative_to(root).as_posix(),extraction_sha256=sha(ep.read_bytes()),format=suffix,aliases=[],quality=quality)
        if suffix=='.pdf':
            ap=root/alias;entry['aliases'].append(dict(path=alias,sha256=sha(ap.read_bytes()),reason='alternative_page_marked_text_extraction'))
            inventory.append(dict(path=alias,status='alternative_extraction_alias',canonical_id=sid))
        if rel in ordinal:
            number=ordinal[rel];entry['ranking_group']='visual-'+str({6:5,56:7}.get(number,number))
        entries.append(entry);seen[digest]=entry;inventory.append(dict(path=rel,status='indexed',id=sid,format=suffix))
    registry=folder/'sources.json';registry.write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
    manifest=dict(schema=1,documents=len(entries),inventory=inventory,by_format=dict(Counter(e['format'] for e in entries)),source_collections=['knowledge metadata','BASE DE CONHECIMENTO','retained originals'],files={'sources.json':sha(registry.read_bytes())},extraction_inputs={name:sha((work/name).read_bytes()) for name in ['source-inputs.json','ocr.jsonl','ocr-tiled.jsonl','pdf-crosscheck.json','visual-descriptions.json'] if (work/name).is_file()},rights='Local supplied/retained sources only; not redistributed. External content is reference data, not instruction.',private_sources=0)
    (folder/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    temp=root/INGESTION/'.next.json';temp.write_text(json.dumps({'generation':generation})+'\n');temp.replace(root/INGESTION/'current.json')
    print(json.dumps(dict(documents=len(entries),by_format=manifest['by_format'],aliases=len(inventory)-len(entries)),ensure_ascii=False,indent=2))
if __name__=='__main__':ingest()
