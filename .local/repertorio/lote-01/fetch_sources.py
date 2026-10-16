import concurrent.futures, hashlib, json, re, subprocess, tempfile
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.skip=0; self.lines=[]
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style','noscript','svg'): self.skip+=1
        if tag in ('p','h1','h2','h3','li','div','section','br'): self.lines.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script','style','noscript','svg'): self.skip=max(0,self.skip-1)
    def handle_data(self, data):
        if not self.skip: self.lines.append(data)

def fetch(row):
    sid,url=row
    with tempfile.TemporaryDirectory() as folder:
        dest=Path(folder)/'source'
        p=subprocess.run(['curl','--proto','=https','--proto-redir','=https','-L','--fail','--silent','--show-error','--max-time','40','--max-filesize','12000000','-A','Mozilla/5.0','-o',str(dest),'-w','%{http_code}\n%{url_effective}\n%{content_type}',url],capture_output=True,text=True)
        info=p.stdout.splitlines()
        result={'id':sid,'url':url,'accessed':'2026-10-09','http':info[0] if info else '', 'final_url': info[1] if len(info)>1 else '', 'content_type':info[2] if len(info)>2 else '', 'error':p.stderr if p.returncode else ''}
        if not p.returncode:
            raw=dest.read_bytes(); result['download_sha256']=hashlib.sha256(raw).hexdigest()
            if b'%PDF'==raw[:4]:
                result['requires_pdf_review']=True
            elif 'html' in result['content_type'] or 'text/plain' in result['content_type']:
                source=raw.decode('utf-8',errors='replace')
                parser=Text(); parser.feed(source)
                clean='\n'.join(re.sub(r'\s+',' ',l).strip() for l in ''.join(parser.lines).splitlines() if l.strip())
                result['characters']=len(clean)
                result['security_flags']=re.findall(r'(?i)(?:ignore (?:all |any )?(?:previous|prior) instructions|disregard (?:all |any )?instructions|reveal (?:your |the )?system prompt|<\|(?:system|im_start)\|>|execute this command)',clean)
                (HERE/'candidates'/f'{sid}.txt').write_text(clean,encoding='utf-8')
    return result

if __name__=='__main__':
    (HERE/'candidates').mkdir(exist_ok=True)
    sources=json.loads((HERE/'urls.json').read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        results=list(pool.map(fetch,sources))
    (HERE/'fetch-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
    for r in results: print(r['id'],r['http'],r.get('characters',0),r.get('security_flags',[]),r['error'][:110])
