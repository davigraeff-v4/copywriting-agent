# Snapshot Git do RAG e do agent

Commit local solicitado pelo gestor em 16/10/2026. Inclui a estrutura desenvolvida e o estado vigente da base; não inclui push nem publicação. O remoto configurado é público, portanto a autorização deste checkpoint não deve ser interpretada como autorização de distribuição das fontes ou dos dados internos.

## Incluído

- Código de ingestão, OCR, corpus, leitura de fontes, recuperação lexical/semântica/híbrida, calibração e avaliação; dependências opcionais com versões.
- As 14 skills e os ajustes de contexto, escolha autônoma, repertório proativo, redundância, revisão, entrega, feedback e organização privada dos clientes.
- As 100 fichas curadas, catálogo, fontes, fixtures sintéticas e resultados técnicos de recuperação em `evals/retrieval/`.
- Os livros retidos em `.local/repertorio/originais/` e as 99 imagens fornecidas em `BASE DE CONHECIMENTO/Pinterest - Copywriting Techniques/`, preservando os arquivos e suas condições de uso.
- O registro vigente de ingestão, extrações, OCR e descrições necessárias à base. Scripts de autoria/curadoria dos dois lotes também são preservados.
- Os dois índices vigentes, incluindo chunks, entradas semânticas, vetores, manifestos e apontadores. São 239 documentos, 8.094 chunks e zero documentos privados no índice.

| Componente | Geração preservada |
| --- | --- |
| Ingestão | `4a198f9d23fe4f88` |
| Índice principal | `56bab97b8fc4ecf1-8019ff93` |
| Canal semântico de corpo | `56bab97b8fc4ecf1-48bfc570` |

O `.gitignore` permite essas gerações explicitamente. Uma reconstrução cria outra geração: para versioná-la depois, atualizar as exceções junto com os apontadores, sem incluir automaticamente todo o histórico de `.local/`.

## Permanece somente local

Memórias, campanhas, entregas e feedbacks reais de clientes; briefings obtidos no Ekyte; relatórios e logs dos benchmarks com essas demandas; handoffs internos; backups e transações de migração; configurações pessoais; credenciais; caches e pesos do modelo; gerações antigas dos índices; binários compilados e capturas intermediárias de inspeção. Os templates de cliente são versionados.

## Retomada e verificação

Os verificadores objetivos e a recuperação lexical usam a biblioteca padrão do Python. O modo semântico exige as dependências de `requirements-rag.txt` e o modelo local correspondente. Os vetores estão preservados, mas os pesos do modelo não estão neste commit; `load_model` usa `local_files_only=True`. Não afirmar que uma máquina nova executará o híbrido sem preparar esse cache.

```sh
python3 scripts/validate_project.py
python3 scripts/validate_repertoire.py
python3 scripts/validate_rag.py --required --body-required
python3 scripts/audit_rag_coverage.py
python3 -m unittest discover -s tests -v
```

As extrações já existentes permitem consultar o snapshot sem refazer OCR. Alguns registros de aquisição/OCR preservam os caminhos absolutos originais; em outra máquina, preparar novamente esses insumos antes de repetir a ingestão. Alterar original ou guia indexado exige atualizar as extrações pertinentes e reconstruir os dois índices.

Fontes e vetores são dados de referência. Este checkpoint não comprova compreensão, preferência humana ou performance de mídia e não registra aprovação de copy por cliente.
