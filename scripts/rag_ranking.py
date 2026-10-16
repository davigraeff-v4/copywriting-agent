"""Query-time calibration. No source edits, client reads, or hidden corpus exclusions."""
from rag_corpus import tokens
EN_STOP=set('the a an and or of to in on for with by as at from into that this these those is are was were be been being have has had do does did should would could can will may might not but than then there their its it you your our us we they them which what why how when where who whom all any each every more most very only also about over under so such own need must through before after between per while whose both some no'.split())
SEMANTIC_DOCUMENT_FLOOR=.49
SEMANTIC_CANDIDATE_FLOOR=.25
BODY_BLEND_CURATED=.8
BODY_BLEND_ORIGINAL=.5
META_WEIGHT=.25
RRF_DOCUMENT_K=8
RRF_PASSAGE_K=8
SEMANTIC_WEIGHT_CURATED=.6
SEMANTIC_WEIGHT_ORIGINAL=1.25
ROUTE_PRIOR=1.12
TRACEABLE_ORIGINAL_PRIOR=1.08
RANKING_VERSION=1

def rank_tokens(text):
    out=[]
    for word in tokens(text):
        if word in EN_STOP:continue
        if word=='salesmen':word='salesman'
        elif len(word)>5 and word.endswith('ies'):word=word[:-3]+'y'
        elif len(word)>4 and word.endswith('s') and not word.endswith(('ss','us','is')):word=word[:-1]
        out.append(word)
    return out

def metadata_intent(query):return bool(set(tokens(query))&{'sha256','hash','url','urls','proveniencia','licenca','license','catalogo','manifesto','metadados','copyright'})

def metadata_penalty(doc,chunk,query):
    if metadata_intent(query):return 0.0
    if doc['path'].endswith('.json'):return .22
    if chunk['section'].casefold()=='proveniência':return .15
    return 0.0

def relevance_prior(doc,route):
    prior=ROUTE_PRIOR if doc.get('primary_route')==route or doc['routes']==[route] else 1.0
    if doc.get('use')=='original' and doc.get('authority')=='historical_original' and doc.get('source_urls'):prior*=TRACEABLE_ORIGINAL_PRIOR
    return prior

def section_key(chunk):
    # A chapter can span many pages. Other sources retain their own section key.
    return ('chapter',chunk['chapter_number']) if chunk.get('chapter_number') else ('parent',chunk['parent_id'])
