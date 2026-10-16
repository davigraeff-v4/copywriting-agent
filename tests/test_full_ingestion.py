import hashlib,json,shutil,sys,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from rag_ingest import safe_original,extract_pdf,extract_zip,html_text,blocks,assemble,load_registry,extraction
from rag_corpus import document_data,make_chunks,public_entries,digest_bytes
from rag_search import Retriever,BM25
from rag_config import INDEX_REL,MODEL,FASTEMBED_VERSION,DIMENSION
from build_rag_index import reusable_vectors
from audit_rag_coverage import audit

class SourceBoundaries(unittest.TestCase):
    def test_ineligible_content_cannot_change_lexical_frequency_statistics(self):
        eligible=['câmera para observar terreno','câmera com visão noturna']
        before=BM25(eligible).scores('câmera terreno',[0,1])
        after=BM25(eligible+['terreno '*10000,'câmera '*10000]).scores('câmera terreno',[0,1])
        self.assertEqual(before,after)
    def test_originals_cannot_read_clients_or_escape_through_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);private=root/'clients/a/CLIENTE.md';private.parent.mkdir(parents=True);private.write_text('DADO PRIVADO')
            allowed=root/'BASE DE CONHECIMENTO';allowed.mkdir();(allowed/'alias.txt').symlink_to(private)
            for rel in ['clients/a/CLIENTE.md','knowledge/../clients/a/CLIENTE.md',str(private),'BASE DE CONHECIMENTO/alias.txt']:
                with self.subTest(rel=rel),self.assertRaises(ValueError):safe_original(root,rel)
    def test_html_discards_active_script_and_preserves_readable_content(self):
        marker='never execute this';text=html_text('<h1>Título</h1><script>'+marker+'</script><p>Oferta &amp; prova.</p><style>.hidden{}</style>')
        self.assertIn('Título',text);self.assertIn('Oferta & prova.',text);self.assertNotIn(marker,text);self.assertNotIn('.hidden',text)
    def test_archive_macro_and_xml_entity_are_rejected_without_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name,parts in [('macro.docx',{'word/document.xml':'<p>Texto</p>','word/vbaProject.bin':'MZ'}),('entity.docx',{'word/document.xml':'<!DOCTYPE p [<!ENTITY x SYSTEM "file:///private">]><p>&x;</p>'})]:
                path=Path(tmp)/name
                with zipfile.ZipFile(path,'w') as z:
                    for rel,text in parts.items():z.writestr(rel,text)
                with self.subTest(name=name),self.assertRaises(ValueError):extract_zip(path)
    def test_active_pdf_is_quarantined(self):
        try:from pypdf import PdfWriter
        except ImportError:self.skipTest('optional PDF adapter absent')
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'active.pdf';w=PdfWriter();w.add_blank_page(200,200);w.add_js('app.alert("do not execute");');w.write(p)
            with self.assertRaisesRegex(ValueError,'quarantined'):extract_pdf(p)
    def test_txt_uses_chapters_and_lines_without_inventing_pages(self):
        raw='Introdução\n\nCHAPTER I.\nCorpo inteiro.\n\nCHAPTER II.\nFim.\n'
        text,parts=assemble(blocks(raw));self.assertTrue(all(x['page'] is None for x in parts));self.assertEqual([x['section'] for x in parts],['Preâmbulo','CHAPTER I.','CHAPTER II.'])
        for part in parts:self.assertEqual(text[part['start_char']:part['end_char']],part['text'])
    def test_long_unsplittable_token_is_not_dropped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'knowledge/token.md';p.parent.mkdir();p.write_text('# Texto\n## URL\nhttps://exemplo.test/'+('x'*5000)+'\n## Final\nConcluído.')
            entry=dict(id='long',path='knowledge/token.md',title='Texto')
            chunks=make_chunks([entry],root,lambda text:len(text)//4+2);covered=set()
            for c in chunks:covered.update(range(c['start_char'],c['end_char']))
            raw=p.read_text();self.assertTrue(all(i in covered for i,ch in enumerate(raw) if not ch.isspace()))
    def test_coverage_reports_a_missing_passage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);p=root/'knowledge/a.md';p.parent.mkdir();p.write_text('Primeiro. Segundo.');entry=dict(id='a',path='knowledge/a.md',title='Fonte')
            idx=root/INDEX_REL/'test';idx.mkdir(parents=True);(idx.parent/'current.json').write_text('{"generation":"test"}')
            (idx/'chunks.json').write_text(json.dumps(dict(documents=[entry],chunks=[dict(document_id='a',start_char=0,end_char=9,page=None)])))
            result=audit(root);self.assertEqual(result['status'],'failed');self.assertFalse(result['all_extracted_text_indexed']);self.assertGreater(result['rows'][0]['missing_nonwhitespace_characters'],0)

