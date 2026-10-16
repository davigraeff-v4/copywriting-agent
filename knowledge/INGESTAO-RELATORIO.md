# Ingestão integral do acervo local no RAG

Este documento preserva o resultado da ingestão e a avaliação anterior à calibração. A ordenação atual e a comparação antes/depois estão em [RAG-CALIBRACAO.md](../RAG-CALIBRACAO.md).

Concluída em **13/10/2026**. O índice compartilhado reúne **239 documentos, 8.089 chunks e 8.089 embeddings locais de 384 dimensões**. Todas as 100 fichas curadas e todos os originais de conteúdo disponíveis nas coleções de conhecimento estão representados. As 116 páginas do PDF foram ingeridas, com vínculo à página física e ao capítulo. Os arquivos dos clientes foram preservados e permanecem fora desse índice compartilhado.

## Conteúdo efetivamente indexado

| Conteúdo | Documentos | Tratamento |
|---|---:|---|
| Fichas curadas dos dois lotes | 100 | Markdown integral, títulos, introdução, análise, limites e proveniência |
| Método e contexto locais | 35 | Markdown integral, segmentos por seção |
| Scientific Advertising, edição digital disponível | 1 | PDF completo: 116 páginas, 21 capítulos e apêndice da edição |
| A History of Advertising, Henry Sampson | 1 | TXT completo: 247.423 palavras, capítulos e localizadores de texto |
| Imagens locais do acervo | 99 | 72 JPG, 20 PNG e 7 WebP: OCR, descrição visual e ligação ao original |
| Índices e registros de conhecimento | 3 | JSON integral, com extração validada |
| **Total** | **239** | **135 Markdown, 1 PDF, 1 TXT, 99 imagens e 3 JSON** |

O TXT de Scientific Advertising foi preservado como **extração alternativa ligada ao PDF**, sem contar duas vezes o mesmo livro. Três cópias idênticas usadas na preparação dos lotes também foram identificadas por hash e preservadas sem duplicar os documentos. As duas duplas de imagens visualmente equivalentes têm ambos os arquivos/extrações preservados, mas compartilham grupo de ranking para não consumir vagas repetidas na busca.

README de navegação, relatórios gerados, manifesto auxiliar de proveniência, `.DS_Store` e prévia de capa têm sua função registrada no inventário; não são tratados como repertório de copy. Scripts, logs, avaliações e baselines de preparação não foram promovidos a fontes de conteúdo. O inventário não deixou arquivo de conteúdo disponível sem classificação nas três coleções autorizadas.

**Limite de disponibilidade:** os lotes têm 90 fontes externas rastreáveis. As fichas e links de todas essas fontes estão indexados; isso não significa que os arquivos integrais de todos esses artigos/páginas tenham sido conservados localmente. Originais externos não disponíveis não foram declarados ingeridos. Livros ou cursos apenas citados no apêndice do PDF também não fazem parte do seu conteúdo integral.

## Extração, páginas e leitura completa

Scientific Advertising foi extraído com pypdf por página, conservando cabeçalhos, rodapés e texto de todas as páginas. Títulos de capítulos continuam ligados às páginas seguintes. As páginas 115–116 foram identificadas como apêndice comercial da edição digital, sem atribuir seu catálogo à metodologia original de 1923. Retratos e composição da capa/última página receberam descrições visuais separadas e localizadas.

Todas as 116 páginas foram renderizadas e examinadas em folhas de contato, com inspeção individual da capa e última página. Uma leitura adicional por OCR foi comparada ao texto nativo de cada página. A menor proporção de palavras distintas do texto nativo encontradas no OCR foi **95,1%**; a média por página foi **99,932%**. Na comparação inversa, o mínimo foi **97,75%** e a média, **99,968%**. Essa comparação verifica concordância lexical, sem comprovar ordem perfeita, pontuação ou fidelidade visual absoluta.

O TXT de Henry Sampson foi integralmente segmentado por cabeçalho de capítulo, incluindo preâmbulo e material final. Como o arquivo não oferece paginação física confiável, seu localizador utiliza capítulo, segmento, caracteres e linhas. Não foram inventadas páginas.

Nas 99 imagens, o OCR é local pelo Apple Vision. Arquivos pequenos foram ampliados; imagens muito altas receberam leitura em faixas sobrepostas. A nova passada no cartaz de modelos de negócio aumentou a extração de 13 para 563 linhas reconhecidas. O conjunto final tem **4.673 linhas de OCR**, das quais **147 apresentam confiança inferior a 0,65**. As caixas de texto são normalizadas em relação à imagem original e ligadas aos intervalos da extração. Cada imagem também tem descrição visual autoral, feita após inspeção de todas as folhas de contato.

