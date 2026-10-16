import hashlib,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from rag_search import Retriever,BM25
from rag_ranking import rank_tokens,metadata_penalty,SEMANTIC_DOCUMENT_FLOOR
from rag_corpus import digest_bytes
from rag_config import MODEL,FASTEMBED_VERSION,DIMENSION
from rag_semantic_channel import CHANNEL_REL,encoder_hash,load_channel,inspect_channel,channel_stamp

class RankingBehavior(unittest.TestCase):
    def synthetic(self,root):
        p=root/'knowledge/one.md';p.parent.mkdir();p.write_text('# Instalação\n\n## Leitura\nSensor disponível.\n\n## Limites\nMaterial técnico.\n\n## Próximo\nMais contexto.\n')
        return dict(id='one',path='knowledge/one.md',title='Instalação',summary='Referência fictícia',status='active',use='guidance',client='*',routes=['ads'],tags=[],sha256=digest_bytes(p.read_bytes()))
    def test_plural_and_english_function_words_are_normalized(self):
        self.assertEqual(rank_tokens('the product samples and letters for salesmen'),rank_tokens('product sample letter salesman'))
        self.assertEqual(rank_tokens('planos'),rank_tokens('plano'))
    def test_provenance_and_json_remain_searchable_for_explicit_metadata_queries(self):
        d=dict(path='knowledge/catalogo.json');c=dict(section='Proveniência')
        self.assertGreater(metadata_penalty(d,c,'argumento de venda'),0)
        self.assertEqual(metadata_penalty(d,c,'URL e hash da fonte'),0)
        self.assertEqual(metadata_penalty(dict(path='knowledge/fonte.md'),c,'proveniência'),0)
    def test_field_overlap_is_evaluated_across_body_and_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);entry=self.synthetic(root)
            with patch('rag_search.public_entries',return_value=[entry]),patch('rag_search.load_model',side_effect=AssertionError('no embeddings')):
                r=Retriever(root);out=r.search('sensor instalação avaliar temperatura conhecer','ads','teste',engine='lexical')
            self.assertTrue(out['results']);self.assertEqual(out['results'][0]['id'],'one')
            self.assertFalse(BM25(['Sensor disponível.']).scores('sensor instalação avaliar temperatura conhecer',[0]))
    def test_one_semantic_spike_without_section_support_abstains(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);entry=self.synthetic(root)
            with patch('rag_search.public_entries',return_value=[entry]):r=Retriever(root)
            r.generation=root;r.manifest={}
            scores={i:(.60 if i==0 else .20) for i in range(len(r.chunks))}
            with patch.object(r,'_refresh'),patch.object(r,'_semantic',return_value=scores):out=r.search('orbital aerolito helicoidal quantum','ads','teste',engine='semantic')
            self.assertFalse(out['results']);self.assertFalse(out['semantic_used'])
    def test_page_and_section_filters_never_broaden(self):
        r=Retriever();source='orig-94211e766522b503'
        with patch('rag_search.load_model',side_effect=AssertionError('no model for lexical')):
            out=r.search('letters headline attention','direct','teste',use='original',engine='lexical',source_ids=[source],page=104,section='Chapter 19')
            empty=r.search('samples','ads','teste',use='original',engine='lexical',source_ids=[source],page=9999)
        self.assertTrue(out['results']);self.assertFalse(empty['results']);self.assertEqual(empty['eligible_chunks'],0)
        for h in out['results']:
            self.assertEqual(h['locator']['page'],104)
            for p in h['matched_passages']:self.assertEqual(p['page'],104);self.assertIn('Chapter 19',p['section'])
    def test_page_filter_precedes_semantic_similarity(self):
        r=Retriever();captured=[]
        def dense(query,allowed):captured.extend(allowed);return {i:.8 for i in allowed}
        with patch.object(r,'_semantic',side_effect=dense):out=r.search('amostras','ads','teste',use='original',engine='semantic',source_ids=['orig-94211e766522b503'],page=75)
        self.assertTrue(captured);self.assertTrue(out['results'])
        self.assertTrue(all(r.chunks[i]['page']==75 and r.chunks[i]['document_id']=='orig-94211e766522b503' for i in captured))
    def test_invalid_location_filter_is_refused_before_embeddings(self):
        r=Retriever()
        with patch('rag_search.load_model',side_effect=AssertionError('must not embed')):
            for kw in [dict(page=0),dict(page=True),dict(section='')]:
                with self.subTest(kw=kw),self.assertRaises(ValueError):r.search('texto','ads','teste',**kw)

