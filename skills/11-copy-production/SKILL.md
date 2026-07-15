---
name: 11-copy-production
description: "Escreve a copy final com base em briefing, marca, público, funil, big idea, oferta, framework e CTA já definidos. Use após 09-offer-promise-analysis (fluxo simples) ou 10-framework-trigger-selector (fluxo estratégico completo) — nunca antes."
dependencies: ["09-offer-promise-analysis"]
outputs: ["copy final (base, antes da adaptação por canal)"]
week: 1
estimated_time: "20-30 min"
---

# Copy Production

O coração do agent: escreve a copy final combinando tudo que foi decidido nas skills anteriores.

## Dados necessários

1. Briefing organizado (`01`), análise de marca (`03`), oferta/promessa (`09`) — OBRIGATÓRIO.
2. Big idea (`08`) e framework/gatilho/CTA (`10`), quando existirem (fluxo estratégico completo).
3. Persona (`05`), quando existir.
4. `knowledge/metodologia-thamy.md`, `knowledge/banco-de-headlines.md`, `knowledge/termos-a-evitar.md`.
5. `knowledge/banco-de-ganchos.md` — aberturas prontas por categoria (adaptar à persona real, nunca usar 1:1).
6. `knowledge/processo-de-copy.md` — as 12 regras de copy de alta conversão, como checklist complementar ao scorecard.
7. `knowledge/vicios-ia-humanizacao.md` — OBRIGATÓRIO. Os 12 vícios de linguagem de IA e a lista negra de palavras — evitar desde a primeira escrita, não só na revisão.

## Checkpoint único — Copy base

Produza a copy final combinando:

```
briefing
marca
público
funil
objetivo
canal
formato
big idea
oferta
framework
gatilho
CTA
tom de voz
```

Critérios obrigatórios — a copy deve ser:
```
clara
humana
conversacional
específica
orientada a benefício
conectada com o público
não genérica
não excessivamente funcional
```

Regra crítica: nunca use termos de `knowledge/termos-a-evitar.md` nem da lista negra de `knowledge/vicios-ia-humanizacao.md`. Nunca escreva a copy antes de ter oferta (skill 09) e, no fluxo estratégico, framework (skill 10) definidos. Comece direto pelo gancho/promessa — sem parágrafo de aquecimento (vício #10 de `vicios-ia-humanizacao.md`). Consulte o bloco `HARD CONSTRAINTS` vigente antes de escrever qualquer linha — nenhuma promessa/claim pode violá-lo.

## Modo de operação

- **Estratégico:** produza a copy base (sem adaptação de canal ainda) e pergunte, como abaixo. A skill `12` adapta depois, em checkpoint separado.
- **Rápido/Express:** não produza uma copy base genérica intermediária. Escreva já em conjunto com o contrato de canal/formato da skill `12` (ver `CONTRATO-OPERACIONAL-MODOS.md` seção 5) — o gestor só vê a versão final já adaptada, dentro do Checkpoint 3 ("Entrega revisada"), junto com scorecard e entrega.

**Apresente a copy e pergunte (checkpoint isolado só no modo Estratégico; nos modos Rápido/Express, a pergunta some para dentro do Checkpoint 3):**
- "Essa copy captura a big idea e fala a língua dessa persona?"
- "Algum trecho soa genérico ou fora do tom da marca?"

No modo Estratégico, aguarde aprovação antes de avançar — esta copy ainda não está adaptada por canal, isso é a skill 12.

## Auto-validação

- [ ] Cita o produto/cliente e a dor/desejo específicos, não é copy genérica reaproveitável para qualquer marca?
- [ ] Nenhum termo de `knowledge/termos-a-evitar.md` ou da lista negra de `knowledge/vicios-ia-humanizacao.md` presente?
- [ ] Nenhum vício de IA óbvio (travessão descontextualizado, "não é X, é Y", aquecimento antes do gancho, adjetivo vago sem evidência)?
- [ ] Todas as características viraram benefício (consistente com skill 09)?
- [ ] CTA está presente e alinhado ao objetivo?
- [ ] Rastreável: dá para dizer qual framework/ângulo gerou essa copy?

Se falhou → regenere silenciosamente.

## Finalização

1. Informe: "Copy base produzida. Próximo passo: `12-channel-format-adapter` para adaptar ao(s) canal(is) do briefing."
