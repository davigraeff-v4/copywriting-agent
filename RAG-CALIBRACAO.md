# Calibração do RAG lexical e semântico

Concluída em **13/10/2026**, mantendo os **239 documentos e 8.089 chunks** da ingestão integral. O modo padrão híbrido voltou a recuperar referências esperadas entre os três primeiros resultados nos 40 casos anteriores. O acerto no primeiro resultado passou de 32/40 para 37/40. Nos capítulos do PDF usados em desenvolvimento, o trecho principal correto passou de 8/12 para 11/12.

A avaliação adicional, com consultas novas congeladas antes dos ajustes, confirmou melhora na ordem: **25/32 para 30/32 referências esperadas no primeiro resultado**. Não houve melhora em todas as métricas; as perdas e os falsos positivos estão registrados abaixo. Nenhum arquivo de cliente ou fonte indexada foi alterado para obter esses resultados.

## O que causava a perda

A fusão anterior atribuía o mesmo peso a um resultado lexical forte e a um resultado semântico apenas acima do piso. Com constante RRF 40, a diferença entre posições próximas era pequena; resultados com dois sinais moderados podiam ultrapassar um encaixe específico. Empates dependiam da ordem dos identificadores.

Título, seção e tags eram concatenados ao corpo em um único campo lexical. Contexto repetido, proveniência e termos amplos entravam na comparação junto com o conteúdo. No componente semântico, o maior cosseno de uma passagem determinava o documento inteiro: fontes longas ofereciam muitas oportunidades de uma coincidência isolada. Além disso, escolher uma página diretamente entre chunks curtos podia perder informação distribuída pelo capítulo.

A auditoria anterior já distinguia presença do documento e acerto de página. Esta calibração preserva essa distinção: localizar o livro correto não certifica que o trecho destacado responde à pergunta.

## Mudanças implementadas

**Lexical por campo.** Corpo e contexto têm índices BM25 separados. O corpo recebe peso 1; título, seção e tags, 0,25. As estatísticas continuam calculadas após os filtros. A normalização de busca remove palavras funcionais em inglês e aproxima plurais simples, além de conservar a normalização de acentos. Isso altera apenas os termos de busca, nunca a redação original ou a copy.

A exigência de pelo menos dois termos em perguntas longas é conferida pela união dos campos. Assim, uma informação no corpo e outra no título podem sustentar o resultado. Proveniência e JSON recebem peso menor em perguntas de conteúdo; consultas explícitas sobre URL, hash, catálogo, licença ou proveniência recuperam esses trechos com peso normal. Nenhum desses conteúdos foi excluído.

**Dois canais semânticos.** Os 8.089 embeddings anteriores com título/seção permanecem vinculados aos chunks. Acrescentei **8.089 embeddings de contexto do corpo**, com janela ampliada dentro da mesma página/seção e limite de 120 tokens. Cabeçalhos recorrentes do PDF podem ser removidos desse canal auxiliar quando cabem na janela; continuam integralmente no texto e no canal anterior. Não se criam novas páginas ou fontes.

A combinação usa 80% do corpo e 20% do contexto em fichas/métodos; nos originais, 50% de cada. O documento é avaliado pelo melhor sinal e pelo apoio das três melhores seções distintas, reduzindo o efeito de um único pico. O piso do documento é 0,49; candidatos internos abaixo desse piso podem contribuir para a medição de apoio, sem se tornar documentos liberados automaticamente. Esses números são parâmetros de recuperação, não confiança factual.

**Fusão por perfil.** A constante RRF de documento passou para 8. Peso lexical 1; semântico 0,6 em fichas/métodos e 1,25 em originais. Fonte dedicada à rota recebe preferência moderada de 12%; original histórico com origem rastreável, 8%. Esses sinais organizam pertinência e rastreabilidade, sem criar aprovação humana, atualidade ou prova de cliente. Empates favorecem o sinal lexical antes do identificador.

**Capítulo/seção antes da página.** Uma etapa lexical sobre o texto completo da seção ou capítulo complementa os sinais dos chunks. O motor escolhe a seção e depois sua melhor passagem/página. As passagens complementares priorizam seções/capítulos diferentes. Isso ajuda quando a pergunta depende de informação distribuída entre páginas, mas também pode trocar diversidade de páginas por diversidade de capítulos; esse efeito aparece na validação nova.

**Filtros e integridade.** `--source`, `--page` e `--section` restringem os chunks antes da comparação lexical/semântica. Filtro sem conteúdo devolve vazio, sem ampliar a busca. O modo legado de metadados recusa esses filtros em vez de ignorá-los. Uma página pode ser lida integralmente com `read_rag_source.py`.

