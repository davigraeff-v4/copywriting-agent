# THAMY IA

Agent de copywriting estratégico inspirado no método de trabalho da Thamy, copywriter da V4. Transforma um briefing de campanha em copy final pronta para uso — com variações, explicação estratégica, orientação para design/tráfego e revisão crítica.

## Como usar

1. Abra esta pasta no **Claude Code** ou no **Codex**.
2. Cole o briefing completo da campanha no chat (ou diga qual cliente/copy você quer trabalhar).
3. Digite `/copy-final` — ou simplesmente cole o briefing, a THAMY IA já aciona o fluxo sozinha.
4. A THAMY IA vai diagnosticar o briefing, perguntar o que faltar de crítico, produzir a copy, adaptar por canal e revisar com scorecard antes de entregar.
5. Aprove, reprove ou peça ajuste quando ela perguntar.
6. Quando aprovado, o output fica salvo automaticamente em `outputs/approved/` e um exemplo em `examples/approved/`.

### Modos de operação (quantas vezes a THAMY IA vai te interromper)

- **Rápido (padrão)** — até 3 validações no total: diagnóstico do briefing, mapa estratégico (marca, público, ideia, framework) e entrega final. Use no dia a dia, sem precisar digitar nada extra.
- **Express** — 2 validações no total. Só disponível quando o cliente já tem ficha completa em `clients/` (marca, público e restrições conhecidos) e a demanda é parecida com campanha anterior. Peça com `/copy-final --express`.
- **Estratégico** — uma validação a cada etapa da metodologia (até 14 no total). Use quando quiser acompanhar/construir passo a passo — cliente novo e complexo, reposicionamento de marca, campanha institucional grande, ou qualquer oferta que você prefira validar com calma. Peça com `/copy-final --estrategico`.

Se você não pedir nenhum modo, a THAMY IA decide sozinha (regra em `CLAUDE.md`) e avisa qual escolheu logo no início. Em qualquer modo, ela sempre para e pergunta se faltar informação crítica (cliente, oferta, canal, restrições) ou se detectar uma promessa arriscada — isso nunca é pulado, independente do modo.

## Estrutura

```
CLAUDE.md                        → instruções para Claude Code
AGENTS.md                        → instruções equivalentes para Codex
CONTRATO-OPERACIONAL-MODOS.md    → definição dos 3 modos, checkpoints, hard constraints e padrões de canal/formato
briefings/                       → template e exemplos de briefing
knowledge/                       → base de conhecimento (metodologia, frameworks, exemplos) — preencher com materiais reais
clients/                         → ficha operacional por cliente (memória entre conversas)
skills/                          → as 14 skills da THAMY IA, uma pasta por skill
examples/                        → copies aprovadas/reprovadas, comparativos, por canal/segmento
outputs/                         → rascunhos, aprovados e revisados
quality/                         → scorecard e critérios de revisão
.claude/commands/                → atalhos nativos (/copy-final, /revisar-copy, /aprovar-copy, /reprovar-copy) no Claude Code
```

## Base de conhecimento — o que já está pronto e o que falta

`knowledge/README.md` indexa tudo. Três camadas:

- **Real, da Thamy/V4** (importada do Google Drive): `metodologia-thamy.md` (o documento-cérebro dela — o mais importante de todo o sistema), `processo-kickoff-cliente.md`, `canais-por-modelo-de-negocio.md`, `use-case-map-exemplos.md`, `exemplos-de-estruturas.md` (templates reais de Meta Ads/LP + exemplos preenchidos) e `quality/analise-semanal-comunicacao.md`. Esta camada tem prioridade sobre as demais.
- **Genérica de mercado** (convertida do swipe file de ~130 pins do Pinterest, deduplicada): `processo-de-copy.md`, `frameworks-copy.md`, `gatilhos-psicologicos.md`, `banco-de-ganchos.md`, `banco-de-ctas.md`, `regras-por-canal.md`, `estrategia-de-marca.md`, `funil-e-jornada.md`, `prompts-de-apoio.md`.
- **Ainda placeholder**: `padroes-copy-v4.md`, `banco-de-angulos.md`, `banco-de-headlines.md`, `erros-comuns.md`, `termos-a-evitar.md`.

A THAMY IA já opera com metodologia real da Thamy para a maior parte do fluxo — os placeholders restantes cobrem casos mais específicos (tom institucional fixo, bancos maiores de ângulos/headlines aprovados, erros recorrentes documentados).

A pasta `BASE DE CONHECIMENTO/Pinterest - Copywriting Techniques/` mantém as imagens originais (swipe file visual) usadas pela skill `07-reference-competitor-analysis` — o conteúdo textual delas já foi extraído para `knowledge/`.

## MVP — o que está dentro e fora do escopo

**Dentro:** briefing colado no chat, diagnóstico, metodologia da Thamy, geração de copy final por canal, variações, explicação estratégica, revisão com scorecard, feedback e memória por cliente em Markdown.

**Fora (por enquanto):** interface visual própria, banco de dados, RAG vetorial, integração automática com Drive, automação (Make/N8N), dashboard de performance, múltiplos agents especializados.

Ver `PRD - THAMY IA.md` para o detalhamento completo e `GUIA-REPLICAR-ESTRUTURA-AGENT-IA.md` para o padrão arquitetural de referência.
