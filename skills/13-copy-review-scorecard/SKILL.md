---
name: 13-copy-review-scorecard
description: "Revisa linguagem, argumento e fatos da versão exata e executa o gate local antes de entrega/aprovação."
---

# 13-copy-review-scorecard

## Dados necessários

Ler o SKILL.md integralmente. Modos e checkpoints seguem `CONTRATO-OPERACIONAL-MODOS.md`; caminhos relativos à raiz do projeto.

- `knowledge/vicios-ia-humanizacao.md`
- `knowledge/politica-editorial.md`
- `quality/scorecard.md`
- `quality/FORMATO-ENTREGA.md`
- `knowledge/provas-e-claims.md`
- `knowledge/narrativa-lp.md` (somente rota LP)

## Execução e auto-validação

Em revisão avulsa, ler índice/metodologia/rota e contexto necessário. Reler integralmente humanização com recibo de fase review após a última alteração. Não usar a lembrança da produção.

1. Rodar `python3 scripts/copycheck.py caminho/delivery.json`. Bloqueios objetivos voltam à escrita; alertas exigem decisão editorial por ocorrência.
2. Criar review.json com `--review-template`. Conferir inventário de TODAS as afirmações, inclusive não numéricas, com fonte/limite; registrar claim_checks e constraint_checks.
3. Revisar argumento e rota: objetivo/barreira, informação nova, mecanismo, utilidade, voz, viabilidade e conjunto. Avaliar cada critério com trecho EXATO, id do campo e justificativa específica. Não preencher tudo com a mesma justificativa genérica.
   - Em LP, ler apenas a escada de títulos, resumir a tese, testar troca/remoção de dobras, listar repetições e adiamentos para o especialista e contar palavras. Aplicar os tetos de nota de `knowledge/narrativa-lp.md`. Um bom trecho isolado não justifica progressão, especificidade, relevância, redundância ou utilidade da página inteira.
4. Revisar português, cadência, falso contraste, repetição e sintaxe. Preencher notas individuais da rubrica; o código calcula as médias. Registrar limitações reais. Nenhum score compensa falha crítica.
5. Associar delivery_sha256 atual, recibos e resoluções dos alertas. Rodar novamente com `--review caminho/review.json`. Somente ready_for_human_approval libera a 14.

Qualquer alteração em copy, fatos, requisitos ou contexto invalida a revisão. Corrigir e refazer, até 2 ciclos por direção. O script não prova veracidade/gramática completa nem execução mental; evidência registrada e julgamento continuam necessários. Não declarar “sem vícios” só porque um contador passou.

Saída: versão revisada, relatório verificável, scores calculados e limitações; nenhuma aprovação humana presumida.

Em ajuste de escopo ou campo na mesma conversa, usar a revisão derivada de `scripts/revise_delivery.py`. Preencher somente `review-delta.json`: critérios cuja evidência sumiu, critérios afetados pelo papel do campo, claims alterados, restrições e inventário quando aplicáveis. Não refazer scores herdados nem reler fontes intactas. Mudança estratégica/factual continua exigindo revisão completa.
