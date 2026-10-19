"""Cache survives cwd/session changes; runtime never downloads missing weights."""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import rag_model
from rag_config import FASTEMBED_VERSION,MAX_TOKENS

class PersistentCache(unittest.TestCase):
    def test_default_is_project_relative_not_working_directory(self):
        previous=Path.cwd()
        with tempfile.TemporaryDirectory() as tmp,patch.dict(os.environ,{},clear=True):
            try:
                os.chdir(tmp)
                self.assertEqual(rag_model.resolve_cache_dir(),ROOT/'.local/fastembed-cache')
            finally:os.chdir(previous)

    def test_explicit_argument_overrides_environment(self):
        with tempfile.TemporaryDirectory() as tmp,patch.dict(os.environ,{'FASTEMBED_CACHE_PATH':str(Path(tmp)/'env')}):
            self.assertEqual(rag_model.resolve_cache_dir(Path(tmp)/'caller'),(Path(tmp)/'caller').resolve())

    def test_environment_override_and_empty_environment_default(self):
        with tempfile.TemporaryDirectory() as tmp,patch.dict(os.environ,{'FASTEMBED_CACHE_PATH':tmp}):
            self.assertEqual(rag_model.resolve_cache_dir(),Path(tmp).resolve())
        with patch.dict(os.environ,{'FASTEMBED_CACHE_PATH':''}):
            self.assertEqual(rag_model.resolve_cache_dir(),ROOT/'.local/fastembed-cache')

    def test_memory_cache_tracks_effective_path_and_keeps_runtime_offline(self):
        calls=[]
        def fake_embedding(**kwargs):
            calls.append(kwargs)
            return SimpleNamespace(model=SimpleNamespace(tokenizer=SimpleNamespace(truncation={'max_length':MAX_TOKENS})))
        fake=SimpleNamespace(__version__=FASTEMBED_VERSION,TextEmbedding=fake_embedding)
        with tempfile.TemporaryDirectory() as tmp,patch.dict(sys.modules,{'fastembed':fake}),patch.object(rag_model,'MODEL_CACHE',{}):
            first=Path(tmp)/'one';second=Path(tmp)/'two'
            with patch.dict(os.environ,{'FASTEMBED_CACHE_PATH':str(first)}):
                a=rag_model.load_model()
                self.assertIs(a,rag_model.load_model(first))
            with patch.dict(os.environ,{'FASTEMBED_CACHE_PATH':str(second)}):
                self.assertIsNot(a,rag_model.load_model())
        self.assertEqual(len(calls),2)
        self.assertTrue(all(x['local_files_only'] is True for x in calls))
        self.assertEqual([x['cache_dir'] for x in calls],[str(first.resolve()),str(second.resolve())])

if __name__=='__main__':unittest.main()
