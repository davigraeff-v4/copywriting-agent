# Base de Conhecimento — Índice e Roteamento

A base tem três níveis de autoridade:

1. **Fonte real Thamy/V4** — materiais importados do Drive; maior precedência metodológica.
2. **Referência de mercado** — sínteses de frameworks e boas práticas; apoio, nunca substitui a fonte real.
3. **Baseline operacional Copywriting Agent** — regras criadas para fechar lacunas do agent. Não devem ser apresentadas como padrão oficial da V4.

## Knowledge Gate e uso atual

- Início: ler índice, metodologia e rota aplicável (`rotas/lp.md`, `rotas/social.md`, `rotas/ads.md`, `rotas/direct.md`).
- Ler apenas referências pertinentes da skill; índice é mapa, não lista de carregamento obrigatório.
- Humanização: leitura integral independente antes de produção e revisão; recibos via `scripts/read_context.py`.
- Precedência operacional: instrução atual explícita → restrições ativas/política → estado atual do cliente → metodologia aplicável → referência histórica compatível. Fato depende de fonte, não desta ordem editorial.
- Material histórico: consultar `calibracao-editorial.md` antes de usar. Origem real não torna toda frase um modelo positivo.

## Núcleo operacional v2

| Arquivo | Uso |
|---|---|
| `politica-editorial.md` | Português e padrão de expressão |
| `pacote-contexto.md` | Pesquisa convertida em matéria-prima e claims |
| `rotas/lp.md` | Argumentação por dúvida do comprador |
| `rotas/social.md` | Pauta, viabilidade e conjunto editorial |
| `rotas/ads.md` | Anúncios, arte e campos da plataforma |
| `rotas/direct.md` | E-mail/WhatsApp |
| `memoria-clientes.md` | Estado vigente separado do histórico |
| `calibracao-editorial.md` | Compatibilidade dos exemplos e pares anotados |
| `recuperacao-contexto.md` | Busca lexical com escopo e metadados |
| `ajustes-incrementais.md` | Interpretação e revisão rápida de versão existente |

## Camada 1 — Fonte real Thamy/V4

| Arquivo | Conteúdo | Skills principais |
|---|---|---|
| `metodologia-thamy.md` | 4 etapas, 11 perguntas, matriz funil×framework×gatilho×CTA, revisão e exemplo Gotter | todas |
| `processo-kickoff-cliente.md` | Kickoff, análise de ambientes e Manual de Comunicação | `03`, `04` |
| `canais-por-modelo-de-negocio.md` | Canais por modelo e caso de franquias | `03`, `12` |
| `use-case-map-exemplos.md` | Persona→problema→alternativas→valor, com exemplos reais | `05`, `09` |
| `exemplos-de-estruturas.md` | Templates reais Meta Ads/LP, concorrência e público | `05`, `07`, `11`, `12` |
| `quality/analise-semanal-comunicacao.md` | Revisão retrospectiva de campanha publicada | `04`, governança |

## Camada 2 — Referências de mercado

| Arquivo | Conteúdo | Skills principais |
|---|---|---|
| `processo-de-copy.md` | Processo de pesquisa→ideação→escrita→edição | `08`, `11` |
| `frameworks-copy.md` | AIDA, PAS, BAB, PASTOR, QUEST e storytelling | `10`, `11` |
| `gatilhos-psicologicos.md` | Gatilhos, framing e preço | `10` |
| `banco-de-ganchos.md` | Aberturas por categoria | `11` |
| `banco-de-ctas.md` | CTAs por intenção | `10`, `12` |
| `regras-por-canal.md` | Princípios por Google, Meta, e-mail, LP, LinkedIn, vídeo e SEO | `12` |
| `estrategia-de-marca.md` | Fundamento, posicionamento, voz e expressão | `03` |
| `funil-e-jornada.md` | Consciência, funil e jornada não linear | `06` |
| `prompts-de-apoio.md` | Estruturação de clarificações e pedidos | uso interno |
| `vicios-ia-humanizacao.md` | 12 vícios + 8 dimensões do score de humanização | `11`, `13`, gate na `14` |