Duas imagens não têm texto latino reconhecível: uma fotografia de anel sem texto e outra com inscrição parcialmente oculta. Elas estão indexadas pela descrição visual, com os pixels originais preservados. A inscrição não recebeu transcrição inventada. Cartazes densos, lettering e texto pequeno podem conservar erros de OCR; a baixa confiança e o caminho do original permanecem acessíveis para conferência.

Embeddings das imagens representam o **OCR e a descrição textual**, não vetores visuais dos pixels. Um resultado limitado não substitui a leitura da referência completa. `read_rag_source.py` devolve a página ou seção inteira por padrão e recusa filtros inexistentes, sem escolher outro documento em seu lugar.

## Chunks, embeddings e recuperação

Cada chunk contém vínculo ao documento e ao segmento pai, caminho original, hash, página/capítulo quando disponíveis, seção e posições de caracteres/linhas. As imagens mantêm coordenadas e confiança por linha no registro de extração; o resultado principal expõe as caixas que intersectam seu trecho.

O modelo local já instalado é `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, com FastEmbed 0.8.0 e 384 dimensões. O tokenizer real aceita 128 tokens; o corte utiliza **até 120 tokens**, incluindo título, seção e tokens especiais. Todos os **8.089 inputs foram recontados com o tokenizer sem truncamento: zero excederam o orçamento**. A sobreposição é de oito palavras dentro da mesma página/seção; uma sequência longa sem espaços pode ser cortada por caracteres, sem desaparecer do índice.

BM25, busca semântica e fusão RRF estão disponíveis. Rota, uso e fonte são filtrados antes da recuperação. As estatísticas lexicais também são calculadas dentro do conjunto permitido: um livro excluído pelo filtro não altera a frequência das palavras de uma consulta a fichas. A fusão por documento evita que livros longos ocupem todas as vagas. A seleção de passagem combina sinais dentro do documento e devolve **até três passagens de páginas/seções diferentes**, além do contexto do trecho principal e da indicação de truncamento.

Os originais usam `--use original`; as fichas mantêm `positive`, `guidance` e `structure`. `--source ID` permite aprofundar em uma fonte conhecida. Autoridade histórica, aprovação humana, origem sintética, performance e evidência de cliente permanecem estados separados. Um original histórico ou uma imagem sem origem confirmada não se torna exemplo aprovado apenas por ser recuperado.

A atualização reaproveita embeddings apenas quando o texto de entrada é idêntico e modelo, versão, pesos/configuração e artefatos conferidos também coincidem. Entradas novas são calculadas localmente. Gerações anteriores são preservadas, com troca atômica do apontador atual. Divergência do original, alias, extração ou índice é recusada ou gera fallback lexical explícito, conforme a etapa.

## Auditoria de cobertura

A auditoria compara a união dos intervalos dos chunks com o texto completo de cada extração, verificando também as páginas presentes. Resultado: **100% dos 1.979.774 caracteres não brancos extraídos/descritos estão cobertos**, em todos os 239 documentos. Todas as **116 páginas físicas** do PDF têm chunks e embeddings. Não há introdução, seção de proveniência ou apêndice retirados para aumentar esse percentual.

**Esse 100% é cobertura do texto extraído e das descrições. Não certifica OCR perfeito, interpretação integral dos elementos visuais ou que o agente leia toda a biblioteca em cada tarefa.** A produção continua recuperando referências pertinentes e lendo as páginas/seções selecionadas.

## Qualidade da recuperação

Foram executados **72 casos de consulta**: os 48 anteriores, congelados como regressão, e 24 novos sobre originais. Há comparação de cinco motores nos casos anteriores e três motores com/sem restrição de fonte nos originais, totalizando 384 execuções. Consultas e alvos são rotulados pelo agente, sem validação humana independente. Os 20 casos antes reservados agora também servem como regressão histórica; não são uma nova avaliação cega.

### Regressão das fichas e métodos

| Motor | Desenvolvimento: alvo entre 3, 24 casos positivos | Validação histórica: alvo entre 3, 16 positivos | Combinado |
|---|---:|---:|---:|
| Metadados anteriores | 19/24 | 11/16 | 30/40 |
| BM25 no corpus atual | 23/24 | 16/16 | 39/40 |
| Semântico isolado | 15/24 | 14/16 | 29/40 |
| Híbrido no corpus atual | 23/24 | 16/16 | 39/40 |

As oito consultas fora do assunto ficaram sem resultado em BM25, semântico e híbrido. Houve zero violações de rota/uso e zero fallbacks nas execuções comparadas.

**A ampliação não melhorou todas as métricas.** Na implantação anterior, o híbrido tinha 40/40 acertos entre três resultados e 38/40 no primeiro. Agora são **39/40 entre três e 32/40 no primeiro**. Na validação histórica, o MRR@5 do híbrido passou de 0,9583 para 0,9062; o BM25 manteve 0,9583. O semântico isolado perdeu precisão nos métodos/fichas após a inclusão integral de introduções, contexto e proveniência. Esses dados ficam registrados para a próxima calibração; a cobertura integral não foi reduzida para esconder a perda.

### Recuperação dos originais

| Motor | Fonte entre 3 resultados na busca global, 24 casos | Fonte no primeiro resultado com fonte restrita, 24 casos |
|---|---:|---:|
| BM25 | 19/24 | 19/24 |
| Semântico | 24/24 | 24/24 |
| Híbrido | 23/24 | 24/24 |

Nos **12 casos com capítulo/páginas esperados do PDF**, o híbrido apontou a página/capítulo correto como trecho principal em **8/12**. Com até três passagens e fonte restrita, recuperou a página e capítulo esperados em **12/12**. Na busca global, foram 11/12 nas passagens complementares. Os seis casos de imagens também recuperaram sua página única quando a fonte estava restrita. O TXT histórico não foi contado como acerto de página: não tem paginação física.

A busca semântica contribui principalmente na passagem entre português e originais em inglês. Ainda é possível recuperar o livro correto e destacar outra parte dele. Por isso o fluxo registra passagens complementares, oferece restrição de fonte e exige leitura da página/seção. Acerto nessa amostra não garante acerto universal nem melhora editorial/conversão.

## Testes, segurança e preservação

- **126 testes aprovados**, incluindo cobertura, arquivos longos, capítulos/páginas, OCR e descrições, alias, localização adulterada, escopo lexical, corrupção, filtros, recursos ativos de PDF, HTML, macros/entidades XML e reúso seguro de embeddings.
- Validação do projeto, integridade do RAG e auditoria de cobertura aprovadas. Vetores são numéricos, com 384 dimensões, normalizados e carregados sem pickle.
- Consulta híbrida/semântica real aprovada com conexões de rede bloqueadas, sem tentativa de conexão. Leitura integral de página confirmada, sem truncamento; página inexistente recusada.
- **436 arquivos do snapshot preservados por SHA-256**, incluindo **332 arquivos privados**, originais e imagens. Nenhum foi modificado ou removido. As 100 fichas e seus catálogos/fontes também permanecem idênticos.
- Zero documentos de clientes no índice compartilhado. Copies, feedbacks, perfis e históricos continuam em suas pastas, sem upload e sem transferência de fatos entre clientes.
- Nenhuma instrução ou código das fontes foi executado. PDF com ações ativas/anexos, arquivo com macro/executável, expansão excessiva ou caminho fora das coleções autorizadas é recusado. Trechos externos continuam tratados como dados, sem autoridade para mudar regras ou obter credenciais. Não foi baixado software remoto neste processamento.

Inspeção de recursos ativos e busca por sinais de instrução maliciosa são controles limitados; não foram declarados uma certificação antivírus ou detecção universal de prompt injection. Novos DOCX/PPTX/XLSX/EPUB/HTML/CSV têm adaptadores, mas o acervo disponível nesta execução não continha esses formatos; sua fidelidade integral precisa ser verificada quando houver arquivos reais.

## Onde ficam os resultados

- `knowledge/INGESTAO-RELATORIO.md`: este relatório; o anterior permanece em `RAG-RELATORIO.md` como histórico.
- `knowledge/recuperacao-contexto.md`: protocolo atualizado de seleção, leitura e manutenção; AGENTS, CLAUDE e skill 07 foram conectados a esse fluxo.
- `.local/rag/ingestion/current.json`: geração atual de extrações e registro de originais.
- `.local/rag/index/current.json`: geração atual de chunks, embeddings e manifesto de integridade.
- `.local/rag/full-ingestion/source-inventory.json`, `coverage.json`, `preservation-final.json`, `offline-validation.json`: inventário, cobertura, preservação e conferência offline.
- `.local/rag/full-ingestion/curated-development.json`, `curated-validation.json`, `original-recovery-final.json`, `tests-final.txt`: resultados por caso e testes.
- `.local/rag/full-ingestion/ocr*.jsonl`, `pdf-ocr.jsonl`, `pdf-crosscheck.json`, `visual-descriptions.json`: leituras e evidências locais de extração.

Os arquivos derivados permanecem locais e fora do Git. Não houve commit, push, publicação ou alteração no Agent Tráfego. Próxima decisão técnica sugerida pelos testes: calibrar a ordenação entre fichas/métodos e originais com novos casos independentes e revisão humana, preservando os conjuntos atuais como regressão. A ingestão integral disponível e sua auditoria estão concluídas.
