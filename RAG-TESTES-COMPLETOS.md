# Testes ampliados de RAG — THAMY IA

Avaliação de 13/10/2026. O híbrido teve **9,01/10 para recuperação de fontes**, com **202/214 acertos entre os três primeiros documentos**. A localização interna foi mais fraca: **5,37/10 por página** e **5,56/10 por seção** no primeiro resultado. Essas notas medem dimensões distintas. Não há uma nota geral que esconda a localização fraca nem uma nota de qualidade de copy.

Foram **250 casos principais e 948 execuções**, mais **16 casos de isolamento de formatação e 48 execuções**: **266 casos e 996 execuções dos motores**. Os 14 testes operacionais e os 142 testes automatizados são verificações separadas. Apenas avaliação e documentação foram adicionadas; o ranking não foi alterado.

## Como consultar os resultados

- [Painel de todos os exemplos](evals/retrieval/resultados/2026-10-13/painel.html): pesquisa, filtros e comparação de fontes, páginas, seções e trechos.
- [Planilha CSV com 996 linhas de avaliação](evals/retrieval/resultados/2026-10-13/notas-por-exemplo.csv): uma linha por caso, motor e escopo.
- [Resultados completos da rodada principal](evals/retrieval/resultados/2026-10-13/resultados-completos.json) e [testes de formatação](evals/retrieval/resultados/2026-10-13/formatacao-completa.json).

## Base e preservação

Base avaliada: **239 documentos, 8.089 chunks**, dois canais semânticos locais de 384 dimensões. Formatos: 135 Markdown, 1 PDF, 1 TXT, 99 imagens e 3 JSON. Entre os Markdown há 100 fichas de repertório. Os testes consultaram a base inteira elegível, respeitando rota e tipo de uso; não reduziram a base aos documentos esperados.

Os **239 arquivos-fonte**, **338 arquivos privados** em clientes, entregas e exemplos, **5 arquivos do motor**, **5 conjuntos de testes anteriores** e os apontadores dos índices permaneceram idênticos ao início. Inventário privado sem adições ou remoções. Os alvos dos dois novos conjuntos permaneceram iguais aos congelados antes de suas respectivas execuções. [Auditoria de preservação](evals/retrieval/resultados/2026-10-13/preservacao.json).

A auditoria confirmou **100% do texto extraído indexado**, sem lacunas nos caracteres não brancos. Isso não comprova OCR perfeito ou compreensão integral de elementos visuais. [Auditoria de cobertura](evals/retrieval/resultados/2026-10-13/cobertura.json).

## Critérios das notas

Os alvos, páginas e seções foram definidos antes das buscas. São cenários e rótulos elaborados pelo próprio agente, não julgamentos independentes de especialistas. Nenhum parâmetro do ranking foi ajustado com esta rodada. As métricas são diagnósticas, não uma garantia de desempenho em qualquer consulta.

- Recuperação da fonte: `10 × (0,6 × MRR@5 + 0,4 × Hit@3)`. MRR dá 1 para posição 1, 1/2 para posição 2, até 1/5 para posição 5; ausência recebe 0.
- Primeiro resultado e disponibilidade: `10 × Hit@1` e `10 × Hit@3`.
- Página/seção: `10 × proporção de consultas cujo primeiro resultado acerta simultaneamente a fonte e a página/seção esperada`.
- Complementos: mesma conferência em até três passagens de cada um dos três primeiros documentos. Medida auxiliar; não substitui a nota do primeiro resultado.
- Abstenção: `10 × proporção de respostas vazias em 20 consultas claramente fora do domínio`.
- Nota individual no painel/CSV: `10 / posição da fonte esperada`; ausência vale 0. Em consultas fora do domínio: 10 se vazio, 0 se retornar conteúdo. É diferente da fórmula agregada. Limites de evidência não recebem nota de relevância.
- Sem amostra aplicável, a dimensão aparece como N/A. Verificação técnica não é misturada à relevância.

## Comparação dos motores

