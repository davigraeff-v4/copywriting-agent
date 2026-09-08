# Recuperação seletiva sem banco vetorial

O briefing, política, rota e restrições vigentes entram sempre no pacote; não dependem de ranking. `scripts/retrieve.py` busca referências em índice de metadados, filtra cliente/rota/uso e ranqueia termos. Ele não consulta Drive nem classifica a verdade automaticamente.

Uso: `python3 scripts/retrieve.py --query "marca desconhecida custo benefício" --route lp --client cliente --index knowledge/retrieval-index.json --index examples/curated/index.json`.

Índice local de exemplos é opcional. Ausência de exemplo pertinente é resultado válido; não preencher com outro cliente como fonte factual. Busca retorna caminho/uso e excerto; abrir o documento selecionado antes de usar. Não carregar todas as referências.

Metadados: id, path, client (`*` apenas para metodologia/didático), routes, tags, status (`active`, `historical`, `superseded`), use (`guidance`, `positive`, `negative`, `structure`), summary. O comando exclui superseded/historical por padrão, bloqueia exemplos de outro cliente e pastas de avaliação. Referência histórica só entra via consulta explícita e leitura das ressalvas.

Métrica de recuperação: encontrou regra/exemplo aplicável, evitou estado superado e contexto de outro cliente? Anotar falhas reais antes de adotar embeddings. Não confundir consulta de palavras com RAG vetorial ou validação factual.
