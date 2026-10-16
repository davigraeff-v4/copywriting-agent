# Implantação do RAG lexical e semântico da THAMY IA

Este relatório registra a implantação inicial com 132 documentos. A expansão integral dos originais e as métricas atuais estão em [INGESTAO-RELATORIO.md](INGESTAO-RELATORIO.md).

Concluída em **13/10/2026**, no projeto local. A consulta padrão do agente agora combina recuperação pelo conteúdo e pelo significado, com fallback lexical, escopo público e localizadores de origem.

## O que foi implementado

**132 documentos selecionados**, com as 100 fichas dos dois lotes e 32 documentos de metodologia/rotas. Foram gerados **1.117 chunks e embeddings de 384 dimensões**. Os índices existentes do Agent Tráfego permaneceram naquele projeto, e seus arquivos foram preservados.

A estrutura por seção H2 foi adaptada do builder de conhecimento localizado no checkout de performance-ads-ia do acervo local. O motor FastEmbed 0.8.0 e os pesos MiniLM já estavam instalados/em cache na máquina. A THAMY tem configuração e índice próprios, adequados a copy, sem carregar contas ou clientes de tráfego.

A inspeção do tokenizer mostrou limite de **128 tokens**. A janela de 180 palavras do padrão anterior podia excedê-lo. O novo corte limita a entrada a **120 tokens**, já incluindo título, seção e tokens especiais, com sobreposição de oito palavras dentro da mesma seção. Todos os 1117 trechos foram conferidos com o tokenizer real; **zero trechos truncados**. Proveniência repetitiva fica nos metadados, enquanto limites editoriais permanecem consultáveis.

O BM25 busca palavras no conteúdo dos chunks e metadados. A busca semântica usa cosseno de vetores locais. A fusão RRF combina posições por documento; vários chunks da mesma ficha não ocupam várias vagas. Rota e uso são filtrados antes do ranking. O resultado traz trecho, seção, caminho, posição no arquivo, hash, origem e limites de autoridade; o agente precisa ler a ficha inteira.

## Qualidade da recuperação

As consultas e seus alvos foram escritos pelo agente antes da comparação. Há **24 consultas positivas e quatro negativas de desenvolvimento**. Depois de ajustar somente em desenvolvimento, os parâmetros foram congelados e aplicados a **16 positivas e quatro negativas reservadas**. São consultas sintéticas, com alvos pendentes de revisão humana; a reserva reduz ajuste aos casos, mas não constitui avaliação humana cega independente.

### Desenvolvimento: 24 positivas e quatro negativas

| Motor | Acerto no 1º | Acerto nos 3 primeiros | MRR@5 | Sem sugestão fora do assunto |
|---|---:|---:|---:|---:|
| Anterior: metadados, 108 documentos | 58.33% | 79.17% | 0.6771 | 25% |
| Metadados, mesmos 132 documentos | 58.33% | 79.17% | 0.6667 | 25% |
| BM25 no conteúdo | 91.67% | 95.83% | 0.9458 | 100% |
| Semântico isolado | 54.17% | 83.33% | 0.6840 | 100% |
| Híbrido BM25 + semântico | 95.83% | 100.00% | 0.9792 | 100% |

### Validação reservada: 16 positivas e quatro negativas

| Motor | Acerto no 1º | Acerto nos 3 primeiros | MRR@5 | Sem sugestão fora do assunto |
|---|---:|---:|---:|---:|
| Anterior: metadados, 108 documentos | 56.25% | 68.75% | 0.6250 | 25% |
| Metadados, mesmos 132 documentos | 56.25% | 68.75% | 0.6250 | 25% |
| BM25 no conteúdo | 93.75% | 100.00% | 0.9583 | 100% |
| Semântico isolado | 81.25% | 87.50% | 0.8438 | 100% |
| Híbrido BM25 + semântico | 93.75% | 100.00% | 0.9583 | 100% |

Acerto nos três primeiros significa encontrar ao menos uma referência rotulada como pertinente entre três documentos retornados. MRR@5 premia aparecer mais cedo. A coluna de abstenção usa somente as quatro consultas negativas de cada conjunto, fora de copy. Os dois comparadores de metadados separam ampliação de cobertura e mudança do motor.

No conjunto combinado, a busca anterior acertou **30/40** consultas positivas entre os três primeiros; BM25, **39/40**; híbrido, **40/40**. A híbrida acertou **38/40** no primeiro resultado. As oito consultas negativas ficaram sem sugestões na busca nova. Houve **zero violações de filtros** e **zero fallbacks** nas execuções lexical/semântica/híbrida do comparativo final.

