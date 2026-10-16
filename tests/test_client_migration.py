import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import migrate_clients as migration
from client_brief import brief
from client_paths import resolve_reference
from retrieve import retrieve


class Migration(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.write('clients/current/a.md', '# A\n\nRegra vigente.\n\n## Campanhas\n\nAprovação pendente.\n')
        self.write('clients/a.md', 'Histórico original, não reconfirmado.')
        self.write('campaigns/a/demo/v1/delivery.json', '{"version":"v1"}')
        self.write('campaigns/a/demo/v1/review.json', '{"score":10}')
        self.write('campaigns/a/demo/v1/final.md', 'Copy original')
        self.write('campaigns/a/demo/v2/final.md', 'Copy diferente')
        self.write('campaigns/a/demo/v2/feedback.md', 'Aprovação apenas da peça 2 pelo gestor. Publicação não informada.')
        self.write('outputs/approved/a-demo-v1.md', 'Copy original')
        self.write('examples/approved/a-demo-v1.md', 'Copy original')
        self.write('clients/current/b.md', 'Dados de outro cliente')
        self.write('campaigns/b/demo/v1/final.md', 'Copy original')

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return path

    def test_dry_run_and_roundtrip_preserve_bytes_and_signed_json(self):
        manifest = migration.plan(['a'], self.root)
        before = {i['source']: (self.root / i['source']).read_bytes() for i in manifest['moves']}
        self.assertFalse((self.root / 'clients/a').exists())
        result = migration.apply(manifest, self.root)
        self.assertEqual(result['status'], 'passed')
        self.assertEqual(migration.verify(manifest, self.root)['errors'], [])
        for old, content in before.items():
            self.assertFalse((self.root / old).exists())
            self.assertEqual(resolve_reference(old, self.root).read_bytes(), content)
        self.assertEqual((self.root / 'campaigns/b/demo/v1/final.md').read_text(), 'Copy original')
        self.assertEqual(result['original_files'] - result['canonical_files'], 2)
        migration.rollback(self.root / result['transaction'], self.root)
        for old, content in before.items():
            self.assertEqual((self.root / old).read_bytes(), content)
        self.assertFalse((self.root / 'clients/a').exists())

    def test_collision_preflight_changes_nothing(self):
        manifest = migration.plan(['a'], self.root)
        self.write(manifest['moves'][0]['destination'], 'existing different data')
        with self.assertRaises(ValueError):
            migration.apply(manifest, self.root)
        self.assertTrue(all((self.root / i['source']).is_file() for i in manifest['moves']))
        self.assertFalse((self.root / '.local/client-path-map.json').exists())

    def test_changed_source_invalidates_plan(self):
        manifest = migration.plan(['a'], self.root)
        self.write(manifest['moves'][0]['source'], 'changed')
        with self.assertRaises(ValueError):
            migration.apply(manifest, self.root)
        self.assertFalse((self.root / 'clients/a').exists())

    def test_escape_or_cross_client_destination_refused(self):
        for destination in ('../escape', 'clients/b/stolen.md'):
            manifest = migration.plan(['a'], self.root)
            manifest['moves'][0]['destination'] = destination
            with self.assertRaises(ValueError):
                migration.apply(manifest, self.root)

    def test_apply_twice_refused_without_overwrite(self):
        manifest = migration.plan(['a'], self.root)
        migration.apply(manifest, self.root)
        with self.assertRaises(ValueError):
            migration.apply(manifest, self.root)
        self.assertEqual(migration.verify(manifest, self.root)['status'], 'passed')

    def test_copy_failure_restores_originals(self):
        manifest = migration.plan(['a'], self.root)
        original = Path.open
        def failing(path, *args, **kwargs):
            if path.resolve() == (self.root / 'clients/a/CLIENTE.md').resolve():
                raise OSError('synthetic write failure')
            return original(path, *args, **kwargs)
        with patch.object(Path, 'open', failing):
            with self.assertRaises(OSError):
                migration.apply(manifest, self.root)
        self.assertTrue(all((self.root / i['source']).is_file() for i in manifest['moves']))
        self.assertFalse((self.root / '.local/client-path-map.json').exists())
        self.assertFalse((self.root / 'clients/a').exists())

    def test_verify_and_rollback_refuse_post_migration_edits(self):
        manifest = migration.plan(['a'], self.root)
        result = migration.apply(manifest, self.root)
        self.write(manifest['moves'][0]['destination'], 'new human edit')
        self.assertEqual(migration.verify(manifest, self.root)['status'], 'failed')
        with self.assertRaises(ValueError):
            migration.rollback(self.root / result['transaction'], self.root)
        self.assertEqual((self.root / manifest['moves'][0]['destination']).read_text(), 'new human edit')

    def test_rollback_does_not_erase_later_registry(self):
        manifest = migration.plan(['a'], self.root)
        result = migration.apply(manifest, self.root)
        registry_path = self.root / '.local/client-path-map.json'
        registry = json.loads(registry_path.read_text())
        registry['paths']['later.md'] = dict(destination='clients/b/later.md', sha256='later', client='b')
        registry_path.write_text(json.dumps(registry))
        with self.assertRaises(ValueError):
            migration.rollback(self.root / result['transaction'], self.root)
        self.assertIn('later.md', json.loads(registry_path.read_text())['paths'])

    def test_brief_keeps_partial_feedback_separate_from_score(self):
        legacy = brief('a', self.root)
        self.assertEqual(legacy['layout'], 'legacy')
        migration.apply(migration.plan(['a'], self.root), self.root)
        result = brief('a', self.root)
        self.assertEqual(result['layout'], 'client_folder')
        self.assertEqual(len(result['context']), 2)
        versions = result['campaigns'][0]['versions']
        self.assertIsNone(versions[0]['feedback'])
        self.assertEqual(versions[1]['feedback']['literal'], legacy['campaigns'][0]['versions'][1]['feedback']['literal'])
        self.assertEqual(result['campaigns'][0]['latest_version'], 'v2')
        self.assertNotIn('approved', result)
        with self.assertRaises(ValueError):
            brief('../b', self.root)

    def test_retrieval_resolves_alias_without_client_crossover(self):
        self.write('examples/curated/a-card.md', 'Anotação do cliente a')
        entry = dict(id='a-card', path='examples/curated/a-card.md', client='a', routes=['ads'],
                     status='active', use='negative', tags=['redundância'])
        self.write('examples/curated/index.json', json.dumps([entry]))
        migration.apply(migration.plan(['a'], self.root), self.root)
        result = retrieve('redundância', [entry], 'ads', 'a', root=self.root)
        self.assertEqual(result[0]['path'], 'clients/a/referencias/curadas/a-card.md')
        self.assertEqual(result[0]['excerpt'], 'Anotação do cliente a')
        self.assertEqual(retrieve('redundância', [entry], 'ads', 'b', root=self.root), [])
        forged = dict(entry, client='b')
        self.assertEqual(retrieve('redundância', [forged], 'ads', 'b', root=self.root), [])

    def test_client_without_profile_keeps_materials_without_invented_facts(self):
        self.write('outputs/drafts/c-lp-v1.md', 'Copy antiga sem aprovação')
        self.write('c-reuniao.txt', 'Feedback literal sobre a copy')
        manifest = migration.plan(['c'], self.root)
        result = migration.apply(manifest, self.root)
        self.assertEqual(result['status'], 'passed')
        state = (self.root / 'clients/c/CLIENTE.md').read_text()
        self.assertIn('Não havia ficha', state)
        self.assertEqual(resolve_reference('c-reuniao.txt', self.root).read_text(), 'Feedback literal sobre a copy')
        self.assertEqual(resolve_reference('outputs/drafts/c-lp-v1.md', self.root).read_text(), 'Copy antiga sem aprovação')
        with self.assertRaises(ValueError):
            migration.plan(['unknown'], self.root)

    def test_legacy_only_and_non_markdown_feedback_preserved(self):
        (self.root / 'clients/current/a.md').unlink()
        self.write('outputs/revised/a-feedback.json', '{"feedback":"reprovado"}')
        manifest = migration.plan(['a'], self.root)
        migration.apply(manifest, self.root)
        self.assertIn('Histórico original', (self.root / 'clients/a/CLIENTE.md').read_text())
        self.assertEqual(resolve_reference('outputs/revised/a-feedback.json', self.root).read_text(), '{"feedback":"reprovado"}')

    def test_explicit_folder_alias_and_supplement_do_not_rewrite_profiles(self):
        source = self.write('tmp/alias/source.txt', 'Fonte atribuída explicitamente')
        manifest = migration.plan(['a'], self.root, materials={'a':[dict(path='tmp/alias', area='fontes')]})
        migration.apply(manifest, self.root)
        self.assertEqual(resolve_reference('tmp/alias/source.txt', self.root).read_text(), 'Fonte atribuída explicitamente')
        before = (self.root / 'clients/a/CLIENTE.md').read_bytes()
        self.write('tmp/new/asset.png', 'asset bytes')
        supplement = migration.material_plan({'a':[dict(path='tmp/new', area='assets')]}, self.root)
        applied = migration.apply(supplement, self.root)
        self.assertEqual((self.root / 'clients/a/CLIENTE.md').read_bytes(), before)
        self.assertEqual(migration.verify(manifest, self.root)['status'], 'passed')
        migration.rollback(self.root / applied['transaction'], self.root)
        self.assertEqual((self.root / 'clients/a/CLIENTE.md').read_bytes(), before)
        self.assertEqual(migration.verify(manifest, self.root)['status'], 'passed')

    def test_supplement_requires_known_client_and_valid_area(self):
        self.write('tmp/asset.txt', 'Fonte')
        with self.assertRaises(ValueError):
            migration.material_plan({'unknown':[dict(path='tmp/asset.txt')]}, self.root)
        with self.assertRaises(ValueError):
            migration.plan(['a'], self.root, materials={'a':[dict(path='tmp/asset.txt', area='../b')]})


if __name__ == '__main__':
    unittest.main()
