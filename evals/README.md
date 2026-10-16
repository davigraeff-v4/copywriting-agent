# Avaliação da otimização

## O que está pronto

13 briefings sintéticos controlados em `evals/cases.json`: 5 LPs, 4 demandas sociais, 4 anúncios. O protocolo original tinha 12; o caso lp-05 foi acrescentado em 09/09. Não são prompts históricos reconstruídos nem aprovações de cliente. A pasta é excluída da recuperação de referências. Casos reais da DMF, Viezza e Scann-Up são regressões de desenvolvimento já conhecidas; não contá-los como teste cego inédito.

O verificador e os testes medem cumprimento objetivo. Só avaliação humana de novas saídas pode sustentar preferência editorial pelo agent. Não usar autoavaliação da mesma geração como resultado do benchmark.

## Comparação controlada

1. Congelar o mesmo briefing e pacote factual para três condições: LLM com instrução simples, agent anterior (snapshot local) e agent v2. Usar exatamente o mesmo identificador de modelo e esforço médio; não presumir que o alias `sonnet` identifica a versão usada no teste original.
2. Fazer duas execuções independentes por condição e briefing: o protocolo original previa 12 × 3 × 2 = 72 saídas; usar os 13 casos atuais resulta em 78. O piloto menor em `evals/PILOTO-EDITORIAL.md` permite começar antes dessa rodada. Comparar inicialmente contexto idêntico; depois avaliar recuperação de Drive separadamente. Acesso ao mesmo Drive não garante seleção dos mesmos documentos.
3. Registrar identificação exata do modelo, esforço, hashes do prompt/contexto/instrução de sistema, texto, latência e consumo quando disponíveis. Sessões novas, sem histórico da comparação. Configuração de ferramentas e habilidades deve ser documentada por condição.
4. Uma ablação opcional compara o fluxo atual com e sem exemplos curados nos casos de desenvolvimento. O RAG local já existe; sua otimização está separada desta etapa editorial. Registrar consultas, seleção e leitura de referências quando variarem entre condições; nesse caso, medir o efeito do fluxo completo, sem atribuí-lo só à escrita.
5. Entregar apenas copies, briefings e evidências ao avaliador, em ordem embaralhada. Guardar o mapa de sistemas separado. A formatação textual pode revelar a condição; o embaralhamento reduz viés de identificação, sem garantir cegamento perfeito.
6. Avaliador humano escolhe a preferida por caso, justifica com trechos, marca violações e mede tempo real de edição até utilizável. Aprovação deve considerar argumento, especificidade, progressão, voz e português, além dos critérios por rota. Comparar resultados por LP, social e anúncios; não diluir regressão de LP em bom resultado de estáticos.

Meta inicial proposta, sujeita à calibração: zero violações objetivas; preferência humana pela v2 em pelo menos 70% das comparações; menor tempo de edição. Reportar empates e denominador. Amostra pequena e repetições do mesmo briefing não comprovam ganho de conversão.

## Ferramenta

Arquivo `records.json` é uma lista de objetos com `case_id`, `repetition`, `system`, `model_id`, `effort`, `prompt_sha256`, `context_sha256`, `system_prompt_sha256`, `text`; opcionais `latency_seconds`, `input_tokens`, `output_tokens`, `cost`. Para o avaliador receber o pedido, incluir `briefing` e `route` juntos; precisam ser iguais nas condições de cada comparação. Usar a mesma matriz de sistemas em todos os casos. Hashes devem refletir os materiais efetivamente enviados, não nomes de arquivos. Instruções de sistema podem diferir por condição; briefing e fatos permanecem iguais. Os hashes declarados não são autenticados pelo script.

```
python3 scripts/evaluate.py prepare evals/runs/records.json --out evals/runs/blind-001
python3 scripts/evaluate.py summarize evals/runs/blind-001/key-private.json evals/runs/blind-001/votes.json
```

`prepare` rejeita comparação com modelos, esforços, prompts ou contextos distintos e não sobrescreve diretório. `votes.json` exige `rater`, `winner` (A/B/C ou `tie`) e `reason`. `hard_failures` aceita `{ "label": "A", "reason": "trecho e regra violada" }`. Não colocar chaves privadas junto das opções apresentadas ao avaliador.

`edit_minutes` associa rótulo a minutos efetivamente medidos, com valores finitos não negativos. Ausência permanece N/A, sem estimativa. `assessments` é opcional: rótulo → dimensão (`argumento`, `especificidade`, `voz`, `progressao`, `portugues`, `utilidade`) → `{score: 1..5, quote, reason}`. Notas são humanas, não as do gate. Dimensões não avaliadas permanecem sem medida. `diagnoses` aceita rótulo → `{stage, reason}`, com etapa `contexto_evidencia`, `recuperacao`, `direcao`, `escrita`, `revisao` ou `indeterminada`. São relatos do avaliador, não causas provadas.

`summarize` separa votos e pendências por rota, empates, falhas, contagem/média/mediana dos minutos e das dimensões avaliadas, além dos diagnósticos relatados. Mede cada variável separadamente, sem score agregado de criatividade. Informar apenas votos concluídos ao apurar parcialmente; formulários em branco continuam pendentes, nunca viram votos. O script exige texto nas justificativas/citações, mas não autentica o avaliador, a medição ou a veracidade da análise.

O script não chama LLM, não cria agente e não inventa avaliações. A execução comparativa e o julgamento humano continuam pendentes. A menção histórica ao Sonnet não fixa o modelo do novo piloto; registrar o modelo exato e o esforço efetivamente usados. Autenticação de uma CLI não confirma disponibilidade de um modelo. O snapshot anterior local fica em `.local/optimization-2026-09-08/baseline/`; não versionar dados de clientes para publicar o benchmark.

## Repertório proativo e seleção de skills

Ao testar autonomia, fornecer briefing e catálogo/entrada, permitir leitura e busca reais e registrar ferramentas. Não pré-carregar uma lista fixa de skills ou uma referência vencedora. O protocolo precisa distinguir escolha observada de obediência a dependências obrigatórias. Comparar o fluxo completo com baseline congelado e, para investigar contribuição de repertório, usar ablação com as mesmas skills/instruções sem referências externas; diferenças de consulta/seleção impedem atribuição exclusiva à escrita. Registrar fonte/trecho, escolha orientada, aplicação nos campos, contribuição julgada e eventual piora/ausência de ganho. Descartes precisam de motivos individuais. Reavaliar textos antigos e novos com a mesma calibração de redundância; score histórico isolado não mede melhora. Manter fatos, modelo e esforço; revisão em sessão separada com rótulos embaralhados continua julgamento de modelo, não voto humano ou conversão.
