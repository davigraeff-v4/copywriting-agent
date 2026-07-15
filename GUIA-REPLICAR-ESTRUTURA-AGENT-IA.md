# Guia Completo — Como Replicar a Estrutura de Agent IA com Skills

> Baseado na arquitetura do sistema EE Clientes V4 (V4 Company).  
> Use este guia para criar qualquer agent especializado — o exemplo concreto aqui é um **Agent de Copy**.

---

## Índice

1. [Conceito da Arquitetura](#1-conceito-da-arquitetura)
2. [As 5 Peças Obrigatórias](#2-as-5-peças-obrigatórias)
3. [Estrutura de Pastas para Replicar](#3-estrutura-de-pastas-para-replicar)
4. [Como Criar o CLAUDE.md (o cérebro)](#4-como-criar-o-claudemd-o-cérebro)
5. [Como Criar Agents](#5-como-criar-agents)
6. [Como Criar Skills](#6-como-criar-skills)
7. [Como Criar o schema.json](#7-como-criar-o-schemajson)
8. [Como Criar o dependency_graph.json](#8-como-criar-o-dependency_graphjson)
9. [Exemplo Completo — Agent de Copy](#9-exemplo-completo--agent-de-copy)
10. [Checklist de Criação](#10-checklist-de-criação)
11. [Dúvidas Frequentes](#11-dúvidas-frequentes)

---

## 1. Conceito da Arquitetura

O sistema funciona como um **workflow engine operado por linguagem natural**. O Claude Code lê arquivos de instrução (CLAUDE.md, SKILL.md, agents) e executa tarefas estruturadas com checkpoints, validação e output padronizado.

### Os 3 princípios que fazem funcionar

**Princípio 1 — Estado persistido em arquivo**  
Tudo que importa fica em JSON. O sistema nunca depende de memória de conversa — a qualquer momento você pode fechar e retomar porque o estado está no arquivo.

**Princípio 2 — Instrução como código**  
CLAUDE.md e SKILL.md são instruções precisas, não conversas. Funcionam como `if/else`, com regras explícitas de roteamento, checkpoints numerados e validação automática.

**Princípio 3 — JSON é a verdade, HTML é a visualização**  
Sempre gere o output estruturado primeiro. O template visual é consequência. Isso permite reprocessar, exportar para outras ferramentas e versionar.

---

## 2. As 5 Peças Obrigatórias

| Peça | Arquivo | Papel |
|---|---|---|
| **1. Cérebro** | `CLAUDE.md` | Define comportamento base do Claude naquela pasta |
| **2. Agentes** | `.claude/agents/*.md` | Papéis especializados (orquestrador, revisor, etc.) |
| **3. Skills** | `.claude/skills/*/SKILL.md` | Cada tarefa do workflow |
| **4. Grafo** | `dependency_graph.json` | Ordem obrigatória entre skills |
| **5. Estado** | `projetos/*/project.json` | Contexto e progresso por projeto/cliente |

---

## 3. Estrutura de Pastas para Replicar

```
meu-agent-copy/                          ← pasta raiz (abrir com Claude Code)
│
├── CLAUDE.md                            ← OBRIGATÓRIO — comportamento base
├── AGENTS.md                            ← documentação dos agents (opcional mas útil)
├── dependency_graph.json                ← grafo de dependências entre skills
├── VERSION.txt                          ← versão do sistema (ex: 1.0.0)
│
├── .claude/
│   ├── agents/
│   │   ├── orquestrador.md             ← agent principal (gerencia fluxo)
│   │   └── revisor-qualidade.md        ← agent de QA (valida outputs)
│   │
│   └── skills/
│       ├── copy-novo-projeto/           ← cadastra novo projeto
│       │   ├── SKILL.md
│       │   └── references/
│       │       └── briefing-fields.md
│       │
│       ├── copy-continuar/              ← retoma trabalho
│       │   └── SKILL.md
│       │
│       ├── copy-s1-pesquisa-icp/        ← skill de pesquisa
│       │   ├── SKILL.md
│       │   ├── schema.json
│       │   └── references/
│       │       └── jtbd-framework.md
│       │
│       ├── copy-s2-angulos/             ← skill de ângulos de copy
│       │   ├── SKILL.md
│       │   ├── schema.json
│       │   └── references/
│       │       └── exemplos-angulos.md
│       │
│       └── copy-s3-variações/           ← skill de variações finais
│           ├── SKILL.md
│           ├── schema.json
│           └── references/
│               └── formulas-copy.md
│
├── projetos/                            ← um diretório por projeto/cliente
│   └── nome-projeto/
│       ├── project.json                ← estado (briefing + progress + history)
│       ├── base-de-conhecimento/       ← docs que o usuário sobe
│       └── outputs/                    ← JSONs gerados pelas skills
│           └── copy-s1-pesquisa-icp.json
│
├── shared-templates/                    ← padrões visuais e contratos de output
│   └── PADRAO-OUTPUT.md               ← campos obrigatórios em todo output JSON
│
└── scripts/                             ← automação (opcional)
    └── render_output.sh               ← gera HTML do output JSON
```

---

## 4. Como Criar o CLAUDE.md (o cérebro)

O CLAUDE.md fica na **raiz do projeto** e é lido automaticamente pelo Claude Code em toda conversa. É o arquivo mais importante — define tudo.

### Template base do CLAUDE.md

```markdown
# [Nome do Sistema] — Agent Instructions

Você é [descrição do papel]. Você opera interativamente com [quem usa] para [objetivo principal].

## Princípios

1. **[Princípio 1].** [Descrição do comportamento esperado.]
2. **[Princípio 2].** [Descrição do comportamento esperado.]
3. **[Princípio 3].** [Descrição do comportamento esperado.]

## Ao iniciar qualquer conversa

1. [O que fazer primeiro]
2. [O que carregar/ler]
3. [O que apresentar ao usuário]
4. [O que perguntar]

## Ao executar uma skill

1. [Passo 1]
2. [Passo 2]
...

## Formato de project.json

[Cole aqui o schema JSON do arquivo de estado]

## Skills disponíveis

### [Módulo 1]
- `skill-nome-1` — [descrição]
- `skill-nome-2` — [descrição]

### [Módulo 2]
- `skill-nome-3` — [descrição]

## Regras críticas

- NUNCA [o que nunca fazer].
- SEMPRE [o que sempre fazer].
```

### O que colocar em cada seção

**"Ao iniciar qualquer conversa"** — instrua o Claude a:
- Identificar a pasta de trabalho
- Ler o estado de todos os projetos ativos
- Apresentar panorama (o que está pendente, em andamento, concluído)
- Perguntar o que o usuário quer trabalhar

**"Ao executar uma skill"** — instrua o Claude a:
- Ler os dados do projeto antes de começar
- Verificar dependências (via `dependency_graph.json`)
- Executar checkpoints em ordem
- Pedir validação do usuário em cada checkpoint
- Registrar decisões no `project.json`
- Salvar output JSON antes de qualquer visualização

**"Regras críticas"** — as mais importantes para QUALQUER sistema:
- Nunca gere output genérico (sempre mencione o projeto/cliente pelo nome)
- Nunca pule checkpoints
- Nunca modifique outputs anteriores sem pedir
- Sempre salve o JSON antes de renderizar o HTML

---

## 5. Como Criar Agents

Localização: `.claude/agents/[nome-do-agent].md`

### Estrutura de um agent

```markdown
---
name: nome-do-agent
description: "Uma linha descrevendo quando este agent é invocado e o que faz."
tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]
---

# Título do Agent

[Descrição do papel e contexto]

## Responsabilidades

### 1. [Responsabilidade 1]
[Instruções específicas]

### 2. [Responsabilidade 2]
[Instruções específicas]

## Regras
- [Regra 1]
- [Regra 2]
```

### Os dois agents que todo sistema precisa

**Agent Orquestrador** — gerencia o ciclo de vida:
- Lê estado de todos os projetos ao iniciar
- Verifica dependências antes de iniciar cada skill
- Executa os checkpoints, apresenta resultados, pede validação
- Atualiza o `project.json` após cada aprovação
- Invoca o revisor de qualidade antes de exports

**Agent Revisor de Qualidade** — valida antes de exportar:
- Verifica se o output menciona o projeto pelo nome (não é genérico)
- Cruza campos com o briefing do projeto
- Valida contra o `schema.json` da skill
- Retorna `{approved: true/false, issues: [...], auto_fixed: [...]}`
- Issues `high` bloqueiam export, `medium/low` apenas alertam

### Diferença entre Agent e Skill

| | Agent | Skill |
|---|---|---|
| **O que é** | Papel permanente com comportamento fixo | Tarefa específica com começo, meio e fim |
| **Quando usar** | Para papéis que se repetem (gerenciar, revisar) | Para entregas únicas (pesquisar, criar copy) |
| **Como invocar** | Automaticamente ou pelo orquestrador | Pelo usuário via `/nome-da-skill` |
| **Tem checkpoint?** | Não | Sim |
| **Gera output?** | Não diretamente | Sim (JSON estruturado) |

---

## 6. Como Criar Skills

Cada skill é uma pasta em `.claude/skills/[nome-da-skill]/`.

### Estrutura da pasta

```
copy-s2-angulos/
├── SKILL.md                ← instruções completas (OBRIGATÓRIO)
├── schema.json             ← schema do output JSON (OBRIGATÓRIO se gera output)
└── references/             ← documentos de apoio (opcional)
    ├── exemplos-angulos.md
    └── formulas-copy.md
```

### Template do SKILL.md

```markdown
---
name: nome-da-skill
description: "Descrição de quando invocar esta skill. Use quando o usuário disser X, Y ou Z."
dependencies: ["skill-anterior-1", "skill-anterior-2"]
outputs: ["nome-do-output.json"]
week: 1
estimated_time: "30-45 min"
---

# Título da Skill

[Descrição do objetivo e importância desta skill]

## Dados necessários

Leia os seguintes arquivos antes de começar:

1. `projetos/{slug}/project.json` (seção `briefing`) — OBRIGATÓRIO
2. `projetos/{slug}/base-de-conhecimento/*.md` — se existirem
3. `projetos/{slug}/outputs/skill-dependente.json` — campo `summary` apenas

## Checkpoints

### Checkpoint 1 — [Nome do checkpoint]

[O que gerar neste checkpoint]

[Formato esperado]

**Apresente ao usuário e pergunte:**
- "[Pergunta de validação 1]"
- "[Pergunta de validação 2]"

Aguarde aprovação antes de avançar.

### Checkpoint 2 — [Nome do checkpoint]

[O que gerar neste checkpoint]

**Apresente ao usuário e pergunte:**
- "[Pergunta de validação]"

Aguarde aprovação antes de avançar.

## Auto-validação (antes de mostrar ao usuário)

- [ ] Mencionou o projeto pelo nome?
- [ ] Usou dados reais do project.json (não inventou)?
- [ ] Nenhum item genérico?
- [ ] Schema validou?
- [ ] Todos os campos obrigatórios preenchidos?

Se falhou → regenere silenciosamente. Não avise o usuário.

## Finalização

Após aprovação:
1. Salve em `projetos/{slug}/outputs/[nome-da-skill].json`
2. Atualize `project.json`: `progress.skills.[nome-da-skill]` → `completed`
3. Registre em `project.json.history[]`
4. Sugira a próxima skill disponível
```

### Como escrever bons checkpoints

Um bom checkpoint tem:
1. **O que fazer** — instrução clara e sem ambiguidade
2. **Formato esperado** — estrutura do que gerar (JSON, lista, texto)
3. **O que apresentar** — como mostrar ao usuário
4. **Pergunta de validação** — o que pedir ao usuário validar
5. **"Aguarde aprovação"** — explícito, nunca avance sozinho

Regra de ouro: **um checkpoint = uma decisão do usuário**.

---

## 7. Como Criar o schema.json

O schema define a estrutura exata do JSON de output. O revisor de qualidade valida contra ele. O renderer de HTML usa ele.

### Template base

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "NomeDaSkill",
  "description": "Descrição do output desta skill.",
  "type": "object",
  "required": ["summary", "campo_obrigatorio_1", "campo_obrigatorio_2"],
  "properties": {

    "summary": {
      "type": "string",
      "description": "Resumo em 1-2 frases. Usado por skills dependentes sem carregar o JSON completo."
    },

    "summary_headline": {
      "type": "string",
      "maxLength": 200,
      "description": "Manchete com o veredito desta skill. Específica, com dados reais."
    },

    "summary_highlights": {
      "type": "array",
      "minItems": 3,
      "maxItems": 6,
      "items": {
        "type": "object",
        "required": ["category", "label", "value"],
        "properties": {
          "category": {"type": "string", "enum": ["posicao", "competicao", "janela", "oportunidade", "risco", "maturidade"]},
          "label": {"type": "string", "maxLength": 40},
          "value": {"type": "string"},
          "subtext": {"type": "string", "maxLength": 80},
          "tone": {"type": "string", "enum": ["green", "yellow", "red", "blue", "gray"]}
        }
      }
    },

    "summary_key_findings": {
      "type": "array",
      "minItems": 3,
      "maxItems": 6,
      "items": {
        "type": "object",
        "required": ["category", "text"],
        "properties": {
          "category": {"type": "string", "enum": ["vantagem", "contexto", "ameaca", "acao"]},
          "text": {"type": "string"}
        }
      }
    },

    "campo_obrigatorio_1": {
      "type": "object",
      "description": "Descrição do campo",
      "required": ["sub_campo_1", "sub_campo_2"],
      "properties": {
        "sub_campo_1": {"type": "string"},
        "sub_campo_2": {"type": "array", "items": {"type": "string"}}
      }
    },

    "honesty_alert": {
      "type": "string",
      "description": "Alerta obrigatório se a análise revelou fragilidade real. Nunca omitir se justificado."
    }
  }
}
```

### Campos obrigatórios em TODO output (padrão do sistema)

| Campo | Tipo | Para que serve |
|---|---|---|
| `summary` | string | Resumo para skills downstream lerem sem carregar o JSON completo |
| `summary_headline` | string (max 200) | Manchete que o stakeholder lê primeiro |
| `summary_highlights` | array de KPIs | Cards visuais com dados em destaque |
| `summary_key_findings` | array de achados | Insights categorizados por tipo |
| `honesty_alert` | string (opcional) | Alerta quando há fragilidade real |

### Regras de completude (crítico)

- **Nunca** deixe campo em branco (`""`) — substitua por `null` + `unavailable_reason`
- **Nunca** omita campo obrigatório — o renderer quebra silenciosamente
- **Arrays vazios legítimos** → adicione `{campo}_note` explicando por quê
- **Estimativas** → marque com `estimated: true` ou `[E]` no texto

---

## 8. Como Criar o dependency_graph.json

Define quais skills precisam estar completas antes de uma skill poder iniciar.

```json
{
  "copy-s1-pesquisa-icp": [],
  "copy-s2-angulos": ["copy-s1-pesquisa-icp"],
  "copy-s3-variações": ["copy-s2-angulos", "copy-s1-pesquisa-icp"],
  "copy-s4-revisao": ["copy-s3-variações"]
}
```

**Regras:**
- Skills sem dependências têm array vazio `[]`
- O orquestrador lê esse arquivo antes de iniciar qualquer skill
- Se falta dependência → avisa o usuário e sugere rodar a dependência primeiro
- O usuário pode forçar (insistir em pular) — o sistema permite mas registra no `history[]`

---

## 9. Exemplo Completo — Agent de Copy

### project.json (estado por projeto)

```json
{
  "meta": {
    "name": "Nome do Projeto",
    "slug": "nome-do-projeto",
    "created_at": "2026-01-01",
    "tipo": "lançamento|perpetuo|anuncio|email"
  },
  "briefing": {
    "produto": "Nome do produto/serviço",
    "proposta_de_valor": "O que entrega de único",
    "publico_alvo": "Descrição do público",
    "ticket": "R$ X",
    "concorrentes": ["Concorrente 1", "Concorrente 2"],
    "tom_de_voz": "formal|profissional|descontraído|informal",
    "objetivo_copy": "O que a copy deve fazer (converter, engajar, educar)",
    "plataformas": ["meta_ads", "google_ads", "email", "landing_page"]
  },
  "progress": {
    "skills": {
      "copy-s1-pesquisa-icp": {"status": "pending", "checkpoint": 0, "completed_at": null},
      "copy-s2-angulos": {"status": "pending", "checkpoint": 0, "completed_at": null},
      "copy-s3-variações": {"status": "pending", "checkpoint": 0, "completed_at": null},
      "copy-s4-revisao": {"status": "pending", "checkpoint": 0, "completed_at": null}
    }
  },
  "history": []
}
```

### CLAUDE.md para Agent de Copy

```markdown
# Agent de Copy IA — Instruções

Você é um especialista em copywriting direto ao ponto. Opera com redatores e marketeiros
para criar copies de alta conversão com base em dados reais do público.

## Princípios

1. **Copy específica, não genérica.** Toda copy deve citar o público, a dor real e o produto pelo nome.
2. **Ângulo antes de variação.** Nunca escreva variações sem antes definir o ângulo estratégico.
3. **Dados reais, nunca suposições.** Use o briefing e o ICP pesquisado. Se falta dado, pergunte.

## Ao iniciar qualquer conversa

1. Leia `projetos/*/project.json` de todos os projetos
2. Mostre panorama: projetos ativos, progresso, próxima skill disponível
3. Pergunte qual projeto trabalhar

## Ao executar uma skill

1. Leia `projetos/{slug}/project.json` — fonte única de verdade
2. Leia `projetos/{slug}/base-de-conhecimento/` — materiais do usuário
3. Leia outputs de skills dependentes (campo `summary` apenas — não o JSON completo)
4. Execute checkpoints em ordem. Nunca pule.
5. Após cada checkpoint aprovado: registre decisão em `history[]`
6. Salve output JSON em `outputs/{skill}.json` antes de qualquer export

## Skills disponíveis

### Pesquisa e Estratégia
- `copy-s1-pesquisa-icp` — Pesquisa do público: dores, desejos, linguagem, objeções
- `copy-s2-angulos` — Define 5-7 ângulos de copy com hipótese de melhor performer

### Produção
- `copy-s3-variações` — Gera 20-30 variações por plataforma seguindo os ângulos definidos
- `copy-s4-revisao` — Revisão final: consistência, tom, CTAs, compliance

## Regras críticas

- NUNCA use frases genéricas como "a melhor solução", "qualidade incomparável", "resultados garantidos"
- NUNCA gere variações antes de ter os ângulos aprovados
- NUNCA aprove copy que não menciona a dor específica do ICP
- SEMPRE cite qual ângulo gerou cada variação (para rastrear performance)
```

### SKILL.md — copy-s2-angulos (exemplo completo)

```markdown
---
name: copy-s2-angulos
description: "Define os ângulos estratégicos de copy antes de produzir variações. Use quando o usuário disser 'ângulos', 'estratégia de copy', 'por onde atacar' ou após completar copy-s1-pesquisa-icp."
dependencies: ["copy-s1-pesquisa-icp"]
outputs: ["copy-s2-angulos.json"]
estimated_time: "30-45 min"
---

# Ângulos de Copy

Você vai definir os ângulos estratégicos que vão guiar TODA a produção de copy.
Um ângulo é a perspectiva única de abordagem — não é o título final, é a hipótese de como tocar o público.

## Dados necessários

1. `projetos/{slug}/project.json` — briefing completo (OBRIGATÓRIO)
2. `projetos/{slug}/outputs/copy-s1-pesquisa-icp.json` — campo `summary` (OBRIGATÓRIO)
3. `projetos/{slug}/base-de-conhecimento/*.md` — se existirem

## Checkpoint 1 — Mapeamento de tensões

Com base no ICP pesquisado, identifique as 5 tensões centrais:

Para cada tensão:
- **Dor:** Como o público articula o problema (linguagem deles, não jargão)
- **Desejo oposto:** O que eles realmente querem (o estado após)
- **Bloqueio:** Por que ainda não resolveram (objeção ou crença limitante)
- **Gatilho:** Evento que faz eles buscarem solução agora

**Apresente as 5 tensões e pergunte:**
- "Alguma tensão não reflete o público real desse produto?"
- "Falta alguma tensão relevante que você conhece desse público?"

Aguarde aprovação antes de avançar.

## Checkpoint 2 — Definição dos ângulos

Com as tensões aprovadas, gere 7 ângulos de copy. Para cada ângulo:

- **Nome do ângulo:** (ex: "Vergonha silenciosa", "Ceticismo de quem já tentou")
- **Tensão de origem:** qual das 5 tensões ele explora
- **Promessa central:** em 1 frase, o que a copy promete
- **Mecanismo:** por que acreditariam (prova, história, dado, lógica)
- **Risco:** por que esse ângulo pode não funcionar
- **Melhor formato:** video curto, carrossel, texto longo, headline

**RECOMENDAÇÃO OBRIGATÓRIA:** Indique qual ângulo você apostaria como melhor performer e por quê.

**Apresente os 7 ângulos e pergunte:**
- "Qual ângulo ressoa mais com o que você conhece desse público?"
- "Tem algum ângulo que está fora do tom de voz da marca?"
- "Quer combinar elementos de mais de um ângulo?"

Aguarde a seleção de 3-5 ângulos para produção.

## Auto-validação

- [ ] Mencionou o produto pelo nome em cada ângulo?
- [ ] Cada ângulo tem tensão de origem clara?
- [ ] Nenhuma promessa genérica ("mude sua vida")?
- [ ] Fez recomendação de melhor performer com justificativa?
- [ ] Tom de voz coerente com o briefing?

Se falhou → regenere silenciosamente.

## Finalização

1. Salve em `projetos/{slug}/outputs/copy-s2-angulos.json`
2. Atualize `project.json`: `progress.skills.copy-s2-angulos` → `completed`
3. Registre em `history[]`: `{"ts": "ISO", "skill": "copy-s2-angulos", "decision": "Ângulos selecionados: [lista]"}`
4. Informe: "Ângulos salvos. Próximo passo: copy-s3-variações vai usar esses ângulos para gerar 20-30 variações."
```

---

## 10. Checklist de Criação

Use este checklist ao montar seu agent do zero.

### Estrutura
- [ ] Pasta raiz criada com nome descritivo
- [ ] `CLAUDE.md` na raiz (com princípios, fluxo de início, lista de skills, regras críticas)
- [ ] `dependency_graph.json` com todas as skills mapeadas
- [ ] `.claude/agents/orquestrador.md` criado
- [ ] `.claude/agents/revisor-qualidade.md` criado
- [ ] Pasta `projetos/` criada (vazia, pronta para receber projetos)
- [ ] Pasta `shared-templates/` com `PADRAO-OUTPUT.md`

### Por skill criada
- [ ] Pasta `.claude/skills/[nome-da-skill]/` criada
- [ ] `SKILL.md` com frontmatter, dependências, checkpoints, auto-validação e finalização
- [ ] `schema.json` com campos obrigatórios + campos específicos da skill
- [ ] `references/` com documentos de apoio (frameworks, exemplos, checklists)
- [ ] Skill adicionada ao `dependency_graph.json`

### Por projeto iniciado
- [ ] Pasta `projetos/[slug]/` criada
- [ ] `project.json` inicializado com meta, briefing, progress (todas skills `pending`), history vazio
- [ ] Pasta `base-de-conhecimento/` criada
- [ ] Pasta `outputs/` criada

### Validação final
- [ ] Abriu o Claude Code na pasta raiz
- [ ] Claude leu o CLAUDE.md e apresentou panorama correto
- [ ] Criou projeto de teste e executou a primeira skill
- [ ] Output JSON gerado com todos os campos obrigatórios
- [ ] Revisor de qualidade invocado e aprovado

---

## 11. Dúvidas Frequentes

**Q: Precisa ser git?**  
Não obrigatoriamente. Git ajuda no `synch-hub` (atualizar skills de um repositório central para times), mas o sistema funciona sem.

**Q: Posso ter uma skill sem schema.json?**  
Sim, mas não recomendado. Sem schema, o revisor de qualidade só verifica consistência — não valida estrutura. Skills operacionais (como `copy-continuar`) não precisam.

**Q: Como fazer o sistema funcionar para um time (várias pessoas)?**  
Suba o repositório no GitHub. Cada membro clona localmente. A pasta `projetos/` pode ser sincronizada via Google Drive ou similar. Os arquivos `.claude/` e `CLAUDE.md` ficam no git — são as instruções do sistema.

**Q: Posso ter skills opcionais (não aparecem em todos os projetos)?**  
Sim. No `project.json`, inclua a skill no `progress.skills` só quando for relevante. No CLAUDE.md, documente sob qual condição a skill aparece (ex: "apenas se tipo = lançamento").

**Q: Como economizar tokens ao referenciar outputs anteriores?**  
Nunca carregue o JSON completo de uma skill anterior. Leia apenas o campo `summary`. É por isso que `summary` é obrigatório em todo output — ele existe para ser consumido por skills downstream com custo mínimo de contexto.

**Q: E se o usuário quiser refazer uma skill já completa?**  
Permita, mas avise que outputs dependentes podem ficar inconsistentes. Registre a decisão em `history[]`. Opcionalmente, versione o output anterior (ex: `copy-s2-angulos-v1.json`).

**Q: Como usar com PRD já existente?**  
Cole o PRD como um documento em `projetos/{slug}/base-de-conhecimento/prd.md`. Na skill, instrua o Claude a ler `base-de-conhecimento/*.md` antes de fazer perguntas — ele vai extrair os dados do PRD automaticamente e só perguntar o que falta.

---

## Referência rápida — Estrutura mínima para começar

Se quiser começar pelo mínimo viável, crie apenas:

```
meu-agent/
├── CLAUDE.md                          ← descreva o papel e as skills disponíveis
├── dependency_graph.json              ← {"skill-1": [], "skill-2": ["skill-1"]}
├── .claude/
│   ├── agents/
│   │   └── orquestrador.md           ← gerencia checkpoints e estado
│   └── skills/
│       └── skill-1/
│           ├── SKILL.md              ← checkpoints + auto-validação
│           └── schema.json           ← estrutura do output
└── projetos/
    └── projeto-teste/
        └── project.json              ← briefing + progress + history
```

Com essas 6 peças, o sistema já funciona. Adicione skills, agents e scripts conforme a necessidade crescer.

---

*Guia gerado em 2026-07-02 | Baseado na arquitetura EE Clientes V4 — V4 Company*
