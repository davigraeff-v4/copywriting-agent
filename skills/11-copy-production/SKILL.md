---
name: 11-copy-production
description: "Escreve copy diretamente no formato solicitado usando argumento, voz e evidências selecionadas."
---

# 11-copy-production

## Dados necessários

Ler o SKILL.md integralmente. Modos e checkpoints seguem `CONTRATO-OPERACIONAL-MODOS.md`; caminhos relativos à raiz do projeto.

- `knowledge/pacote-contexto.md`
- `knowledge/politica-editorial.md`
- `knowledge/vicios-ia-humanizacao.md`
- `quality/FORMATO-ENTREGA.md`
- `knowledge/narrativa-lp.md` (somente rota LP)

## Execução e auto-validação

Antes da primeira linha, ler integralmente e novamente `knowledge/vicios-ia-humanizacao.md` com recibo de fase production. Confirmar índice/metodologia/rota lidos e direção autorizada conforme modo; consultar HARD CONSTRAINTS e exemplos curados pertinentes.

Escrever em conjunto com 12 no formato final em todos os modos. Usar somente o pacote pertinente; não reler todos os bancos de fórmulas. Manter a pergunta do comprador ou valor da pauta como eixo. Informação técnica pode permanecer quando ajuda; não inventar benefício.

Em LP, escrever primeiro todas as headlines, revisar sua sequência e somente depois desenvolver o corpo. Cada dobra recebe uma ideia principal; listas de perfis e características não substituem narrativa. Depois do primeiro rascunho, fazer uma etapa separada de compressão, contar palavras por dobra e no total e aplicar o orçamento de `knowledge/narrativa-lp.md`, salvo necessidade registrada.

Separar campos publicáveis e notas internas em delivery.json. Hipóteses e pendências ficam no contexto, não na copy. Anotar claims com trecho exato e fatos. Cada peça/dobra precisa entregar informação, não apenas variar expressão.

Revisar primeiro o argumento: atende briefing, resolve barreira, tem evidência e desenvolve a mesma tese entre as dobras? Depois revisar frase, ritmo e densidade. Se falhar estrategicamente, retornar à 05/07/08/09 conforme a causa, em vez de trocar sinônimos.

Saída: versão rascunho para 13, sem afirmar qualidade aprovada nem salvar em approved. Até 2 reescritas por direção; depois comunicar a lacuna concreta ou propor nova direção.

Para ajuste de escopo, não reescrever copy. Para ajuste de campo, modificar somente os ids declarados e preservar os demais byte a byte. Usar `scripts/revise_delivery.py` conforme `knowledge/ajustes-incrementais.md`; leitura integral de humanização não se repete na mesma conversa quando política, direção e fatos permanecem idênticos.
