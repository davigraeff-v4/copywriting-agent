import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from retrieve import retrieve

class Retrieval(unittest.TestCase):
    def test_filters_and_ranking(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            entries=[]
            for name,client,route,status,use in [('local','a','lp','active','positive'),('other','b','lp','active','positive'),('old','a','lp','superseded','positive'),('social','a','social','active','positive'),('negative','a','lp','active','negative'),('global','*','lp','active','guidance')]:
                (root/f'{name}.md').write_text('Conteúdo '+name)
                entries.append(dict(id=name,path=f'{name}.md',client=client,routes=[route],status=status,use=use,tags=['catálogo'],summary='Consulta'))
            r=retrieve('catalogo',entries,'lp','a',root=root)
            self.assertEqual({i['id'] for i in r},{'local','negative','global'})
            self.assertEqual([i['id'] for i in retrieve('catalogo',entries,'lp','a',use='positive',root=root)],['local'])
            self.assertEqual(retrieve('inexistente',entries,'lp','a',root=root),[])
            self.assertEqual(len(retrieve('catalogo',entries,'lp','a',limit=1,root=root)),1)

    def test_no_holdout_history_or_path_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); entries=[]
            for name in ['evals/secret.md','.local/secret.md','clients/history/secret.md']:
                p=root/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text('secret')
                entries.append(dict(id=name,path=name,client='a',routes=['lp'],status='active',use='positive',tags=['catálogo']))
            entries.append(dict(id='escape',path='../outside.md',client='a',routes=['lp'],status='active',use='positive',tags=['catálogo']))
            self.assertEqual(retrieve('catalogo',entries,'lp','a',root=root),[])

if __name__=='__main__': unittest.main()
