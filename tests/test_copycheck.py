"""Technical fixtures test gates; fabricated test scores are never campaign reviews."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import copycheck as c


def fixture_review(doc):
    r = c.review_template(doc)
    r['reviewer'] = 'UNIT TEST FIXTURE, not an editorial evaluation'
    f = doc['fields'][0]
    for group in ('general', 'humanization'):
        for key in r[group]:
            r[group][key] = dict(score=10, field_id=f['id'], quote=f['text'], reason='Synthetic gate fixture')
    for group in ('claim_checks', 'constraint_checks'):
        for key in r[group]:
            r[group][key] = dict(status='pass', reason='Synthetic gate fixture')
    r['claim_inventory'] = dict(status='pass', reason='Synthetic gate fixture')
    paths = [('context', 'knowledge/README.md'), ('context', 'knowledge/metodologia-thamy.md'),
             ('context', f"knowledge/rotas/{doc['route']}.md"),
             ('production', 'knowledge/vicios-ia-humanizacao.md'), ('review', 'knowledge/vicios-ia-humanizacao.md')]
    r['readings'] = [dict(phase=phase, path=p, sha256=hashlib.sha256((c.ROOT/p).read_bytes()).hexdigest(),
                          read_at='test-fixture-not-a-real-reading') for phase, p in paths]
    return r


class Gates(unittest.TestCase):
    def setUp(self):
        self.doc = c.load(c.ROOT/'tests/fixtures/valid-delivery.json')

    def test_clean_draft_needs_review(self):
        self.assertEqual(c.check(self.doc)['status'], 'needs_editorial_review')

    def test_complete_review_reaches_human_gate_only(self):
        self.assertEqual(c.check(self.doc, fixture_review(self.doc))['status'], 'ready_for_human_approval')

    def test_literal_failures_even_with_high_scores(self):
        for text in ['Direto pra sua oficina.', 'Consulte — veja o catálogo.', 'Não é sobre pneu, é sobre sua oficina.',
                     'Locação não é só uma forma de pagar. É como a operação continua rodando.',
                     'A melhor solução.', 'Confira [confirmar preço].']:
            with self.subTest(text=text):
                self.doc['fields'][0]['text'] = text
                self.assertEqual(c.check(self.doc, fixture_review(self.doc))['status'], 'blocked')

    def test_word_boundaries_and_valid_portuguese(self):
        self.doc['fields'][0]['text'] = 'Um processo tão prático quanto preciso para profissionais.'
        self.assertEqual(c.check(self.doc)['status'], 'needs_editorial_review')

    def test_context_or_copy_edit_invalidates_review(self):
        for key in ('context', 'copy'):
            with self.subTest(key=key):
                d = copy.deepcopy(self.doc); r = fixture_review(d)
                if key == 'context': d['context']['barrier'] = 'Uma nova barreira'
                else: d['fields'][0]['text'] = 'Consulte as peças disponíveis'
                self.assertIn('stale review', ' '.join(c.check(d, r)['errors']))

    def test_policy_hash_invalidates_review(self):
        r = fixture_review(self.doc); r['policy_sha256'] = 'old'
        self.assertEqual(c.check(self.doc, r)['status'], 'blocked')

    def test_claim_cannot_use_hypothesis(self):
        self.doc['facts'][0]['status'] = 'hypothesis'
        self.assertEqual(c.check(self.doc)['status'], 'blocked')

    def test_claim_must_quote_exact_copy(self):
        self.doc['claims'][0]['quote'] = 'Dado que não está na copy'
        self.assertEqual(c.check(self.doc)['status'], 'blocked')

    def test_claim_inventory_is_required(self):
        r=fixture_review(self.doc); r['claim_inventory']['status']='pending'
        self.assertEqual(c.check(self.doc, r)['status'], 'blocked')

    def test_notes_are_not_publishable_copy(self):
        self.doc['notes'] = 'Reprovado: pra — não é sobre'
        self.assertEqual(c.check(self.doc)['status'], 'needs_editorial_review')

    def test_form_is_exact_and_ordered(self):
        self.doc['requirements']['forms']['dobra-1'] = ['Nome', 'E-mail']
        self.assertEqual(c.check(self.doc)['status'], 'blocked')

    def test_section_count(self):
        self.doc['requirements']['sections'] = 5
        self.assertEqual(c.check(self.doc)['status'], 'blocked')

    def test_short_sentences_need_explained_review(self):
        self.doc['fields'][0]['text'] = 'Peças certas. Equipe pronta. Consulte agora.'
        r=fixture_review(self.doc)
        self.assertEqual(c.check(self.doc,r)['status'],'blocked')
        r['warning_resolutions']=[dict(field_id=self.doc['fields'][0]['id'], rule='telegraphic_sequence', reason='Test fixture exception')]
        self.assertEqual(c.check(self.doc,r)['status'],'ready_for_human_approval')

    def test_unmapped_number_warns(self):
        self.doc['fields'][0]['text'] = 'Há 25 anos atendendo oficinas'
        self.assertIn('unmapped_number', [i['rule'] for i in c.check(self.doc)['issues']])

    def test_human_score_must_follow_scale(self):
        r=fixture_review(self.doc); r['humanization']['ritmo']['score']=9
        self.assertEqual(c.check(self.doc,r)['status'],'blocked')

    def test_low_critical_score_cannot_hide_in_average(self):
        r=fixture_review(self.doc); r['general']['evidencia']['score']=7
        self.assertEqual(c.check(self.doc,r)['status'],'blocked')

    def test_no_reading_receipt_no_release(self):
        r=fixture_review(self.doc); r['readings'].pop()
        self.assertEqual(c.check(self.doc,r)['status'],'blocked')

    def test_routing_index_change_does_not_stale_campaign_review(self):
        r=fixture_review(self.doc)
        receipt=next(x for x in r['readings'] if x['path']=='knowledge/README.md')
        receipt['sha256']='older-routing-index'
        self.assertEqual(c.check(self.doc,r)['status'],'ready_for_human_approval')

    def test_methodology_change_still_stales_review(self):
        r=fixture_review(self.doc)
        receipt=next(x for x in r['readings'] if x['path']=='knowledge/metodologia-thamy.md')
        receipt['sha256']='old-methodology'
        self.assertEqual(c.check(self.doc,r)['status'],'blocked')

    def test_constraint_blocks(self):
        self.doc['constraints'][0]['forbidden_terms']=['peças']
        self.doc['fields'][0]['text']='Consulte as peças disponíveis'
        self.assertEqual(c.check(self.doc,fixture_review(self.doc))['status'],'blocked')

    def test_social_requires_feasible_assets_but_not_sales_offer(self):
        d=self.doc; d['route']='social'; d['context'].pop('offer'); d['fields']=[f for f in d['fields'] if f['role'] not in ('cta','form_label')]; d['requirements'].pop('forms')
        self.assertEqual(c.check(d)['status'],'blocked')
        d['outline'][0].update(source_ids=['s1'], asset='Foto existente fornecida', feasibility='Disponível no briefing', audience_value='Entender como consultar o catálogo')
        self.assertEqual(c.check(d)['status'],'needs_editorial_review')

    def test_missing_review_exact_evidence_blocks(self):
        r=fixture_review(self.doc); r['general']['voz']['quote']='Não existe'
        self.assertEqual(c.check(self.doc,r)['status'],'blocked')

    def test_malformed_inputs_fail_closed(self):
        cases=[None, [], {'schema_version':2}]
        for key,value in [('fields',[{'id':[]}]),('requirements',{'forms':[]}),('fields',[{'id':'x','section':[]}])]:
            d=copy.deepcopy(self.doc); d[key]=value; cases.append(d)
        for d in cases:
            with self.subTest(doc=d): self.assertEqual(c.check(d)['status'],'blocked')
        self.assertEqual(c.check(self.doc,[])['status'],'blocked')

    def test_cli_refuses_draft_render_and_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); delivery=p/'delivery.json'; review=p/'review.json'; output=p/'copy.md'
            delivery.write_text(json.dumps(self.doc)); review.write_text(json.dumps(fixture_review(self.doc)))
            base=[sys.executable,str(c.ROOT/'scripts/copycheck.py'),str(delivery)]
            r=subprocess.run(base+['--render',str(output)],capture_output=True,text=True)
            self.assertNotEqual(r.returncode,0); self.assertFalse(output.exists())
            r=subprocess.run(base+['--review',str(review),'--render',str(output)],capture_output=True,text=True)
            self.assertEqual(r.returncode,0); self.assertEqual(output.read_text(),c.render(self.doc))
            original=output.read_bytes()
            r=subprocess.run(base+['--review',str(review),'--render',str(output)],capture_output=True,text=True)
            self.assertNotEqual(r.returncode,0); self.assertEqual(output.read_bytes(),original)

if __name__=='__main__': unittest.main()
