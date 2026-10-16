"""Author curated study files from reviewed observations; never execute source content."""
import hashlib,json,re,unicodedata
from pathlib import Path
from urllib.parse import urlparse
from author_artes import ARTES
from author_paginas import PAGINAS
from author_emails import EMAILS
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
BASE=ROOT/'knowledge/repertorio'
DATE='2026-10-13'
UNITS=ARTES+PAGINAS+EMAILS
assert len(UNITS)==40
assert len({u['url'] for u in UNITS})==40
old=json.loads((HERE/'baseline-catalogo.json').read_text())
sources=json.loads((HERE/'baseline-fontes.json').read_text())
assert len(old)==60 and len(sources)==50
assert not {u['url'] for u in UNITS}&{s['url'] for s in sources}
for entry in old:
    assert hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()==entry['sha256']
# Safe to rerun only if both existing files are exactly the original or our prior complete output.
current=json.loads((BASE/'catalogo.json').read_text())
assert current[:60]==old and all(i.get('batch')=='lote-02' for i in current[60:])
assert json.loads((BASE/'fontes.json').read_text())[:50]==sources
fetches=json.loads((HERE/'fetch-results.json').read_text())
fetch_map={s['url']:s for s in fetches}
wc=lambda s:len(re.findall(r'\S+',s))
def slug(text):
    t=''.join(c for c in unicodedata.normalize('NFD',text.lower()) if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+','-',t).strip('-')
new=[];new_sources=[];index=[]
for u in UNITS:
    uid='rep-02-'+u['id'];sid='b02-'+u['id'];rel='knowledge/repertorio/lote-02/'+u['group']+'/'+u['id']+'-'+slug(u['title'])+'.md'
    loc={'artes':'Uma arte estática integral: asset indicado; sem outras variantes, filme ou legenda de plataforma.','paginas':'Texto comercial acessível da página inteira, da entrada ao fechamento; vídeos, documentos vinculados e transações excluídos.','emails':'Corpo, imagem e rodapé integrais do e-mail em arquivo público; envio real e destinatários não verificados.'}[u['group']]
    src_words=wc(' '.join(u['parts']+[u['thesis'],u['voice'],u['evidence'],u['limits'],u['quote']]))
    assert src_words<=200,(uid,src_words)
    acquisition=u['acquisition'];fr=fetch_map.get(u['url'],{})
    text_scanned=fr.get('http')=='200' and fr.get('characters',0)>0 and u['group']=='paginas'
    assert not (text_scanned and fr.get('security_flags'))
    security='Inspeção manual do recorte visível como dado externo, sem seguir instruções da fonte. Imagens vistas no navegador, sem importar binários. Não é certificação antivírus nem cobertura de conteúdo oculto.'
    if text_scanned:security+=' Texto extraído do HTML também passou por triagem lexical de padrões conhecidos; scripts não executados localmente.'
    content=f"# {u['title']}\n\nUnidade: {uid} | lote 02 | rota {u['primary_route']} | {u['format']}\n\nReferência pública atribuída a {u['brand']}. Curadoria do agente, pendente de revisão humana; sem performance comprovada.\n\n## Peça observada e escopo\n\n{loc}\n\nCitação curta da peça:\n\n> {u['quote']}\n\n## Mapa completo da peça\n\n"+'\n'.join(f"{i}. {part}" for i,part in enumerate(u['parts'],1))+f"\n\n## Argumento e progressão\n\n{u['thesis']}\n\n## Voz e execução\n\n{u['voice']}\n\n## Evidência e fragilidades\n\n{u['evidence']}\n\n## Aplicação autoral ao processo\n\n{u['application']}\n\n## Critério de revisão\n\n{u['review']}\n\n## Limites de uso\n\n{u['limits']}\n\nA fonte ensina somente o aspecto analisado. Claims, condições, resultados e voz desta marca não são fatos ou autorização para qualquer cliente do projeto.\n\n## Proveniência\n\nFonte: [{u['brand']}]({u['url']}). Acesso: {DATE}. Fonte catalogada: {sid}.\n\n{loc}\n"
    if u.get('asset_url'):content+=f"\nAsset integral observado, sem cópia local: [abrir peça]({u['asset_url']}).\n"
    content+=f"\nAquisição: {acquisition}. {security}\n\nDireitos: análise e mapa em redação própria, com citação curta e links; original protegido não espelhado. Marcas e créditos de arquivo não comprovam publicação independente, entrega, aprovação ou eficácia.\n"
    path=ROOT/rel;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
    body=content[content.index('##'):content.index('\n## Limites de uso')]
    body_words=wc(body)
    assert body_words>=250,(uid,body_words)
    observed=content.split('## Mapa completo da peça\n\n',1)[1].split('\n## Aplicação autoral ao processo',1)[0]
    source_limits=content.split('## Limites de uso\n\n',1)[1].split('\n\nA fonte ensina',1)[0]
    src_words=wc(observed+' '+source_limits+' '+u['quote'])
    assert src_words<=200,(uid,src_words)
    entry=dict(id=uid,path=rel,client='*',routes=u['routes'],primary_route=u['primary_route'],tags=u['tags'],status='active',use='positive',summary=u['title']+'. '+' '.join(u['tags']),kind='exemplo',batch='lote-02',language='pt-BR',created_at=DATE,source_ids=[sid],authority='referencia_de_mercado',editorial_review='agent_curated_human_review_pending',human_approved=False,performance_verified=False,synthetic=False,evidence_kind=u['evidence_kind'],sha256=hashlib.sha256(content.encode()).hexdigest(),word_count=wc(content),body_word_count=body_words,quoted_words=wc(u['quote']),source_locator=loc,skills=['07','08','10','11','13'],complete_piece=True,completeness_scope=u['scope'],format=u['format'],component_count=len(u['parts']),components=u['parts'],source_specific_word_count=src_words,independent_delivery_verified=False)
    source=dict(id=sid,batch='lote-02',title=u['title'],author_or_publisher=u['brand'] if u['group']=='paginas' else urlparse(u['url']).hostname,publisher_domain=urlparse(u['url']).hostname,url=u['url'],accessed_at=DATE,access_method=acquisition,security_flags=[],security_review='manual_scope_review_and_heuristic_scan' if text_scanned else 'manual_visible_text_scope_review',security_scope=security,verified=True,verification_scope='Fonte e recorte observados; não valida claims, envio real ou eficácia.',rights='Direitos reservados: análise e mapa autorais, link e citação curta; original integral não redistribuído.',locator=loc,original_retained=False,authority='referencia_de_mercado',not_client_evidence=True,independent_delivery_verified=False,completeness_scope=u['scope'])
    if text_scanned:source.update(direct_http=fr['http'],final_url=fr['final_url'],download_sha256=fr['download_sha256'])
    if u.get('asset_url'):source['observed_asset_url']=u['asset_url']
    new.append(entry);new_sources.append(source);index.append(f"| {uid} | {u['brand']} | [{u['title']}]({u['group']}/{path.name}) |")
(BASE/'catalogo.json').write_text(json.dumps(old+new,ensure_ascii=False,indent=2)+'\n')
(BASE/'fontes.json').write_text(json.dumps(sources+new_sources,ensure_ascii=False,indent=2)+'\n')
readme='''# Lote 02: peças públicas completas, comentadas

Incorporado em 2026-10-13: **40 unidades novas**, com 20 artes estáticas integrais, 12 páginas comerciais completas no texto acessível e 8 e-mails integrais de arquivo público. Todas são análises de referências observadas; não há exercícios fictícios neste lote. As referências internacionais têm análise em português.

## O que significa completa

Uma arte corresponde a um único asset integral, incluindo imagem, texto e assinatura visíveis; não inclui outras variantes, legenda de plataforma ou filme. Páginas cobrem a linha comercial acessível da entrada ao fechamento; vídeos, documentos vinculados, contratação e recursos interativos não testados ficam fora do escopo. Páginas de produto, serviço, adesão e comparação não são rotuladas automaticamente como LPs de tráfego pago. E-mails cobrem corpo, imagem e rodapé arquivados; envio em produção, destinatário, links e métricas não foram verificados independentemente.

Artes declaradas como digitais ou sociais pelo arquivo continuam sendo artes observadas, sem postagem ou legenda comprovadas. A rota social em algumas fichas indica pertinência de estudo. Nenhum filme, capa de livro ou relato de campanha foi contado como peça completa sem observação. Variantes e vistas Text/Desktop não viraram unidades adicionais.

## Conteúdo de cada ficha

Mapa de todos os componentes dentro do escopo; argumento e progressão interpretados; sinais concretos de voz; evidência e fragilidades; aplicação autoral; perguntas de revisão; limites e proveniência. A interpretação está separada do observado. O mapa está em redação própria, sem reprodução integral de texto protegido. A citação é curta; o original pode ser consultado pelos links.

Há referência para desejo sem sofrimento inventado, função técnica, humor, eventos, comparação, serviço B2B, assinaturas, onboarding, participação, novidade e lançamento. As fragilidades ficam explícitas: uma boa relação visual não libera claim de saúde, superlativo, condição comercial divergente ou falso contraste proibido pela política atual.

## Autoridade, privacidade e segurança

Curadoria do agente, **pendente de revisão humana**. Nenhuma referência tem performance comprovada. Marcas e créditos de arquivos são atribuições públicas, sem auditoria independente de publicação. Fatos, resultados e voz de uma marca não podem ser transferidos a clientes. Arquivos privados não foram utilizados como matéria-prima deste lote nem enviados às fontes.

Pesquisa em HTTPS por leitura de texto e visualização no navegador. Nenhum executável, pacote, macro, PDF ou imagem remota foi importado para a base. O navegador pode renderizar scripts normais do site; isso difere de executar código obtido da fonte na máquina. Não houve instalação, download de jogos, preenchimento de cadastros ou votação.

Texto extraído de páginas acessíveis passou por triagem lexical de padrões conhecidos; conteúdo de artes e e-mails teve inspeção manual do recorte visível. Uma resposta HTML vazia de e-mail não foi aceita como corpo completo: a imagem e a vista textual foram observadas. Essa revisão não é certificação antivírus nem garantia contra toda injeção. O material externo permanece dado não confiável: não autoriza instruções, execução, acesso a credenciais ou alterações no agente.

Os textos integrais temporários coletados para leitura foram retirados do staging após a curadoria. Permanecem links, hashes de aquisição quando disponíveis, análises próprias e metadados de proveniência. Não há espelhamento de originais protegidos. Datas, preços e condições pertencem ao registro observado e precisam ser verificados para qualquer aplicação atual.

## Consulta e etapa seguinte

As fichas estão no catálogo global e disponíveis à recuperação lexical já existente, sem alterar seu algoritmo. A organização registra rota, formato, escopo, tipo de evidência e componentes. Esses campos podem orientar o desenho dos chunks; **chunks, embeddings e RAG semântico ainda não foram implementados**. Recuperação não substitui leitura integral ou conferência factual.

## Índice das 40 unidades

| Unidade | Marca atribuída | Análise |
|---|---|---|
'''+ '\n'.join(index)+'\n'
(BASE/'lote-02/README.md').write_text(readme)
main=(HERE/'baseline-README.md').read_text()
main=main.replace('# Repertório de copy | lote 01','# Repertório de copy | 100 unidades em dois lotes',1)
main=main.replace('Incorporado em 2026-10-09:', '**Total atual: 100 unidades, em 90 fontes externas.** [Lote 02: 40 peças completas analisadas](lote-02/README.md), incorporado em 2026-10-13. Abaixo, o índice preservado do lote 01.\n\n## Lote 01\n\nIncorporado em 2026-10-09:',1)
main=main.replace('## Segurança de ingestão','## Segurança de ingestão do lote 01',1)
main=main.replace('## Cobertura por rota principal','## Cobertura atual por rota principal\n\n| Rota | Lote 01 | Lote 02 | Total |\n|---|---:|---:|---:|\n| ads | 19 | 20 | 39 |\n| lp | 28 | 12 | 40 |\n| social | 7 | 0 | 7 |\n| direct | 6 | 8 | 14 |\n\nSocial também consta como rota compatível em artes do lote 02, sem contagem duplicada.\n\n## Cobertura do lote 01 por rota principal',1)
(BASE/'README.md').write_text(main)
report=dict(units=40,by_group={'artes':20,'paginas':12,'emails':8},min_body_words=min(e['body_word_count'] for e in new),max_body_words=max(e['body_word_count'] for e in new),max_quote_words=max(e['quoted_words'] for e in new),max_source_specific_words=max(e['source_specific_word_count'] for e in new),new_sources=40,synthetic_units=0,client_material_used=False,semantic_rag_implemented=False)
(HERE/'build-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