class BodyChannelIntegrity(unittest.TestCase):
    def setUp(self):
        try:import numpy as np
        except ImportError:self.skipTest('optional NumPy absent')
        self.np=np;self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.folder=self.root/CHANNEL_REL/('a'*16+'-'+'b'*8);self.folder.mkdir(parents=True)
        (self.folder.parent/'current.json').write_text(json.dumps(dict(generation=self.folder.name)))
        self.chunks=[dict(id='one:0000',document_id='one',parent_id='s00000',start_char=0,end_char=6,section='Texto')]
        self.signature={'test':'weights'};self.fingerprint='f'*64;self.base='c'*64
        self.inputs=[dict(chunk_id='one:0000',document_id='one',parent_id='s00000',start_char=0,end_char=6,text='Teste.',text_sha256=digest_bytes(b'Teste.'),token_count=4)]
        (self.folder/'inputs.json').write_text(json.dumps(self.inputs));v=np.ones((1,DIMENSION),dtype=np.float32);v/=np.linalg.norm(v,axis=1,keepdims=True);np.savez_compressed(self.folder/'vectors.npz',vectors=v)
        self.manifest=dict(source_fingerprint=self.fingerprint,encoder_hash=encoder_hash(),base_chunks_sha256=self.base,model=MODEL,fastembed_version=FASTEMBED_VERSION,model_files_sha256=self.signature,dimensions=DIMENSION,private_documents=0,chunk_count=1,files={n:digest_bytes((self.folder/n).read_bytes()) for n in ['inputs.json','vectors.npz']})
        self.save_manifest()
    def save_manifest(self):(self.folder/'manifest.json').write_text(json.dumps(self.manifest))
    def load(self):return load_channel(self.root,self.fingerprint,self.chunks,self.signature,self.base)
    def test_numeric_channel_is_bound_to_base_chunks_model_and_sources(self):
        v,m=self.load();self.assertEqual(v.shape,(1,384));self.assertTrue(self.np.allclose(self.np.linalg.norm(v,axis=1),1))
        for fp,sig,base in [('changed',self.signature,self.base),(self.fingerprint,{'other':'weights'},self.base),(self.fingerprint,self.signature,'changed')]:
            with self.subTest(fp=fp,sig=sig,base=base),self.assertRaises(ValueError):load_channel(self.root,fp,self.chunks,sig,base)
    def test_corruption_is_refused_and_stamp_changes(self):
        before=channel_stamp(self.root);(self.folder/'vectors.npz').write_bytes(b'corrupted')
        self.assertNotEqual(before,channel_stamp(self.root))
        with self.assertRaisesRegex(ValueError,'artifact corrupt'):self.load()
    def test_private_document_identity_cannot_be_forged_with_new_hash(self):
        self.inputs[0]['document_id']='clients/private';(self.folder/'inputs.json').write_text(json.dumps(self.inputs))
        self.manifest['files']['inputs.json']=digest_bytes((self.folder/'inputs.json').read_bytes());self.save_manifest()
        with self.assertRaisesRegex(ValueError,'identity mismatch'):self.load()
    def test_pointer_escape_does_not_read_client_data(self):
        (self.folder.parent/'current.json').write_text('{"generation":"../../clients"}')
        with self.assertRaisesRegex(ValueError,'pointer'):self.load()
    def test_object_vectors_are_refused_without_pickle_execution(self):
        self.np.savez_compressed(self.folder/'vectors.npz',vectors=self.np.asarray([['data']],dtype=object))
        self.manifest['files']['vectors.npz']=digest_bytes((self.folder/'vectors.npz').read_bytes());self.save_manifest()
        with self.assertRaises(ValueError):self.load()
    def test_cached_retriever_detects_body_artifact_mutation(self):
        r=object.__new__(Retriever);r.root=self.root;r.fingerprint=self.fingerprint;r.chunks=self.chunks;r.docs={'one':dict(path='knowledge/one.md',use='guidance')};r.manifest=dict(fastembed_version=FASTEMBED_VERSION,model_files_sha256=self.signature,files={'chunks.json':self.base})
        r.query_vectors={'query':self.np.ones(DIMENSION,dtype=self.np.float32)/self.np.sqrt(DIMENSION)};r.vectors=r.query_vectors['query'].reshape(1,-1);r.body_vectors=None;r.body_channel_stamp=None;r.body_channel_error=None
        r._semantic('query',[0]);self.assertIsNotNone(r.body_vectors)
        (self.folder/'vectors.npz').write_bytes(b'changed')
        r._semantic('query',[0]);self.assertIsNone(r.body_vectors);self.assertIn('artifact corrupt',r.body_channel_error)

if __name__=='__main__':unittest.main()
