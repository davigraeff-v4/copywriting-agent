# Avaliação da otimização

## O que está pronto

12 briefings sintéticos controlados em `evals/cases.json`: 4 LPs, 4 demandas sociais, 4 anúncios. Não são prompts históricos reconstruídos nem aprovações de cliente. A pasta é excluída da recuperação de referências. Casos reais da DMF, Viezza e Scann-Up são regressões de desenvolvimento já conhecidas; não contá-los como teste cego inédito.

O verificador e os testes medem cumprimento objetivo. Só avaliação humana de novas saídas pode sustentar preferência editorial pelo agent. Não usar autoavaliação da mesma geração como resultado do benchmark.

## Comparação controlada

1. Congelar o mesmo briefing e pacote factual para três condições: LLM com instrução simples, agent anterior (snapshot local) e agent v2. Usar exatamente o mesmo identificador de modelo e esforço médio; não presumir que o alias `sonnet` identifica a versão usada no teste original.
2. Fazer duas execuções independentes por condição e briefing: 12 × 3 × 2 = 72 saídas. Comparar inicialmente contexto idêntico; depois avaliar recuperação de Drive separadamente. Acesso ao mesmo Drive não garante seleção dos mesmos documentos.
3. Registrar identificação exata do modelo, esforço, hashes do prompt/contexto/instrução de sistema, texto, latência e consumo quando disponíveis. Sessões novas, sem histórico da comparação. Configuração de ferramentas e habilidades deve ser documentada por condição.
4. Uma ablação opcional compara v2 com e sem exemplos curados nos casos de desenvolvimento. Não decidir adicionar RAG vetorial antes de observar falha de recuperação que justifique isso.
5. Entregar apenas copies, briefings e evidências ao avaliador, em ordem embaralhada. Guardar o mapa de sistemas separado. A formatação textual pode revelar a condição; o embaralhamento reduz viés de identificação, sem garantir cegamento perfeito.
6. Avaliador humano escolhe a preferida por caso, justifica com trechos, marca violações e mede tempo real de edição até utilizável. Aprovação deve considerar argumento, especificidade, progressão, voz e português, além dos critérios por rota. Comparar resultados por LP, social e anúncios; não diluir regressão de LP em bom resultado de estáticos.

Meta inicial proposta, sujeita à calibração: zero violações objetivas; preferência humana pela v2 em pelo menos 70% das comparações; menor tempo de edição. Reportar empates e denominador. Amostra pequena e repetições do mesmo briefing não comprovam ganho de conversão.

## Ferramenta

Arquivo `records.json` é uma lista de objetos com `case_id`, `repetition`, `system`, `model_id`, `effort`, `prompt_sha256`, `context_sha256`, `system_prompt_sha256`, `text`; opcionais `latency_seconds`, `input_tokens`, `output_tokens`, `cost`. Hashes devem refletir os materiais efetivamente enviados, não nomes de arquivos.

```
python3 scripts/evaluate.py prepare evals/runs/records.json --out evals/runs/blind-001
python3 scripts/evaluate.py summarize evals/runs/blind-001/key-private.json evals/runs/blind-001/votes.json
```

`prepare` rejeita comparação com modelos, esforços, prompts ou contextos distintos e não sobrescreve diretório. `votes.json` exige `rater`, `winner` (A/B/C ou `tie`) e `reason`. `hard_failures` aceita `{ "label": "A", "reason": "trecho e regra violada" }`. Não colocar chaves privadas junto das opções apresentadas ao avaliador.

O script não chama LLM, não cria agente e não inventa avaliações. Execução das 72 gerações com o Sonnet solicitado e julgamento humano continuam pendentes. Autenticação de uma CLI não confirma disponibilidade daquele modelo exato. O snapshot anterior local fica em `.local/optimization-2026-09-08/baseline/`; não versionar dados de clientes para publicar o benchmark.
