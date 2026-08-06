# Copywriting Agent

Agent de copywriting estratégico inspirado no método de trabalho da Thamy, copywriter da V4. Transforma um briefing de campanha em copy final pronta para uso — com variações, explicação estratégica, orientação para design/tráfego e revisão crítica.

Feito para **gestores de projeto**, não só para copywriters: você cola o briefing (ou até um texto solto, sem formatação) e o agent conduz o raciocínio inteiro — diagnóstico, marca, público, big idea, framework, produção, adaptação por canal e revisão — perguntando só o que for realmente crítico.

## Requisitos

- **Claude Code** (`CLAUDE.md` + `.claude/commands/`) ou **Codex** (`AGENTS.md`) instalado e configurado.
- Nenhuma dependência externa, banco de dados ou build — o agent roda inteiramente sobre os arquivos Markdown deste repositório.

## Instalação

```bash
git clone https://github.com/davigraeff-v4/thamy-ia.git
cd thamy-ia
```

Abra a pasta no Claude Code, no Codex, ou no VS Code (com a extensão do Claude Code). Não há passo de build/instalação — o agent lê `CLAUDE.md`/`AGENTS.md` automaticamente ao abrir a pasta.

## Como usar — primeiro contato

1. Cole o briefing completo da campanha no chat (ou diga qual cliente/copy você quer trabalhar).
2. Digite `/copy-final` — ou simplesmente cole o briefing, o agent já aciona o fluxo sozinho.
3. O Copywriting Agent vai diagnosticar o briefing, perguntar o que faltar de crítico (nunca mais que o necessário), produzir a copy, adaptar por canal e revisar com scorecard antes de entregar.
4. Aprove, reprove ou peça ajuste quando ela perguntar.
5. Quando aprovado, o output fica salvo automaticamente em `outputs/approved/` e um exemplo em `examples/approved/`; a ficha do cliente em `clients/{cliente}.md` é criada/atualizada com o que foi aprendido.

### Exemplo rápido do que esperar

```
Você: [cola um briefing de campanha de Reels para um cliente novo]

Copywriting Agent: Sem indicação sua, vou seguir no modo Rápido — até 3 checkpoints.

  Checkpoint 1 — Diagnóstico, fontes e restrições
  [...briefing organizado, lacunas críticas, se houver...]

Você: [responde o que faltou]

Copywriting Agent: Checkpoint 2 — Mapa estratégico consolidado
  [...marca, público, big idea, framework, HARD CONSTRAINTS...]
  Posso produzir com essa direção?

Você: sim

Copywriting Agent: Checkpoint 3 — Entrega revisada
  [...copy final adaptada ao canal, variações, score, justificativa...]
  A copy foi aprovada, reprovada ou precisa de ajuste?

Você: aprovada

Copywriting Agent: Salvo em outputs/approved/... e clients/{cliente}.md atualizado.
```

## Modos de operação (quantas vezes o Copywriting Agent vai te interromper)

- **Rápido (padrão)** — até 3 validações no total: diagnóstico do briefing, mapa estratégico (marca, público, ideia, framework) e entrega final. Use no dia a dia, sem precisar digitar nada extra.
- **Express** — 2 validações no total. Só disponível quando o cliente já tem ficha completa em `clients/` (marca, público e restrições conhecidos) e a demanda é parecida com campanha anterior. Peça com `/copy-final --express`.
- **Estratégico** — uma validação a cada etapa da metodologia (até 14 no total). Use quando quiser acompanhar/construir passo a passo — cliente novo e complexo, reposicionamento de marca, campanha institucional grande, ou qualquer oferta que você prefira validar com calma. Peça com `/copy-final --estrategico`.

Se você não pedir nenhum modo, o Copywriting Agent decide sozinho (regra em `CLAUDE.md`) e avisa qual escolheu logo no início. Em qualquer modo, ele sempre para e pergunta se faltar informação crítica (cliente, oferta, canal, restrições) ou se detectar uma promessa arriscada — isso nunca é pulado, independente do modo. Ver `CONTRATO-OPERACIONAL-MODOS.md` para a definição completa (matriz de campos, checkpoints, hard constraints, padrões de canal/formato).

## Comandos disponíveis

Nativos no Claude Code (`.claude/commands/`) — no Codex, os mesmos comandos funcionam como convenção de texto (basta digitar no chat):

| Comando | O que faz |
|---|---|
| `/copy-final` | Roda o fluxo completo a partir do briefing colado, no modo Rápido por padrão. Aceita `--rapido`, `--express`, `--estrategico`. |
| `/revisar-copy` | Roda o Score Geral (12 critérios) e o Score de Humanização/Anti-Vícios de IA sobre uma copy existente, mesmo que ela não tenha passado pelo fluxo completo. |
| `/aprovar-copy` | Valida os dois scores da versão atual e, só então, registra a aprovação (ficha do cliente + `outputs/approved/` + `examples/approved/`). |
| `/reprovar-copy` | Registra reprovação, perguntando o motivo, e salva em `examples/rejected/`. |

Comandos secundários por canal (`/copy-criativo`, `/copy-carrossel`, `/copy-meta`, `/copy-google`, `/copy-lp`, `/copy-whatsapp`, `/copy-email`, `/copy-video`) equivalem a `/copy-final` já fixando o canal/formato, pulando essa pergunta — são convenções de texto, não têm arquivo próprio em `.claude/commands/`.