O canal novo mantém manifesto próprio com origem, hashes, modelo, versão, identidade/ordem de chunks, dimensão e tokens. Corrupção, incompatibilidade ou desatualização são detectadas. Sem o canal auxiliar válido, a consulta pode usar o canal anterior e informa `semantic_channel_warning`; não declara a calibração completa ativa. Sem o índice/motor principal válido, continua o fallback lexical explícito. A validação com `--body-required` exige os dois canais. Ambos usam somente o modelo local em cache.

## Como a calibração foi avaliada

Os 48 casos anteriores e os 24 casos de originais foram preservados por hash. Os 28 casos de desenvolvimento e os 24 de originais apoiaram os experimentos. Os 20 casos antes reservados são agora regressão histórica, pois já haviam sido examinados em trabalhos anteriores.

Antes de calibrar, criei **36 casos novos**: 32 positivos e quatro fora do assunto. Entre os positivos, 16 são fichas/métodos e 16 são originais; oito exigem capítulo/páginas do PDF. Consultas, alvos e páginas ficaram congelados. As previsões do motor anterior foram salvas sem inspecionar seus resultados durante os ajustes. A configuração e os arquivos de ranking foram congelados antes de avaliar e abrir as previsões novas. Nenhum ajuste foi feito depois para melhorar esses casos.

Os rótulos foram escritos pelo agente, com conferência das fontes/páginas, sem avaliação humana independente. Não foram ampliados os alvos para contar referências próximas como acerto. Os resultados medem recuperação nesta amostra; não medem preferência por copy ou conversão.

Foram executadas **540 comparações finais**, em 108 consultas: 240 nos casos anteriores, 144 nos originais e 156 na validação nova, incluindo motores isolados e busca restrita à fonte. Os arquivos por caso registram o hash do conjunto e do corpus.

## Resultados antes e depois

### Fichas e métodos: 40 casos positivos anteriores

| Motor | Primeiro resultado: antes → depois | Entre três: antes → depois |
|---|---:|---:|
| Lexical | 37/40 → 37/40 | 39/40 → 39/40 |
| Semântico | 22/40 → 27/40 | 29/40 → 29/40 |
| **Híbrido padrão** | **32/40 → 37/40** | **39/40 → 40/40** |

Na regressão histórica de 16 positivos, o MRR@5 híbrido passou de **0,9062 para 0,9688** e o nDCG@5, de **0,8914 para 0,9342**. Entre os oito casos negativos históricos, a abstenção híbrida/lexical passou de **8/8 para 7/8**; a semântica manteve 8/8. A normalização lexical aproximou palavras genéricas como “forma”/“formas” numa consulta de bioquímica e retornou referências de estrutura de texto. É um falso positivo registrado, não evidência de cobertura desse assunto.

### Originais: 24 casos anteriores

| Motor | Primeiro documento, busca global: antes → depois | Documento entre três: antes → depois |
|---|---:|---:|
| Lexical | 18/24 → 17/24 | 19/24 → 19/24 |
| Semântico | 21/24 → 22/24 | 24/24 → 24/24 |
| **Híbrido** | **20/24 → 21/24** | **23/24 → 24/24** |

Com a fonte conhecida e restrita, o híbrido continua encontrando o documento no primeiro resultado em **24/24**. Isso não é mérito de descoberta da fonte: avalia principalmente a localização interna depois que a fonte foi indicada.

Nos **12 casos de capítulo do PDF**, o híbrido passou de **8/12 para 11/12** capítulos/páginas corretos no trecho principal, tanto globalmente quanto com fonte restrita. Entre as três passagens, passou de **11/12 para 12/12** na busca global; com fonte restrita, manteve 12/12. Os seis casos de imagens mantiveram a localização em sua página única. O TXT sem paginação física não entra no denominador de página.

### Validação nova: 32 positivos, sem ajuste posterior

| Motor global | Primeiro resultado: antes → depois | Entre três: antes → depois | MRR@5: antes → depois |
|---|---:|---:|---:|
| Lexical | 22/32 → 18/32 | 22/32 → 23/32 | 0,6875 → 0,6302 |
| Semântico | 21/32 → 23/32 | 25/32 → 24/32 | 0,7135 → 0,7344 |
| **Híbrido** | **25/32 → 30/32** | **31/32 → 31/32** | **0,8656 → 0,9594** |

A melhora independente concentra-se na **ordenação do modo híbrido**, que permanece padrão. O lexical isolado perdeu primeiro resultado nessa amostra; o semântico isolado perdeu um caso entre três, embora tenha melhorado o primeiro resultado. O híbrido compensou essas diferenças. Não se afirma que ambos os motores isolados melhoraram em todas as métricas.

