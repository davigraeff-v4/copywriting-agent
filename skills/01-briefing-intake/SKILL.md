---
name: 01-briefing-intake
description: "Recebe o briefing colado no chat (ou links/observações do gestor) e transforma em estrutura organizada. Use sempre que um briefing novo for colado no chat, ou quando o usuário disser 'novo briefing', 'nova campanha' ou pedir '/copy-final' sem ter rodado essa skill ainda nesta conversa."
dependencies: []
outputs: ["briefing-organizado (em memória de conversa, ou salvo em outputs/drafts/ se pedido)"]
week: 1
estimated_time: "5-10 min"
---

# Briefing Intake

Primeira skill do fluxo. Recebe o material bruto do gestor — briefing colado, links, observações — e organiza em uma estrutura padrão que todas as skills seguintes vão consumir.

## Dados necessários

1. O texto colado pelo gestor no chat — OBRIGATÓRIO.
2. `clients/{cliente}.md`, se já existir — para preencher lacunas com dados já conhecidos do cliente.
3. `briefings/briefing-template.md` — como referência de campos esperados.

## Checkpoint único — Estrutura organizada

Reorganize o material recebido no formato:

```
Cliente:
Campanha:
Objetivo:
Canal:
Formato:
Público:
Persona:
Oferta:
Referências:
Restrições:
Links auxiliares:
Pontos faltantes:
```

Regras:
- Não invente dado que não veio no briefing e não está em `clients/{cliente}.md` — deixe o campo como "não informado" e liste em "Pontos faltantes".
- Se o gestor colou algo em formato livre (não estruturado), extraia o que for possível e preserve qualquer observação solta em uma seção "Observações do gestor" no final.
- Se `clients/{cliente}.md` já tiver tom de voz, público ou restrições, preencha esses campos a partir dali e sinalize que veio da memória do cliente (não do briefing atual).

## Modo de operação

- **Estratégico:** apresente a estrutura organizada e pergunte "Essa organização está correta? Faltou algo que você mencionou?" — aguarde confirmação antes de avançar.
- **Rápido/Express:** se a extração do briefing for clara (sem campo ambíguo), não pare aqui — encaminhe direto para `02-briefing-diagnosis` no mesmo turno e apresente as duas juntas no Checkpoint 1. Só pause isoladamente se o material recebido for confuso demais para organizar com confiança.

Em qualquer modo: preserve toda observação solta do gestor e qualquer sinalização de fonte permitida/proibida — isso alimenta o Checkpoint 1 (`02`) e o bloco `HARD CONSTRAINTS`.

## Auto-validação

- [ ] Todos os campos do template foram considerados (mesmo que "não informado")?
- [ ] Nenhum dado foi inventado?
- [ ] "Pontos faltantes" lista exatamente os campos vazios?
- [ ] Dados vindos de `clients/{cliente}.md` estão sinalizados como tal?

Se falhou → regenere silenciosamente.

## Finalização

1. Mantenha a estrutura organizada disponível para as próximas skills nesta conversa.
2. Se o gestor pedir para salvar, grave em `outputs/drafts/{cliente}-{campanha}-briefing.md`.
3. Informe: "Briefing organizado. Próximo passo: `02-briefing-diagnosis` para checar se há informação suficiente para produzir."
