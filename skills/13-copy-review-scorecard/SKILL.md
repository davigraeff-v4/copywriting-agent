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
- `quality/DESENVOLVIMENTO-EDITORIAL.md` (comparar intenção e texto, diagnosticar falha antes das notas)
- `knowledge/provas-e-claims.md`
- `knowledge/narrativa-lp.md` (somente rota LP)

- `quality/CICLO-REVISAO.md` (diagnóstico, reescrita limitada e encaminhamento)

- `quality/REDUNDANCIA.md` (contribuição por campo, compressão e julgamento de retomadas)

## Execução e auto-validação

Em revisão avulsa, ler índice/metodologia/rota e contexto necessário. Reler integralmente humanização com recibo de fase review após a última alteração. Não usar a lembrança da produção.

1. Rodar `python3 scripts/copycheck.py caminho/delivery.json`. Bloqueios objetivos exigem conferir a causa: texto incorreto volta à escrita; metadados, mapeamento ou representação incorretos são corrigidos sem reescrever texto válido. O diagnóstico precisa explicar o erro que realmente bloqueou. Alertas exigem decisão editorial por ocorrência.
2. Criar review.json com `--review-template`. Conferir inventário de TODAS as afirmações, inclusive não numéricas, com fonte/limite; registrar claim_checks e constraint_checks.
3. Revisar argumento e rota: objetivo/barreira, informação nova, mecanismo, utilidade, voz, viabilidade e conjunto. Avaliar cada critério com trecho EXATO, id do campo e justificativa específica. Não preencher tudo com a mesma justificativa genérica.
   - Comparar a copy com a direção, sem tomar plano preenchido como evidência de realização. Registrar fragilidade material, ou observação concreta que justifica sua ausência. Distinguir contexto/evidência, recuperação, direção, escrita e revisão; sem evidência causal, registrar indeterminada. Usar notas/justificativas existentes, sem outro score ou gate.
   - Em LP, ler apenas a escada de títulos, resumir a tese, testar troca/remoção de dobras, listar repetições e adiamentos para o especialista e contar palavras. Aplicar os tetos de nota de `knowledge/narrativa-lp.md`. Um bom trecho isolado não justifica progressão, especificidade, relevância, redundância ou utilidade da página inteira.
4. Revisar português, cadência, falso contraste, repetição e sintaxe. Em redundância, comparar dois trechos e sua função antes de descontar, conforme `quality/REDUNDANCIA.md`. Conferir se as referências declaradas se realizaram nos campos e se a técnica é compatível, sem tratar presença de citação como prova de melhora. Preencher notas individuais da rubrica; o código calcula as médias. Registrar limitações reais. Nenhum score compensa falha crítica.
5. Associar delivery_sha256 atual, recibos e resoluções dos alertas. Rodar novamente com `--review caminho/review.json`. Somente ready_for_human_approval libera a 14.

Qualquer alteração em copy, fatos, requisitos ou contexto invalida a revisão. Corrigir e refazer, até 2 ciclos por direção. O script não prova veracidade/gramática completa nem execução mental; evidência registrada e julgamento continuam necessários. Não declarar “sem vícios” só porque um contador passou.

Saída: versão revisada, relatório verificável, scores calculados e limitações; nenhuma aprovação humana presumida.

Em ajuste de escopo ou campo na mesma conversa, usar a revisão derivada de `scripts/revise_delivery.py`. Preencher somente `review-delta.json`: critérios cuja evidência sumiu, critérios afetados pelo papel do campo, claims alterados, restrições e inventário quando aplicáveis. Não refazer scores herdados nem reler fontes intactas. Mudança estratégica/factual continua exigindo revisão completa.

Bloqueio corrigível segue o ciclo registrado por `scripts/review_cycle.py`, na mesma pasta entre tentativas. Executar a próxima ação autorizada; preservar texto e revisão de cada tentativa. Ao esgotar, apresentar a falha e o encaminhamento concreto. Nunca tratar tentativa interna como aprovação humana.