O semântico isolado ficou abaixo do lexical e da fusão, por isso o padrão usa híbrido com fallback BM25. Há uma troca mensurável: nDCG@5 na validação foi **0.9325 no BM25** e **0.9204 no híbrido**. O híbrido não melhorou todas as métricas, embora tenha recuperado no desenvolvimento um caso que ficou fora dos três primeiros no lexical. Não houve reescrita de consultas, alvos ou ajuste de piso com base nos erros da validação reservada.

Resultados por consulta, rota e motor ficam em `.local/rag/development-report.json` e `.local/rag/validation-report.json`. Resumo reproduzível, hashes e parâmetros em `evals/retrieval/baseline.json`. Os casos estão em `evals/retrieval/`; essa pasta nunca é indexada.

## Testes e preservação

- **107 testes aprovados**, incluindo 24 regressões novas sobre chunks, escopo, integridade, filtros, conteúdo externo e compatibilidade.
- Validador geral e validador de RAG aprovados. Fonte, metadados, artefatos, versão e orçamento de tokens são conferidos.
- **332 arquivos privados preservados por SHA-256**, sem alteração ou remoção. As 100 fichas, catálogo e registros de fontes também permaneceram idênticos.
- **758 arquivos do Agent Tráfego preservados por SHA-256**, sem alteração ou remoção.
- Zero documentos privados no índice. Não foram gerados embeddings de clientes nem enviados seus dados a um provedor.
- Consulta semântica real aprovada com conexões de rede bloqueadas durante a conferência. O comando padrão também retornou a referência de instalação adequada, em modo híbrido real.
- Testes bloquearam caminhos privados marcados como globais, propriedade falsa, symlink, escape, avaliação, fonte sinalizada, origem alterada, payload de chunk manipulado e artefato corrompido. Índice desatualizado, ausente ou motor incompatível degrada explicitamente para lexical.

A detecção técnica não certifica toda possível injeção ou qualidade factual. A defesa de uso mantém trechos como dados externos, sem autoridade para alterar regras, executar comandos, revelar informações ou transferir claims entre marcas. Aprovação humana, publicação e performance seguem estados separados.

## Funcionamento e manutenção

Artefatos derivados estão em `.local/rag/index/`, fora do Git, com geração atual indicada por `current.json`. O manifest registra hashes de fontes, chunking, arquivos, pesos/tokenizer, versão, dimensão e limites. Vetores são numéricos e carregados sem pickle. A troca de geração é atômica, preservando as anteriores.

```sh
python3 scripts/retrieve.py --query "como transformar função técnica em uma situação reconhecível" --route ads --client cliente --use positive
python3 scripts/retrieve.py --query "tese e progressão entre títulos" --route lp --client cliente --use guidance --engine lexical
python3 scripts/build_rag_index.py
python3 scripts/validate_rag.py --required
python3 scripts/validate_project.py
python3 -m unittest discover -s tests -v
python3 scripts/eval_rag.py --fixture evals/retrieval/development.json --out .local/rag/development-report.json
python3 scripts/eval_rag.py --fixture evals/retrieval/validation.json --out .local/rag/validation-report.json
```

O motor usa somente o modelo já em cache; não instala bibliotecas ou baixa pesos automaticamente. `requirements-rag.txt` registra as dependências opcionais. Sem elas, o BM25 e os verificadores objetivos continuam funcionando. Índices explícitos via `--index` preservam o modo de metadados e o escopo indicado, sem acrescentar o corpus público ou indexar clientes.

A calibração depende do modelo, corpus e tokenizer atuais. Ao ampliar a base ou mudar o motor, reconstruir o índice e repetir a comparação, mantendo conjuntos e rótulos anteriores como regressões. Consultas semânticas longas são recusadas e o fallback fica visível. Consultas curtas ou ambíguas ainda podem recuperar referências inadequadas; ler limites e selecionar por julgamento continua necessário.

## Limite desta entrega

Está implementado e testado o acesso a referências pertinentes. Esse resultado **não comprova melhora das copies produzidas, preferência humana ou conversão**. O próximo teste editorial é comparar novas saídas com o mesmo briefing, fatos e modelo, avaliando argumento, voz, progressão e esforço de edição. O protocolo existente de avaliação editorial permanece válido.

## Referências técnicas

[Documentação do FastEmbed](https://qdrant.github.io/fastembed/) e [modelo multilíngue MiniLM](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2). O limite de 128 tokens informado aqui foi confirmado na instalação local; não presumido a partir de outra variante do modelo.

[Protocolo de recuperação do agente](recuperacao-contexto.md).