Nos oito capítulos novos do PDF, o primeiro capítulo correto passou de **3/8 para 5/8**. Entre as passagens complementares, caiu de **7/8 para 6/8**. Incluindo as quatro imagens, são **7/12 para 9/12** no trecho principal e **11/12 para 10/12** nas passagens. Há ganho de precisão do destaque principal e uma perda de cobertura complementar que continua aberta para investigação com novos casos.

O único positivo fora dos três primeiros no híbrido ficou no quinto resultado: a pergunta sobre organização de oportunidades comerciais esperava a ficha de Pipedrive, mas as primeiras referências tratavam de outras operações de negócio. Um anúncio de sanduíche ficou em segundo, atrás de outra referência do mesmo setor. Nos quatro negativos novos, a abstenção ficou igual: lexical 4/4; semântico e híbrido 3/4. O falso positivo trata de afinação de piano e recupera publicidade histórica relacionada a instrumentos, sem cobrir a instrução técnica solicitada.

Houve **zero violações de escopo/filtros e zero fallbacks** nas comparações finais. Não houve ajuste ou reescrita da validação nova após observar os erros.

## Testes, cobertura e preservação

- **139 testes aprovados**. Os 13 novos cobrem campos, plurais, consulta explícita de proveniência, pico semântico sem apoio, filtros antes da comparação, páginas inexistentes, integridade e corrupção do canal adicional, identidade privada falsa, escape de caminho e vetores com objetos/pickle.
- Validador do projeto, dos dois canais e auditoria de cobertura aprovados. **239 documentos, 8.089 chunks, 116 páginas do PDF e 100% do texto extraído/descrições cobertos**, sem retirar material para favorecer o ranking.
- São **16.178 vetores**, dois por chunk, de 384 dimensões. As 8.089 entradas de cada canal foram recontadas com o tokenizer real; máximo 120 tokens, sem truncamento.
- Consulta híbrida real em português recuperou o capítulo de amostras com ambos os canais ativos, em conferência com conexões de rede bloqueadas e zero tentativa de conexão.
- **338 arquivos privados do snapshot atual** permaneceram idênticos por SHA-256. As **240 fontes/aliases** e os conjuntos anteriores também ficaram idênticos. As 100 fichas e seus registros não foram reescritos.
- Zero documentos privados nos índices ou embeddings compartilhados. Nenhum dado de cliente foi enviado a provedor. Não houve commit, push ou publicação.

A cobertura continua sendo do texto extraído e das descrições, não de OCR perfeito ou compreensão integral de pixels. As 147 linhas de baixa confiança e as duas imagens sem texto latino reconhecível permanecem como limitações da ingestão anterior. Os testes de ranking não modificaram essas extrações nem certificam ausência universal de prompt injection; referências continuam dados sem autorização para executar ações.

## Uso e manutenção

```sh
python3 scripts/retrieve.py --query "amostras do produto e informações para experimentar" --route ads --client cliente --use original
python3 scripts/retrieve.py --query "letters headline attention" --route direct --client cliente --use original --source orig-94211e766522b503 --section "Chapter 19" --page 104
python3 scripts/read_rag_source.py --id orig-94211e766522b503 --page 104
python3 scripts/build_rag_index.py
python3 scripts/validate_rag.py --required --body-required
python3 scripts/audit_rag_coverage.py
python3 -m unittest discover -s tests -v
```

O builder atualiza o índice principal e o canal auxiliar. `scripts/rag_ranking.py` concentra os parâmetros de consulta; `rag_semantic_channel.py`, o encoder e a integridade do canal novo. Mudança de fonte ou encoder exige reconstrução antes de usar a calibração completa; o aviso de desatualização não deve ser ignorado.

Resultados e evidências em `.local/rag/calibration/`: `ranking-freeze.json`, `validation-freeze.json`, `development-final.json`, `regression-final.json`, `originals-final.json`, `fresh-validation-final.json`, `coverage-final.json`, `preservation-final.json`, `offline-validation.json` e `tests-final.txt`. O baseline anterior permanece em `baseline/`; os artefatos locais não entram no Git.

Próximo foco indicado pelos testes: abstenção lexical em perguntas com termos genéricos e objetos fora da cobertura; precisão lexical isolada em perguntas inéditas; diversidade complementar de capítulos em português sobre livros em inglês. Esses pontos precisam de novos casos e revisão humana, sem reutilizar esta validação como se continuasse inédita. A calibração atual do modo padrão, os testes e a preservação estão concluídos, com essas limitações declaradas.