## Camada 3 — Baseline operacional Copywriting Agent

| Arquivo | Conteúdo | Skills principais |
|---|---|---|
| `padroes-copy-v4.md` | Baseline de qualidade, tom, formatação e compliance leve; ainda aguarda validação oficial V4 | `03`, `11`, `13` |
| `banco-de-angulos.md` | Taxonomia de ângulos, seleção e registro de aprendizado | `08`, `10` |
| `banco-de-headlines.md` | Estruturas por função, consciência e calibração | `11`, `13` |
| `erros-comuns.md` | Diagnóstico/correção por estratégia, escrita, canal e processo | `11`, `13` |
| `termos-a-evitar.md` | Claims proibidos, expressões fracas e termos condicionais | `11`, `13` |
| `pesquisa-voz-do-cliente.md` | Hierarquia de fontes, etiquetas de evidência e extração de linguagem | `03`, `05`, `07` |
| `provas-e-claims.md` | Tipos de claim, escada de prova e gate de sustentação | `07`, `09`, `11`, `13` |
| `objecoes-e-mecanismos.md` | Objeções raiz, mecanismo e resposta proporcional | `05`, `09`, `10` |
| `matriz-de-variacoes-e-testes.md` | Variações por hipótese, controle e registro de aprendizado | `08`, `11`, `12`, `14` |

## Roteamento por etapa

O núcleo obrigatório da campanha é o da seção Knowledge Gate. A tabela abaixo sugere referências; não impõe releitura de todos os arquivos por etapa nem substitui os Dados necessários da skill.

| Etapa | Referências conforme necessidade da skill | Complemento quando aplicável |
|---|---|---|
| Marca | `processo-kickoff-cliente.md`, `estrategia-de-marca.md` | `padroes-copy-v4.md`, `pesquisa-voz-do-cliente.md` |
| Público | `metodologia-thamy.md`, `use-case-map-exemplos.md` | `pesquisa-voz-do-cliente.md`, `objecoes-e-mecanismos.md` |
| Funil | `funil-e-jornada.md`, matriz de `metodologia-thamy.md` | `frameworks-copy.md` |
| Referências | `exemplos-de-estruturas.md` | `pesquisa-voz-do-cliente.md`, `provas-e-claims.md` |
| Big idea | `banco-de-angulos.md`, `processo-de-copy.md` | `matriz-de-variacoes-e-testes.md` |
| Oferta | `use-case-map-exemplos.md`, `provas-e-claims.md` | `objecoes-e-mecanismos.md` |
| Produção | `metodologia-thamy.md`, `vicios-ia-humanizacao.md` | headlines, ganchos, termos, variações |
| Adaptação | `regras-por-canal.md`, `exemplos-de-estruturas.md` | `matriz-de-variacoes-e-testes.md` |
| Revisão | `quality/scorecard.md`, `vicios-ia-humanizacao.md` | claims, erros, termos, headlines |

## Regras de evidência

- Não transformar síntese em citação literal.
- Não usar dado de mercado sem fonte rastreável como verdade universal.
- Não confundir aprovação subjetiva com performance.
- Não chamar baseline operacional de material real da Thamy/V4.
- Limites técnicos de plataformas devem ser verificados quando forem decisivos para a entrega.

## Manutenção

Ao incorporar novo material:

1. Registrar origem e nível de autoridade.
2. Indicar skills consumidoras.
3. Remover duplicação ou criar referência cruzada.
4. Separar exemplo real, exemplo didático e hipótese.
5. Atualizar este índice e o `SKILL.md` consumidor.
6. Para feedback real, registrar contexto e limite de reutilização.

## Referência visual

`BASE DE CONHECIMENTO/Pinterest - Copywriting Techniques/` mantém o swipe file visual. Usar para composição e hierarquia, não como prova de eficácia.

## Materiais externos ainda não incorporados

Calendários e materiais operacionais podem ser fontes da rota social: selecionar pautas, disponibilidade de assets e decisões atuais. Não importar tudo indiscriminadamente.