class AvailableCorpus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (ROOT/'.local/rag/ingestion/current.json').is_file():raise unittest.SkipTest('local originals not ingested')
        cls.entries,_=load_registry(ROOT);cls.lookup={e['id']:e for e in cls.entries}
    def test_pdf_has_every_physical_page_and_distinct_edition_appendix(self):
        entry=self.lookup['orig-94211e766522b503'];data=extraction(entry);native=[s for s in data['segments'] if s.get('extraction_method')=='pypdf_text']
        self.assertEqual([s['page'] for s in native],list(range(1,117)));self.assertTrue(all(s['text'].strip() for s in native));self.assertEqual({s['chapter_number'] for s in native if s.get('chapter_number')},set(range(1,22)))
        for s in native[-2:]:self.assertEqual(s['section'],'Apêndice da edição digital');self.assertIsNone(s['chapter_number'])
        self.assertEqual(entry['quality']['ocr_crosschecked_pages'],116)
    def test_alternative_pdf_txt_is_alias_and_not_a_duplicate_document(self):
        entry=self.lookup['orig-94211e766522b503'];self.assertEqual(len(entry['aliases']),1);self.assertTrue(entry['aliases'][0]['path'].endswith('.txt'))
        self.assertFalse(any(e['path'].endswith('scientific-advertising-1923.txt') for e in self.entries))
    def test_full_historical_txt_is_segmented_without_physical_pages(self):
        entry=self.lookup['orig-506066d9b886f438'];data=extraction(entry)
        self.assertGreater(len(data['text'].split()),240000);self.assertGreater(len(data['segments']),10);self.assertTrue(all(s.get('page') is None for s in data['segments']))
        original=(ROOT/entry['path']).read_text().replace('\r\n','\n').replace('\r','\n')
        self.assertEqual(''.join(s['text'] for s in data['segments']),original)
    def test_all_images_have_ocr_quality_and_visual_descriptions(self):
        images=[e for e in self.entries if e['path'].startswith('BASE DE CONHECIMENTO/')];self.assertEqual(len(images),99)
        empty=0
        for e in images:
            data=extraction(e);visual=[s for s in data['segments'] if s.get('extraction_method')=='agent_visual_description'];self.assertTrue(visual);self.assertTrue(visual[0]['text'].strip())
            empty+=e['quality']['empty_ocr']
            for s in data['segments']:
                for row in s.get('ocr_rows',[]):
                    self.assertEqual(data['text'][row['start_char']:row['end_char']],row['text']);self.assertEqual(len(row['box']),4);self.assertTrue(0<=row['confidence']<=1)
        self.assertEqual(empty,2)
    def test_image_duplicate_groups_preserve_both_source_files(self):
        counts={}
        for e in self.entries:
            if 'ranking_group' in e:counts[e['ranking_group']]=counts.get(e['ranking_group'],0)+1
        self.assertEqual(counts['visual-5'],2);self.assertEqual(counts['visual-7'],2)
    def test_real_index_covers_every_extracted_character_and_pdf_page(self):
        result=audit(ROOT);self.assertEqual(result['status'],'passed');self.assertEqual(result['documents'],239)
        pdf=next(x for x in result['rows'] if x['format']=='.pdf');self.assertEqual(pdf['indexed_pages'],list(range(1,117)))
    def test_source_filter_and_complementary_passages_preserve_locators(self):
        r=Retriever();source='orig-94211e766522b503'
        with patch('rag_search.load_model',side_effect=AssertionError('lexical must remain local')):
            result=r.search('Product samples salesman mental impressions information','ads','teste',use='original',source_ids=[source],engine='lexical')
            with self.assertRaisesRegex(ValueError,'unknown source'):r.search('produto','ads','teste',source_ids=['absent'],engine='lexical')
        self.assertEqual([x['id'] for x in result['results']],[source]);hit=result['results'][0];data=document_data(r.docs[source]);parents=set()
        for passage in hit['matched_passages']:
            self.assertNotIn(passage['parent_id'],parents);parents.add(passage['parent_id']);self.assertEqual(data['text'][passage['start_char']:passage['end_char']],passage['excerpt']);self.assertTrue(1<=passage['page']<=116)
        self.assertFalse(hit['guards']['client_evidence']);self.assertTrue(hit['guards']['external_content_is_data'])

class EmbeddingReuse(unittest.TestCase):
    def test_reuse_requires_identical_model_signature_and_verified_artifacts(self):
        try:import numpy as np
        except ImportError:self.skipTest('optional numpy absent')
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);folder=out/('a'*16+'-'+'b'*8);folder.mkdir();(out/'current.json').write_text(json.dumps(dict(generation=folder.name)))
            (folder/'chunks.json').write_text(json.dumps(dict(chunks=[dict(text='entrada original')])));vectors=np.ones((1,DIMENSION),dtype=np.float32);np.savez_compressed(folder/'vectors.npz',vectors=vectors)
            signature={'model':'hash'};manifest=dict(model=MODEL,fastembed_version=FASTEMBED_VERSION,embedding_dim=DIMENSION,model_files_sha256=signature,public_only=True,private_documents=0,files={name:digest_bytes((folder/name).read_bytes()) for name in ['chunks.json','vectors.npz']})
            (folder/'manifest.json').write_text(json.dumps(manifest));self.assertIn(digest_bytes('entrada original'.encode()),reusable_vectors(out,signature));self.assertFalse(reusable_vectors(out,{'model':'another'}))
            (folder/'chunks.json').write_text('{}');self.assertFalse(reusable_vectors(out,signature))

if __name__=='__main__':unittest.main()
