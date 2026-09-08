import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
class ReadContext(unittest.TestCase):
    def test_prints_full_source_and_appends_phase_receipts(self):
        with tempfile.TemporaryDirectory() as tmp:
            receipts=Path(tmp)/'nested/readings.json'; path='knowledge/vicios-ia-humanizacao.md'
            for phase in ['production','review']:
                r=subprocess.run([sys.executable,str(ROOT/'scripts/read_context.py'),path,'--phase',phase,'--receipts',str(receipts)],capture_output=True,text=True)
                self.assertEqual(r.returncode,0); self.assertIn((ROOT/path).read_text(),r.stdout)
            records=json.loads(receipts.read_text()); self.assertEqual([r['phase'] for r in records],['production','review'])
            self.assertEqual(records[0]['sha256'],hashlib.sha256((ROOT/path).read_bytes()).hexdigest())
    def test_outside_source_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            receipts=Path(tmp)/'readings.json'; source=Path(tmp)/'outside.md'; source.write_text('Outside')
            r=subprocess.run([sys.executable,str(ROOT/'scripts/read_context.py'),str(source),'--phase','context','--receipts',str(receipts)],capture_output=True,text=True)
            self.assertNotEqual(r.returncode,0); self.assertFalse(receipts.exists())
if __name__=='__main__': unittest.main()