## Memória por cliente

Toda vez que uma campanha é trabalhada, o Copywriting Agent cria ou atualiza `clients/{cliente}.md` com marca, tom de voz, público, promessas permitidas/proibidas, preferências de processo e aprendizados — inclusive coisas que só aparecem durante a conversa (ex.: "esse cliente não gosta de silêncio no início dos vídeos", "nunca citar X verbalmente"). Da próxima vez que você trabalhar com o mesmo cliente, o agent já lê essa ficha antes de perguntar qualquer coisa — é o que permite usar o modo Express e não repetir a mesma pergunta duas vezes.

Use `clients/cliente-template.md` como referência dos campos — mas normalmente você não precisa preencher isso manualmente, o agent faz isso sozinho ao longo do fluxo (skill `04-client-memory-builder`).

> Fichas reais de cliente, outputs e exemplos de campanha ficam fora do controle de versão (ver `.gitignore`) — o repositório público não expõe dados de clientes reais trabalhados localmente.

## Estrutura

```
CLAUDE.md                        → instruções para Claude Code
AGENTS.md                        → instruções equivalentes para Codex
CONTRATO-OPERACIONAL-MODOS.md    → definição dos 3 modos, checkpoints, hard constraints e padrões de canal/formato
briefings/                       → template e exemplos de briefing
knowledge/                       → base de conhecimento (metodologia, frameworks, exemplos) — preencher com materiais reais
clients/                         → ficha operacional por cliente (memória entre conversas) — apenas o template é versionado
skills/                          → as 14 skills do Copywriting Agent, uma pasta por skill
examples/                        → copies aprovadas/reprovadas, comparativos, por canal/segmento — não versionado
outputs/                         → rascunhos, aprovados e revisados — não versionado
quality/                         → scorecard e critérios de revisão
.claude/commands/                → atalhos nativos (/copy-final, /revisar-copy, /aprovar-copy, /reprovar-copy) no Claude Code
```

## Base de conhecimento — o que já está pronto e o que falta

`knowledge/README.md` indexa tudo. Três camadas:

O uso da base não é opcional: toda campanha/revisão começa pela leitura do índice e de `metodologia-thamy.md`; cada skill deve ler as fontes listadas em seus dados necessários. `vicios-ia-humanizacao.md` é lido integralmente duas vezes em momentos independentes — antes da escrita (skill `11`) e antes da revisão (skill `13`).

- **Real, da Thamy/V4** (importada do Google Drive): `metodologia-thamy.md` (o documento-cérebro dela — o mais importante de todo o sistema), `processo-kickoff-cliente.md`, `canais-por-modelo-de-negocio.md`, `use-case-map-exemplos.md`, `exemplos-de-estruturas.md` (templates reais de Meta Ads/LP + exemplos preenchidos) e `quality/analise-semanal-comunicacao.md`. Esta camada tem prioridade sobre as demais.
- **Genérica de mercado** (convertida do swipe file de ~130 pins do Pinterest, deduplicada): processo, frameworks, gatilhos, ganchos, CTAs, canais, marca, funil e humanização.
- **Baseline operacional Copywriting Agent**: padrões mínimos, banco de ângulos/headlines, erros, termos, pesquisa de voz do cliente, provas/claims, objeções/mecanismos e matriz de variações/testes. Essa camada fecha lacunas práticas sem se apresentar como padrão oficial da V4.

O Copywriting Agent já opera com metodologia real da Thamy para a maior parte do fluxo. A próxima evolução da base depende menos de teoria e mais de evidência real: headlines/ângulos aprovados ou reprovados, feedbacks da Thamy e resultados de campanhas com contexto.

A pasta `BASE DE CONHECIMENTO/Pinterest - Copywriting Techniques/` mantém as imagens originais (swipe file visual) usadas pela skill `07-reference-competitor-analysis` — o conteúdo textual delas já foi extraído para `knowledge/`.

## Scorecard de qualidade

Toda copy final passa por dois scores independentes em `quality/scorecard.md`: **Score Geral** (12 critérios de estratégia e execução) e **Score de Humanização/Anti-Vícios de IA** (8 dimensões de naturalidade, especificidade, ritmo e ausência de tiques artificiais). Ambos precisam atingir 8/10. Vício crítico, violação de `HARD CONSTRAINTS`, leitura obrigatória pendente ou alteração posterior da copy também reprovam a versão, mesmo com média alta.

## MVP — o que está dentro e fora do escopo

**Dentro:** briefing colado no chat, diagnóstico, metodologia da Thamy, geração de copy final por canal, variações, explicação estratégica, revisão com scorecard, feedback e memória por cliente em Markdown, 3 modos de operação (Rápido/Express/Estratégico).

**Fora (por enquanto):** interface visual própria, banco de dados, RAG vetorial, integração automática com Drive, automação (Make/N8N), dashboard de performance, múltiplos agents especializados.

Detalhamento completo do produto, arquitetura e histórico de decisões ficam em documentos internos (não incluídos neste repositório público).

## Licença

Repositório ainda sem licença definida — considere todos os direitos reservados até uma licença ser adicionada.
