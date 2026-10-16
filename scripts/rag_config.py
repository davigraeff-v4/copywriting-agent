"""Public-copy RAG configuration; no credentials, client paths or runtime secrets."""
MODEL='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
FASTEMBED_VERSION='0.8.0'
DIMENSION=384
MAX_TOKENS=128
TARGET_TOKENS=120
MAX_WORDS=180
OVERLAP_WORDS=8
LEXICAL_WORDS=65
SCHEMA_VERSION=2
INDEX_REL='.local/rag/index'
# Calibrated on development queries only; never interpreted as factual confidence.
SEMANTIC_FLOOR=0.48
RRF_K=40
LEXICAL_WEIGHT=1.0
SEMANTIC_WEIGHT=1.0
# Explicit selection, not recursive discovery. Navigation, prompt packs and baselines excluded.
EXTRA_KNOWLEDGE={
 'ajustes-incrementais':('Ajustes incrementais e preservação de escopo','ajuste localizado escopo revisão'),
 'banco-de-angulos':('Ângulos por decisão e situação','ângulo situação alternativa'),
 'banco-de-ctas':('CTAs por objetivo e compromisso','CTA ação compromisso'),
 'banco-de-ganchos':('Ganchos com objeto e informação','gancho atenção objeto'),
 'banco-de-headlines':('Headlines por intenção e consciência','headline consciência intenção'),
 'canais-por-modelo-de-negocio':('Canais por modelo de negócio','canal modelo franquia'),
 'erros-comuns':('Diagnóstico de erros de copy','erro genérico estratégia escrita'),
 'estrategia-de-marca':('Estratégia e voz de marca','marca posicionamento voz'),
 'exemplos-de-estruturas':('Estruturas históricas de formatos','formato campos arte plataforma'),
 'frameworks-copy':('Frameworks opcionais de organização','framework narrativa opcional'),
 'funil-e-jornada':('Funil, jornada e consciência','funil jornada consciência'),
 'gatilhos-psicologicos':('Influência com prova e escopo','gatilho influência escassez prova'),
 'matriz-de-variacoes-e-testes':('Variações e comparação de copy','variação teste hipótese'),
 'metodologia-thamy':('Metodologia e perguntas Thamy','metodologia briefing direção'),
 'narrativa-lp':('Tese, escada de títulos e compressão de LP','LP tese escada títulos progressão compressão'),
 'objecoes-e-mecanismos':('Objeções e mecanismo sustentado','objeção mecanismo causalidade'),
 'pacote-contexto':('Pacote factual e prontidão de contexto','contexto fonte voz restrição prontidão'),
 'pesquisa-voz-do-cliente':('Voz do cliente e pesquisa de decisões','pesquisa entrevista linguagem situação'),
 'processo-de-copy':('Pesquisa, estratégia e produção de copy','processo pesquisa ideação revisão'),
 'processo-kickoff-cliente':('Kickoff e manual de comunicação','kickoff manual marca'),
 'regras-por-canal':('Campos e funções por canal','formato canal vídeo carrossel'),
 'termos-a-evitar':('Termos fracos e promessas sem sustentação','termo genérico promessa português'),
 'use-case-map-exemplos':('Mapa de uso com exemplos históricos','mapa uso público alternativa valor'),
 'vicios-ia-humanizacao':('Humanização por trecho e ritmo','humanização cadência telegráfica voz'),
}