| Métrica | Lexical | Semântico | Híbrido |
| --- | --- | --- | --- |
| Recuperação da fonte | 8,05 | 6,93 | 9,01 |
| Fonte no primeiro resultado | 7,24 | 6,50 | 7,99 |
| Fonte entre os três primeiros | 8,36 | 7,15 | 9,44 |
| Página certa no primeiro resultado | 3,70 | 5,93 | 5,37 |
| Seção certa no primeiro resultado | 3,33 | 5,56 | 5,56 |
| Abstenção fora do domínio | 8,50 | 10,00 | 8,50 |

Denominadores: **214 consultas positivas globais**; **54 com página rotulada** (42 PDF e 12 imagens); **54 com seção rotulada** (42 PDF e 12 TXT); **20 fora do domínio**. As 4 consultas sobre evidências inexistentes avaliam limites de autoridade, não relevância. Os 12 testes de seção com fonte indicada ficam apenas na avaliação assistida.

| Motor | Fonte 1ª | Fonte top 3 | Fonte top 5 | MRR@5 | Página 1ª | Seção 1ª | Vazio fora do domínio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Lexical | 72,43% | 83,64% | 86,92% | 0,78 | 37,04% | 33,33% | 85,00% |
| Semântico | 64,95% | 71,50% | 72,43% | 0,68 | 59,26% | 55,56% | 100,00% |
| Híbrido | 79,91% | 94,39% | 97,20% | 0,87 | 53,70% | 55,56% | 85,00% |

O híbrido trouxe a fonte esperada em 171/214 primeiras posições, 202/214 top 3 e 208/214 top 5. Página certa: 29/54 primeiras posições; seção certa: 30/54. Quando os complementos são considerados, sobe para 45/54 por página e 46/54 por seção. Aumentar a chance de encontrar o trecho em vários resultados não resolve sozinho a escolha do primeiro trecho.

## Notas por rota

| Rota | Consultas positivas | Lexical | Semântico | Híbrido | Híbrido top 3 |
| --- | --- | --- | --- | --- | --- |
| Anúncios | 115 | 7,05 | 7,86 | 8,79 | 93,91% |
| Landing pages | 58 | 8,98 | 4,84 | 8,92 | 93,10% |
| Orgânico | 18 | 9,44 | 6,11 | 9,36 | 94,44% |
| E-mail / WhatsApp | 23 | 9,57 | 8,26 | 10,00 | 100,00% |

As rotas têm conjuntos diferentes: anúncios inclui muitos capítulos e imagens; as amostras de orgânico e direta são menores. O 10 em direta significa 23/23 primeiros resultados nesta amostra, não excelência garantida em toda consulta de e-mail ou WhatsApp.

## Notas por tipo de cenário

| Cenário | Casos globais positivos | Lexical | Semântico | Híbrido | Página híbrida | Seção híbrida |
| --- | --- | --- | --- | --- | --- | --- |
| Métodos e orientação | 20 | 6,56 | 5,95 | 7,23 | N/A | N/A |
| Peças reais analisadas | 70 | 9,79 | 6,69 | 9,73 | N/A | N/A |
| Estrutura de formatos | 10 | 8,60 | 8,00 | 9,70 | N/A | N/A |
| Originais em imagem | 12 | 8,46 | 7,50 | 7,75 | 5,83 | N/A |
| Capítulos do PDF | 42 | 5,02 | 9,31 | 9,17 | 5,24 | 5,24 |
| Variações de escrita | 24 | 8,40 | 2,85 | 8,44 | N/A | N/A |
| Consultas curtas | 8 | 9,62 | 5,00 | 9,25 | N/A | N/A |
| Problemas de direção e revisão | 16 | 7,38 | 6,72 | 8,12 | N/A | N/A |
| Capítulos do livro TXT | 12 | 9,17 | 10,00 | 10,00 | N/A | 6,67 |

