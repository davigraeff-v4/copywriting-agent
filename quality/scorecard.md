# Revisão por evidência v2

Três camadas: verificação objetiva, julgamento editorial e sustentação factual. A versão atual precisa passar nas três; nenhum score compensa falha crítica. A aprovação humana é um estado posterior.

## Critérios gerais (inteiros de 0 a 10)

A lista executável está em `quality/rubric.json`:

| Critério | Pergunta |
|---|---|
| objetivo | A peça conduz à decisão/ação solicitada? |
| barreira | Responde ao desconhecimento, dúvida, desejo ou motivação real? |
| especificidade | Usa situação, mecanismo ou critério relevante além de nome, cargo ou característica genérica? |
| progressao | A peça desenvolve uma tese; em LP, títulos e dobras formam uma sequência que perde sentido se reordenada? |
| relevancia | O argumento interessa ao comprador/leitor correto? |
| evidencia | Afirmações têm fonte e alcance proporcionais? |
| mecanismo | Relações de causa e benefício são defensáveis? |
| voz | Linguagem pertence à marca/pessoa e respeita o registro? |
| formato | Cumpre briefing, canal, campos e viabilidade? |
| acao | Próximo passo/encerramento é adequado, inclusive sem CTA quando justificado? |
| coerencia | Não há contradição dentro da peça ou com contexto/restrições? |
| utilidade | Leitor recebe informação suficiente para a função da peça? |

0–3: errado/ausente; 4–6: fraco/genérico; 7: precisa de ajuste; 8: suficiente; 9–10: forte, com evidência específica. Não atribuir nota alta por cumprir template. Objetivo, barreira, especificidade, progressão, evidência, mecanismo, voz e formato precisam individualmente de 8 ou mais.

Para LP, aplicar também os testes e tetos de `knowledge/narrativa-lp.md`. A justificativa de progressão precisa considerar a escada completa de títulos e a dependência entre dobras. A justificativa de especificidade precisa apontar um insight de decisão, não apenas uma lista de ocupações. A justificativa de redundância precisa comparar todas as dobras.

## Humanização (0, 5 ou 10)

Português, sintaxe, registro, ritmo, redundância, entrada, vocabulário e naturalidade. 0: falha clara; 5: parcial; 10: atende. Julgar adequação, não identificação da autoria por IA.

Ambas as médias precisam atingir 8; calculadas pelo código a partir das notas individuais, nunca digitadas como estimativa. Com 8 dimensões de 0/5/10, resultados são múltiplos de 0,625; 8,6 ou 9,1 não são médias possíveis. Scores antigos não são comparáveis diretamente à rubrica v2.

## Evidência da revisão

Cada critério exige campo, trecho literal e justificativa. Referenciar outros campos na justificativa para revisão do conjunto. Conferir inventário de todas as afirmações, inclusive qualitativas e causais; inventário vazio precisa de justificativa verdadeira. Conferir cada restrição semântica.

Problemas críticos entram em critical_issues e bloqueiam: claim falso/sem base, restrição violada, objetivo/público errado, causalidade inventada, português que compromete sentido ou falta de substância central. Alertas objetivos precisam de resolução por campo/regra; não resolvê-los em lote com “ok”.

## Processo

A skill 13 lê humanização novamente, avalia texto e fatos, preenche review.json e executa copycheck. A skill 14 renderiza somente com status ready_for_human_approval. Conteúdo ou contexto alterado muda hash e exige revisão nova. Recibos registram fontes lidas, mas não provam compreensão; revisão semântica segue responsável por sustentar suas conclusões.

Uma segunda leitura pelo mesmo modelo não é julgamento independente. Calibrar esta rubrica com feedback humano e avaliação cega em `evals/README.md`.
