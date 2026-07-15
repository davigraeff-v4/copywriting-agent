---
name: 13-copy-review-scorecard
description: "Revisa a copy adaptada com o scorecard de 12 critérios antes da entrega final. Use imediatamente após 12-channel-format-adapter, e também quando o gestor pedir '/revisar-copy' sobre uma copy existente."
dependencies: ["12-channel-format-adapter"]
outputs: ["score + copy revisada (pronta para entrega)"]
week: 1
estimated_time: "10-15 min"
---

# Copy Review Scorecard

Revisão crítica antes da entrega — baseada no checklist de revisão pós-copy da Thamy. Ver `quality/scorecard.md` para a régua completa.

## Dados necessários

1. Copy adaptada por canal (skill `12`), ou copy fornecida diretamente pelo gestor via `/revisar-copy`.
2. `quality/scorecard.md` — critérios e régua de aprovação.
3. `knowledge/termos-a-evitar.md`.
4. `knowledge/vicios-ia-humanizacao.md` — OBRIGATÓRIO. Checklist de humanização (8 itens) a rodar além dos 12 critérios do scorecard — pega o que o scorecard sozinho não captura (ritmo, aquecimento, ponto de vista, palavras-bandeira de IA).

## Checkpoint único — Pontuação e decisão

Antes de pontuar, rode o checklist de humanização de `knowledge/vicios-ia-humanizacao.md` (8 itens — ponto de vista, especificidade, adjetivos vagos, variação de conectores, aquecimento inicial, ritmo de frase, palavras-bandeira). Se falhar em 2+ itens, é sinal de que a copy precisa ser reescrita antes mesmo de rodar o scorecard — trate como sintoma de copy genérica, não como detalhe de estilo.

Avalie de 0 a 10 cada um dos 12 critérios de `quality/scorecard.md`:
```
1. Clareza da headline
2. Força da headline
3. Aderência ao público
4. Clareza da subheadline
5. Força da promessa
6. Tradução de característica em benefício
7. Aderência ao canal
8. CTA claro
9. Tom de voz do cliente
10. Nível de especificidade
11. Conexão emocional
12. Risco de promessa exagerada (nota alta = baixo risco)
```

Calcule a nota final (média) e aplique a régua:
```
9 a 10: aprovado
8 a 8,9: aprovado com ajustes leves
7 a 7,9: revisar antes de entregar
abaixo de 7: refazer
```

**Regra operacional inegociável: nunca entregue versão final com nota abaixo de 8.** Se a nota ficar abaixo de 8, reescreva internamente (volte à skill `11-copy-production` ou `12-channel-format-adapter` conforme o problema) e repita a revisão antes de mostrar ao gestor — não mostre a versão reprovada como se fosse a entrega final.

**Verificação de `HARD CONSTRAINTS`:** antes de calcular a nota, confira a copy contra o bloco de hard constraints vigente. Qualquer violação **reprova a copy automaticamente**, mesmo que a média dos 12 critérios seja ≥ 8 — trate como nota abaixo de 8 para efeito da regra acima, reescreva e repita a verificação.

## Modo de operação

Em todos os modos, esta revisão roda **silenciosamente**, antes de qualquer apresentação ao gestor — não existe checkpoint próprio de "aqui está o score, aprova?" separado da entrega.

- **Estratégico:** apresente nota + pontos fracos como checkpoint próprio (compatível com o fluxo de 14 pausas), mas ainda assim sem pausa extra só para o scorecard em si — a pergunta de validação já é a mesma da entrega.
- **Rápido/Express:** incorpore nota final, nota por critério (se pedido) e pontos fracos diretamente dentro do Checkpoint 3 ("Entrega revisada"), junto com a copy final e o pedido de aprovação da skill `14`. Nunca gere uma mensagem separada só para o scorecard antes da entrega.

**Apresente ao gestor apenas a versão que já atingiu nota ≥ 8 e não viola nenhum hard constraint, junto com:**
- Nota final e nota por critério.
- Os 2-3 pontos mais fracos, mesmo estando aprovada.

A pergunta "Além do scorecard, você vê algo que eu não capturei nos critérios?" e o pedido de aprovação/reprovação/ajuste da skill `14` saem juntos, na mesma mensagem, nos modos Rápido/Express.

## Auto-validação

- [ ] Todos os 12 critérios foram pontuados individualmente, não só uma nota geral?
- [ ] Nenhum termo de `knowledge/termos-a-evitar.md` ou de `knowledge/vicios-ia-humanizacao.md` presente?
- [ ] Checklist de humanização (8 itens) foi rodado antes da pontuação?
- [ ] Se nota < 8, a copy foi reescrita ANTES de ser mostrada ao gestor?
- [ ] A copy foi checada contra o bloco `HARD CONSTRAINTS` vigente? Se violou algo, foi tratada como reprovada e reescrita?
- [ ] Nos modos Rápido/Express, o score foi incorporado ao Checkpoint 3 em vez de virar uma mensagem separada?

Se falhou → regenere silenciosamente.

## Finalização

1. Registre a nota final e os pontos fracos para incluir no output da skill `14`.
2. No modo Estratégico, informe: "Copy revisada, nota [X]/10. Próximo passo: `14-final-delivery-feedback`." Nos modos Rápido/Express, siga direto para a skill `14` e apresente tudo junto no Checkpoint 3 — não anuncie essa transição como uma etapa separada.