As 100 fichas de repertório têm um cenário cada: 20 métodos, 70 peças positivas e 10 estruturas. Há ainda 16 situações de direção/revisão; 42 consultas para os 21 capítulos do PDF em português e inglês; 12 consultas do TXT; 12 referências visuais; 24 variantes de escrita; 8 consultas curtas. Os 12 testes de seção conhecida, 20 negativos e 4 de autoridade completam os 250 casos principais.

Os bons resultados nas peças analisadas incluem consultas específicas próximas de seus casos de uso. Métodos genéricos e situações de direção apresentam mais ambiguidade entre documentos vizinhos. Uma fonte esperada ausente pode coexistir com referências úteis; a nota registra falha contra o alvo definido, não um julgamento automático de inutilidade de todos os retornos.

## Livros, idiomas e localização

| PDF / idioma | Casos | Fonte híbrida | Página/seção híbrida 1ª | Seção híbrida nos complementos |
| --- | --- | --- | --- | --- |
| PT | 21 | 8,62 | 3,81 | 76,19% |
| EN | 21 | 9,71 | 6,67 | 90,48% |

O PDF em inglês expõe uma lacuna de localização nas perguntas em português: capítulo/página corretos no primeiro resultado em **8/21** consultas PT, contra **14/21** EN. O lexical isolado acertou **0/21** páginas PT e **12/21** EN. O híbrido recupera o livro com frequência, mas nem sempre a passagem do capítulo pedido.

No TXT, o híbrido encontrou o livro na primeira posição em **12/12** casos e a seção correta em **8/12**. Não há paginação física no TXT; a referência válida é capítulo/seção/posição do texto. Nos 12 casos de imagem, a fonte esperada apareceu primeiro em **7/12**; todas as imagens usam página 1, portanto a nota de página de imagem acompanha a escolha da fonte e não mede compreensão visual.

## Recuperação com a fonte já indicada

| Métrica | Lexical | Semântico | Híbrido |
| --- | --- | --- | --- |
| Recuperação da fonte | 6,41 | 9,10 | 9,62 |
| Fonte no primeiro resultado | 6,41 | 9,10 | 9,62 |
| Fonte entre os três primeiros | 6,41 | 9,10 | 9,62 |
| Página certa no primeiro resultado | 4,63 | 6,11 | 6,67 |
| Seção certa no primeiro resultado | 3,79 | 6,06 | 6,36 |
| Abstenção fora do domínio | N/A | N/A | N/A |

São **78 consultas assistidas**: 66 aos originais e 12 a seções de fichas. O filtro restringe a busca às fontes esperadas antes do ranking. Esses resultados não demonstram capacidade de descobrir uma fonte sem indicação e não entram na nota global.

No híbrido, 75/78 retornam a fonte indicada; página correta no primeiro resultado em 36/54 e seção em 42/66. Nas 12 fichas com a seção Argumento e progressão como alvo, acertou 8/12 primeiras seções (6,67/10), contra 3/12 do lexical e 9/12 do semântico. Há melhora ao informar a fonte, mas a seleção interna ainda precisa evoluir. Um filtro válido sem passagem elegível pode produzir resposta vazia.

## Robustez a variações de escrita

A estabilidade abaixo mede quantos acertos top 3 da consulta original continuam acertando após a alteração. Denominador inclui apenas as consultas originalmente corretas; uma estabilidade 10 não significa que todas as consultas originais acertaram.

| Variação | Casos | Lexical | Semântico | Híbrido |
| --- | --- | --- | --- | --- |
| Sem acentos | 8 | 10,00 | 8,33 | 10,00 |
| Maiúsculas + pontuação | 8 | 10,00 | 0,00 | 8,75 |
| Erros leves de digitação | 8 | 7,50 | 5,00 | 7,50 |

O resultado em maiúsculas + pontuação motivou 16 casos adicionais, com os mesmos 8 alvos e duas alterações isoladas. Os resultados desta rodada adicional não alteram as notas dos 250 casos principais.

