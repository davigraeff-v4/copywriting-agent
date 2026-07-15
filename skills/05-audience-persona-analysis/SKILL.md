---
name: 05-audience-persona-analysis
description: "Transforma o público-alvo do briefing em leitura estratégica: dores, desejos, objeções, medos, motivadores, nível de consciência, linguagem provável, estilo de vida desejado. Use no fluxo estratégico completo, após 03-brand-context-analysis, quando o usuário disser 'persona', 'público', 'quem é esse público' ou pedir análise estratégica."
dependencies: ["03-brand-context-analysis"]
outputs: ["análise de público/persona (em memória de conversa)"]
week: 1
estimated_time: "15-20 min"
---

# Audience & Persona Analysis

A metodologia da Thamy começa justamente por conhecer público, dores e estilo de vida desejado. Esta skill traduz o "público-alvo" do briefing em algo acionável para escrever copy específica.

## Dados necessários

1. Estrutura organizada (skill `01`) e análise de marca (skill `03`) — OBRIGATÓRIO.
2. `clients/{cliente}.md` — se já tiver persona validada, use como base e apenas refine para esta campanha.
3. `knowledge/metodologia-thamy.md` — as 11 perguntas e o princípio central (JTBD) que orientam a leitura de público.
4. `knowledge/use-case-map-exemplos.md` — framework persona→problema→proposta de valor com exemplos reais (V4 Company, Smart Fit); use como referência de profundidade esperada.
5. `knowledge/exemplos-de-estruturas.md` — exemplo real de estudo de público (nicho fitness) mostrando segmentação, dores em camadas e vocabulário de nicho.

## Checkpoint único — Persona operacional

Mapeie:

```
Persona operacional (nome fictício + descrição curta):
Dores:
Desejos:
Objeções:
Medos:
Motivadores:
Nível de consciência (topo | meio | fundo — hipótese inicial, refinado na skill 06):
Linguagem provável (como essa pessoa fala sobre o problema):
Estilo de vida desejado (o "depois" que ela busca):
```

Regra: se o briefing não trouxe persona (campo "normalmente faltante" segundo o PRD), crie uma persona operacional inferida a partir do público, marca e materiais disponíveis — sinalize claramente com "[H] Persona inferida — validar com o gestor."

## Modo de operação

- **Estratégico:** apresente a persona isoladamente e pergunte, como abaixo.
- **Rápido/Express:** rode silenciosamente dentro do bloco de pesquisa (junto com `03`, `06`, `07`, `08`, `09`, `10`) e leve a persona (com hipóteses `[H]` explícitas) para o Checkpoint 2 ("Mapa estratégico"). Não gera pausa própria.

**Apresente a persona e pergunte (checkpoint isolado, modo Estratégico; ou dentro do Mapa estratégico, modos Rápido/Express):**
- "Essa leitura do público reflete quem você conhece desse cliente?"
- "Alguma dor/objeção está errada ou faltando?"

Aguarde aprovação antes de avançar.

## Auto-validação

- [ ] Mencionou o produto/cliente pelo nome (não é persona genérica de mercado)?
- [ ] Dores e desejos são específicos, não clichês ("quer ser feliz", "quer economizar")?
- [ ] Persona inferida está claramente sinalizada como hipótese?
- [ ] Linguagem provável usa vocabulário real, não jargão de marketing?

Se falhou → regenere silenciosamente.

## Finalização

1. Se a persona for nova/validada e o cliente ainda não tiver isso registrado, sugira `04-client-memory-builder`.
2. Informe: "Análise de público concluída. Próximo passo: `06-funnel-consciousness-mapping`."
