---
name: 13-copy-review-scorecard
description: "Revisa a copy adaptada com 12 critérios gerais e um score obrigatório de humanização/anti-vícios de IA antes da entrega ou aprovação. Use imediatamente após 12-channel-format-adapter, quando o gestor pedir '/revisar-copy' ou quando '/aprovar-copy' não tiver scores válidos para a versão atual."
dependencies: ["12-channel-format-adapter"]
outputs: ["score + copy revisada (pronta para entrega)"]
week: 1
estimated_time: "10-15 min"
---

# Copy Review Scorecard

Revisão crítica antes da entrega — baseada no checklist de revisão pós-copy da Thamy. Ver `quality/scorecard.md` para a régua completa.

## Dados necessários

1. Copy adaptada por canal (skill `12`), ou copy fornecida diretamente pelo gestor via `/revisar-copy`.
2. `knowledge/README.md` e `knowledge/metodologia-thamy.md` — OBRIGATÓRIOS pelo Knowledge Gate, inclusive em revisão avulsa.
3. `quality/scorecard.md` — critérios, fórmula e gates de aprovação.
4. `knowledge/termos-a-evitar.md`.
5. `knowledge/vicios-ia-humanizacao.md` — OBRIGATÓRIO. Releia integralmente antes de pontuar; não reutilize apenas a lembrança da leitura feita na skill `11`.
6. `knowledge/provas-e-claims.md` — OBRIGATÓRIO quando a copy contiver claim quantitativo, comparativo, superlativo, garantia, case ou promessa sensível.
7. `knowledge/erros-comuns.md` — usar como checklist diagnóstico complementar, especialmente em revisão avulsa.

Se os itens 2, 3 e 5 não tiverem sido lidos na execução atual desta skill, pare: a copy não pode ser pontuada, entregue nem aprovada.

## Checkpoint único — Pontuação e decisão

Calcule separadamente os dois scores definidos em `quality/scorecard.md`:

1. **Score Geral:** média dos 12 critérios gerais abaixo.
2. **Score de Humanização/Anti-Vícios de IA:** média das 8 dimensões do checklist de humanização, cada uma pontuada em 0, 5 ou 10.

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

Calcule o Score Geral (média) e aplique a régua:
```
9 a 10: aprovado
8 a 8,9: aprovado com ajustes leves
7 a 7,9: revisar antes de entregar
abaixo de 7: refazer
```

**Gates operacionais inegociáveis:** Score Geral ≥ 8/10; Score de Humanização/Anti-Vícios de IA ≥ 8/10; zero vício crítico; zero violação de `HARD CONSTRAINTS`; Knowledge Gate concluído. Falhar em qualquer gate reprova a versão. Reescreva internamente (volte à skill `11-copy-production` ou `12-channel-format-adapter` conforme o problema) e repita **os dois scores** antes de mostrar ao gestor.

Considere vício crítico: dado/prova inventado para parecer específico; abertura inteira de aquecimento; palavra/expressão da lista negra usada como muleta central; ou dois ou mais vícios dos 12 padrões aparecendo de forma recorrente. Um vício crítico reprova mesmo que os dois scores sejam ≥ 8.

**Verificação de `HARD CONSTRAINTS`:** antes de calcular os scores, confira a copy contra o bloco vigente. Qualquer violação **reprova a copy automaticamente**, mesmo que as médias sejam ≥ 8 — trate como gate reprovado, reescreva e repita a revisão completa.

## Modo de operação

Em todos os modos, esta revisão roda **silenciosamente**, antes de qualquer apresentação ao gestor — não existe checkpoint próprio de "aqui está o score, aprova?" separado da entrega.

- **Estratégico:** apresente os dois scores + pontos fracos como checkpoint próprio (compatível com o fluxo de 14 pausas), mas ainda assim sem pausa extra só para o scorecard em si — a pergunta de validação já é a mesma da entrega.
- **Rápido/Express:** incorpore os dois scores, notas por critério/dimensão (se pedido) e pontos fracos diretamente dentro do Checkpoint 3 ("Entrega revisada"), junto com a copy final e o pedido de aprovação da skill `14`. Nunca gere uma mensagem separada só para o scorecard antes da entrega.

**Apresente ao gestor apenas a versão que passou por todos os gates, junto com:**
- Score Geral e Score de Humanização/Anti-Vícios de IA.
- Nota por critério/dimensão, se pedida.
- Os 2-3 pontos mais fracos, mesmo estando aprovada.

A pergunta "Além do scorecard, você vê algo que eu não capturei nos critérios?" e o pedido de aprovação/reprovação/ajuste da skill `14` saem juntos, na mesma mensagem, nos modos Rápido/Express.

## Auto-validação

- [ ] Knowledge Gate concluído nesta execução da skill, incluindo releitura integral de `knowledge/vicios-ia-humanizacao.md`?
- [ ] Todos os 12 critérios gerais foram pontuados individualmente, não só uma nota geral?
- [ ] As 8 dimensões de humanização foram pontuadas em 0, 5 ou 10 e tiveram média própria?
- [ ] Nenhum termo de `knowledge/termos-a-evitar.md` ou de `knowledge/vicios-ia-humanizacao.md` presente?
- [ ] Nenhum vício crítico foi detectado?
- [ ] Claims sensíveis foram confrontados com fonte, limite e formulação permitida conforme `knowledge/provas-e-claims.md`?
- [ ] Se qualquer score ficou < 8 ou outro gate falhou, a copy foi reescrita ANTES de ser mostrada ao gestor?
- [ ] A copy foi checada contra o bloco `HARD CONSTRAINTS` vigente? Se violou algo, foi tratada como reprovada e reescrita?
- [ ] Nos modos Rápido/Express, o score foi incorporado ao Checkpoint 3 em vez de virar uma mensagem separada?

Se falhou → regenere silenciosamente.

## Finalização

1. Registre o Score Geral, o Score de Humanização/Anti-Vícios de IA e os pontos fracos para incluir no output da skill `14`.
2. No modo Estratégico, informe: "Copy revisada: Score Geral [X]/10; Humanização [Y]/10. Próximo passo: `14-final-delivery-feedback`." Nos modos Rápido/Express, siga direto para a skill `14` e apresente tudo junto no Checkpoint 3 — não anuncie essa transição como uma etapa separada.