| Alteração isolada | Casos | Lexical | Semântico | Híbrido |
| --- | --- | --- | --- | --- |
| Apenas maiúsculas | 8 | 10,00 | 6,00 | 8,75 |
| Apenas pontuação | 8 | 10,00 | 10,00 | 10,00 |

Semântico: dos 5 acertos originais, manteve 3 com maiúsculas e os 5 com pontuação isolada. Híbrido: manteve 7/8 com maiúsculas e 8/8 com pontuação isolada. Na combinação, o semântico caiu para 0/5 e o híbrido manteve 7/8. Há sensibilidade nesta amostra; os testes não isolam todas as interações de tokenização/modelo.

## Exemplos verificáveis de acerto

### broad-014 — Métodos e orientação

Quero alinhar a informação do assunto, o complemento visível na caixa de entrada e o início do e-mail.

Fonte esperada e retornada: `rep-01-m14`. Primeira posição, nota individual 10,00. Página N/A; seção **Decisão de uso**.

## Decisão de uso  Usar quando a abertura de e-mail busca curiosidade, mas o corpo entrega outro assunto. A mensagem deve ser reconhecível na caixa de entrada e útil após a abertura. A coerência entre campos é mais relevante do que uma fórmula fixa d

### broad-021 — Peças reais analisadas

Quero uma referência de software de projetos que apresente a utilidade mostrando tarefas e organização dentro da própria ferramenta.

Fonte esperada e retornada: `rep-01-e01`. Primeira posição, nota individual 10,00. Página N/A; seção **Apresentação**.

# E01 | Basecamp: mostrar a tarefa dentro do produto  Tipo: exemplo. Rota principal: lp. Rotas compatíveis: lp. Estado: Curadoria pelo Codex para estudo. Validação editorial humana pendente; sem eficácia atribuída.  

### broad-126 — Capítulos do PDF

How does a headline attract the intended reader and select the people interested in the offer?

Fonte esperada e retornada: `orig-94211e766522b503`. Primeira posição, nota individual 10,00. Página 27; seção **Chapter 5: Headlines**.

interested people who, by their own volition, study  what we have to say.  The purpose of a headline is to pick out people you  can interest. You wish to talk to someone in a crowd.  So the first thing you say is, "Hey there, Bill Jones" to  get the 

## Exemplos verificáveis de falha

### broad-003 — Métodos e orientação

Tenho várias descobertas de pesquisa soltas. Como agrupá-las em uma tese que a página consiga demonstrar?

Esperado: rep-01-m03. Posição: ausente. Nota individual: 0,00.

- Retorno: `rep-01-m08`; página N/A; seção **Observação da fonte**. Trecho: ## Observação da fonte  Anna Bolton apresenta no tutorial um caso de conversão de respostas de pesquisa em temas, insights e copy de uma página de vendas. O processo inclui agrupar o material e aprese
- Retorno: `rotas-lp`; página N/A; seção **Apresentação**. Trecho: # Rota LP: construir uma decisão  Consumida pelas skills 02, 07, 08, 09, 11, 12 e 13. A página nasce do briefing e da informação disponível; templates históricos são referências de campos, sem ordem o

### broad-071 — Peças reais analisadas

Uma marca de panificação usa uma expressão conhecida com uma alteração visual. Como essa familiaridade serve ao anúncio?

Esperado: rep-02-a11. Posição: ausente. Nota individual: 0,00.

- Retorno: `rep-01-e19`; página N/A; seção **Recorte observado**. Trecho: ## Recorte observado  Trecho curto do original, preservado no idioma de origem:  > Real Beauty Sketches  A agência descreve uma campanha construída sobre diferenças entre a percepção da própria aparên
- Retorno: `rep-01-e22`; página N/A; seção **Limites de uso**. Trecho: ## Limites de uso  Análise do lançamento 2025, sem previsão sobre edições futuras. A rota ads é usada como repertório de campanha e expressão; não houve observação de um anúncio pago específico. Não t

### broad-107 — Problemas de direção e revisão

