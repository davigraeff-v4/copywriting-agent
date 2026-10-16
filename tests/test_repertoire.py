import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from retrieve import load_entries,retrieve
from validate_repertoire import validate_repertoire

class Repertoire(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        shutil.copytree(ROOT/'knowledge/repertorio',self.root/'knowledge/repertorio')
        self.catalog=self.root/'knowledge/repertorio/catalogo.json'
        self.sources=self.root/'knowledge/repertorio/fontes.json'

    def mutate(self,path,change):
        data=json.loads(path.read_text());change(data);path.write_text(json.dumps(data,ensure_ascii=False))

    def test_complete_corpus_contract(self):
        report=validate_repertoire(self.root)
        self.assertEqual(report['errors'],[])
        self.assertEqual(report['units'],100)
        self.assertEqual(report['sources'],90)
        self.assertEqual(report['by_primary_route']['ads']+report['by_primary_route']['lp'],79)
        self.assertEqual(report['by_batch'],{'lote-01':60,'lote-02':40})
        self.assertEqual(report['complete_piece_scopes'],{'single_static_creative':20,'commercial_page_text':12,'archived_email':8})

    def test_changed_material_requires_new_integrity_record(self):
        item=json.loads(self.catalog.read_text())[0]
        p=self.root/item['path'];p.write_text(p.read_text()+'\nTexto alterado.\n')
        errors=validate_repertoire(self.root)['errors']
        self.assertTrue(any('content hash mismatch' in e for e in errors))

    def test_no_synthetic_feedback_or_performance_promotion(self):
        def edit(items):
            rev=next(i for i in items if i['kind']=='revisao')
            rev.update(synthetic=False,human_approved=True,performance_verified=True,use='positive')
        self.mutate(self.catalog,edit)
        errors=validate_repertoire(self.root)['errors']
        for expected in ['unlabeled synthetic','unearned approval','invalid retrieval use']:
            self.assertTrue(any(expected in e for e in errors),expected)

    def test_flagged_source_and_unknown_source_are_rejected(self):
        self.mutate(self.sources,lambda s:s[0].update(security_flags=['untrusted instruction']))
        self.mutate(self.catalog,lambda i:i[0].update(source_ids=['missing']))
        errors=validate_repertoire(self.root)['errors']
        self.assertTrue(any('source security review' in e for e in errors))
        self.assertTrue(any('missing source' in e for e in errors))

    def test_private_or_outside_path_is_rejected(self):
        for path in ['clients/other/CLIENTE.md','../../outside.md']:
            with self.subTest(path=path):
                data=json.loads(self.catalog.read_text());data[0]['path']=path
                self.catalog.write_text(json.dumps(data))
                self.assertTrue(any('outside repertoire' in e for e in validate_repertoire(self.root)['errors']))

    def test_duplicate_identity_or_material_is_rejected(self):
        self.mutate(self.catalog,lambda data:data.append(copy.deepcopy(data[0])))
        errors=validate_repertoire(self.root)['errors']
        self.assertTrue(any('duplicate unit id' in e for e in errors))
        self.assertTrue(any('duplicate indexed file' in e for e in errors))

    def test_existing_retrieval_can_select_each_route_and_use(self):
        entries=json.loads(self.catalog.read_text())
        probes=[('tese progressão','lp','structure','rep-01-r05'),
                ('compatibilidade equipamento','ads','structure','rep-01-r01'),
                ('pauta orgânico','social','guidance','rep-01-m13'),
                ('assunto preheader','direct','guidance','rep-01-m14'),
                ('mecanismo demonstração','lp','positive','rep-01-e01')]
        for query,route,use,expected in probes:
            with self.subTest(query=query):
                result=retrieve(query,entries,route,'cliente-isolado',use=use,root=self.root)
                self.assertIn(expected,[i['id'] for i in result])

    def test_defaults_include_corpus_and_explicit_index_preserves_scope(self):
        core=self.root/'knowledge/retrieval-index.json';core.write_text('[{"id":"core"}]')
        self.assertEqual(len(load_entries(root=self.root)),101)
        self.assertEqual(load_entries([str(core)],root=self.root),[{'id':'core'}])
        self.catalog.unlink()
        self.assertEqual(load_entries(root=self.root),[{'id':'core'}])

    def test_partial_piece_cannot_be_promoted_to_complete_reference(self):
        self.mutate(self.catalog,lambda items:items[-1].update(complete_piece=False))
        self.assertTrue(any('incomplete/unknown piece' in e for e in validate_repertoire(self.root)['errors']))

    def test_component_map_must_match_observed_study(self):
        self.mutate(self.catalog,lambda items:items[-1].update(components=['headline isolada'],component_count=1))
        self.assertTrue(any('incomplete component map' in e for e in validate_repertoire(self.root)['errors']))
        self.mutate(self.catalog,lambda items:items[-1].update(components=['um','dois','três'],component_count=3))
        self.assertTrue(any('component map mismatch' in e for e in validate_repertoire(self.root)['errors']))

    def test_archive_attribution_does_not_prove_real_delivery(self):
        self.mutate(self.sources,lambda sources:sources[-1].update(independent_delivery_verified=True))
        self.assertTrue(any('piece provenance mismatch' in e for e in validate_repertoire(self.root)['errors']))

    def test_synthetic_piece_and_campaign_variants_cannot_inflate_second_batch(self):
        self.mutate(self.catalog,lambda items:items[-1].update(synthetic=True))
        self.mutate(self.sources,lambda sources:sources[-1].update(url=sources[-2]['url']))
        errors=validate_repertoire(self.root)['errors']
        self.assertTrue(any('wrong provenance type' in e for e in errors))
        self.assertTrue(any('duplicate external source URL' in e for e in errors))

    def test_visual_piece_needs_integral_observed_asset(self):
        self.mutate(self.sources,lambda sources:sources[-1].pop('observed_asset_url'))
        self.assertTrue(any('missing observed integral asset' in e for e in validate_repertoire(self.root)['errors']))

    def test_new_examples_are_retrievable_without_changing_lexical_algorithm(self):
        entries=json.loads(self.catalog.read_text())
        probes=[('Amarok câmera terreno','ads','rep-02-a01'),
                ('Intelbras FR101 instalação','lp','rep-02-l07'),
                ('Figma onboarding primeira ação','direct','rep-02-d01'),
                ('McDonald’s desejo situação','social','rep-02-a02')]
        for query,route,expected in probes:
            result=retrieve(query,entries,route,'cliente-isolado',use='positive',root=self.root)
            self.assertIn(expected,[i['id'] for i in result])

    def test_claims_from_public_brand_are_never_client_evidence(self):
        self.mutate(self.sources,lambda sources:sources[-1].update(not_client_evidence=False))
        self.assertTrue(any('source not isolated' in e for e in validate_repertoire(self.root)['errors']))

if __name__=='__main__':unittest.main()