A redação usa frases picadas e promessas vagas. Preciso de critérios para retirar essa cadência artificial.

Esperado: vicios-ia-humanizacao, termos-a-evitar. Posição: ausente. Nota individual: 0,00.

- Retorno: `rep-01-m09`; página N/A; seção **Critério de revisão**. Trecho: ## Critério de revisão  Verifique se o título revela a informação prometida e se o texto seguinte a entrega. Clareza não significa retirar artigos e conectivos do português até criar uma frase truncad
- Retorno: `rep-01-m02`; página N/A; seção **Critério de revisão**. Trecho: ## Critério de revisão  A ficha de direção precisa conter o critério descoberto e a evidência do produto. Uma frase bonita retirada de uma avaliação não deve virar depoimento do cliente nem ser atribu

### broad-151 — Capítulos do PDF

Quero estudar a recomendação de apresentar sucesso e possibilidades, evitando ataques e imagens negativas.

Esperado: orig-94211e766522b503. Posição: ausente. Nota individual: 0,00.

- Retorno: `orig-44107d0390e1387f`; página 1; seção **Texto reconhecido na imagem**. Trecho: Encourage happy customers to leave reviews Strategies: • Provide free trials or demos to showcase your and testimonials. product's value. • Create a referral program with incentives for • Use retarget

### broad-186 — Fora do domínio

Escreva a solução de uma equação diferencial de Navier-Stokes para turbulência.

Esperado: nenhuma referência. Posição: ausente. Nota individual: 0,00.

- Retorno: `processo-de-copy`; página N/A; seção **Roadmap de 5 passos (versão direta, sem enrolação)**. Trecho: ## Roadmap de 5 passos (versão direta, sem enrolação)  1. Chame o leitor → 2. Nomeie a dor dele → 3. Mostre o que muda → 4. Apresente sua solução → 5. Diga o que fazer. "Escreva como um roteiro, não c
- Retorno: `banco-de-headlines`; página N/A; seção **Headline por nível de consciência**. Trecho: ## Headline por nível de consciência  - **Inconsciente:** situação, identidade ou tensão familiar; não apresentar solução complexa cedo demais. - **Consciente do problema:** nomear dor e consequência 

### broad-188 — Fora do domínio

Explique o algoritmo de multiplicação de matrizes usado em criptografia homomórfica.

Esperado: nenhuma referência. Posição: ausente. Nota individual: 0,00.

- Retorno: `orig-d61ccb22ed7b7bfc`; página 1; seção **Texto reconhecido na imagem**. Trecho: Como criar um prompt perteito Contexto → Comece dizendo quem voce "Sou nutricionista e preciso de → é, para quem será o conteúdo um texto para postar no e onde ele será usado. Instagram sobre alimenta

### broad-192 — Fora do domínio

Quero calcular cargas e dimensionar pilares de concreto para uma ponte ferroviária.

Esperado: nenhuma referência. Posição: ausente. Nota individual: 0,00.

- Retorno: `orig-a2beaa87c4484fc5`; página 1; seção **Texto reconhecido na imagem**. Trecho: 3 prompts para você fazer conteudo com Storytelling Storytelling de Experiência Pessoal: Crie um roteiro de carrossel com storyteling para o Instagram no nicho de [nicho]. O objetivo é inspirar e gera

A falha broad-003 devolveu referências próximas, como narrativa de LP, embora não o alvo específico pré-definido. Já os três exemplos fora do domínio ilustram falsos positivos mais claros: o motor usa associações superficiais com material de copy para perguntas técnicas sem resposta na base. São **3/20 falsos positivos** no híbrido e no lexical. O semântico isolado não teve falsos positivos nesses 20 casos; isso vale para esta amostra.

## Integridade, filtros e limites de evidência

- **142/142 testes automatizados passaram**, incluindo 3 testes da aritmética e dos denominadores do novo avaliador.
- **14/14 verificações operacionais passaram**: filtros inválidos, fonte desconhecida, rota/uso incompatível, tentativa de caminho privado, fonte+página+seção, opção não suportada e consulta com comando textual sem execução.
- Nas **996 execuções**, não houve violações registradas de escopo, inconsistências entre trechos/posições/fontes ou erros nos sinalizadores de autoridade; sem fallback e sem alerta de canal semântico.
- Os validadores do projeto, do RAG e da cobertura passaram. Os 239 documentos indexados são compartilhados, com zero documentos privados no índice público.
- As 4 consultas sobre fatos de cliente inexistente, performance, estoque e aprovação conferem os sinalizadores que distinguem referência externa de evidência do cliente. Não testam uma resposta final produzida por LLM.
- A nota técnica de filtros é **10,00** (14/14), separada das notas de relevância. A consulta com comando não foi executada; isso não certifica resistência universal a prompt injection nem ausência de vírus em toda a máquina. Nenhum download foi realizado nesta rodada.

## Tempos observados

| Motor | Mediana (ms) | P95 (ms) | Máximo (ms) |
| --- | --- | --- | --- |
| Lexical | 235.29 | 554.41 | 1635.12 |
| Semântico | 1244.38 | 3655.03 | 11378.66 |
| Híbrido | 272.45 | 647.04 | 1939.71 |

Os lotes rodaram em processos concorrentes; o semântico computou embeddings de consulta antes do híbrido, que reutilizou cache. Portanto esses tempos documentam a execução, mas **não são uma comparação controlada de velocidade dos motores**. Existem avisos locais de dependência Requests e pooling do FastEmbed nos logs; os índices e canais foram validados com a versão vigente.

## Prioridades indicadas pelos testes

1. **Localização por capítulo/página em português**: investigar tradução semântica entre consulta PT e livros EN, representações de seção e seleção da passagem. Manter os 239 documentos e comparar primeiro resultado e complementos.
2. **Estabilidade da consulta semântica**: avaliar normalização de caixa/pontuação e erros leves de digitação, sem degradar siglas, nomes e números. Esta rodada não aplica a normalização.
3. **Recusa de consultas sem apoio na base**: reduzir os 3/20 falsos positivos do híbrido com critérios de suficiência/consistência entre canais, preservando recall de perguntas curtas relevantes.
4. **Escolha de métodos e exemplos visuais**: revisar casos ambíguos com rótulos de múltiplas referências pertinentes e avaliação humana dos retornos; verificar descrições/OCR das imagens com erro de fonte.
5. **Validar o uso na escrita**: testar separadamente se as passagens recuperadas sustentam uma direção específica e uma copy melhor. A presente rodada avalia recuperação, não produção de copy ou performance comercial.

O próximo ajuste deve usar um conjunto de desenvolvimento separado. Congelar estes resultados como referência e acrescentar nova avaliação humana e casos não vistos antes da próxima calibração. Nenhuma das otimizações acima foi implementada nesta rodada.

## Reprodução e evidência

Fixture principal: `evals/retrieval/broad-suite-v1.json`, SHA-256 `49583fab15ac21b181174693745e887b7ffeae83f3ab04f9106fc4e02661b554`.

Base: `b68b7cc0bf7f87c391f13a75ec510da4fda5f9abbb511bb5d5f1dceeadc18f35`. Geração do índice: `b68b7cc0bf7f87c3-c6bb0a7f`.

A busca foi feita nos três motores com até 5 documentos e parâmetros vigentes. O script `scripts/eval_rag_broad.py` executa a avaliação, permite os lotes catalog/originals/stress e calcula as mesmas métricas, sem alterar o motor. A fixture adicional é `evals/retrieval/formatting-probes-v1.json`.

Os JSON preservam perguntas, alvos, ranking, notas, páginas, seções, hashes, sinalizadores, tempos e trechos. Os trechos exibidos são limitados a 380 caracteres; as fontes completas permanecem no projeto. O painel/CSV incluem 996 linhas, correspondentes às execuções principais e adicionais, com os escopos separados.
