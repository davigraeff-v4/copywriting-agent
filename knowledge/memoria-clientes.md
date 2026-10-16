# Memória: estado atual, campanha e histórico

## Leitura

1. `python3 scripts/client_brief.py {cliente}`: lê ficha e aprendizados completos, lista campanhas/versões e feedback literal. Não interpreta score como aprovação.
2. `clients/{cliente}/CLIENTE.md`: estado atual consolidado com fonte, data, voz, restrições e pendências. `APRENDIZADOS.md`: decisões e cronologia escopadas.
3. `clients/{cliente}/campanhas/{campanha}/vN/`: briefing, contexto, versões, revisão, final e feedback daquela campanha.
4. `fontes/`, `referencias/` e `assets/` dentro do cliente: materiais locais. `historico/legado/`: originais preservados; não tratar resumo antigo conflitante como vigente.

Clientes ainda não migrados usam `clients/current/{cliente}.md`, `clients/{cliente}.md` e `campaigns/{cliente}/`. Para consolidá-los, gerar plano com `scripts/migrate_clients.py plan --client {cliente} --output .local/plano.json`, inspecionar o manifesto, aplicar e verificar. Não misturar layouts nem criar duas fichas vigentes. Migração é manutenção, não confirmação comercial.

O plano também preserva fichas somente legadas e materiais de cliente sem ficha. Nesse último caso, `CLIENTE.md` declara consolidação pendente, sem preencher fatos ou aprovações. Arquivos na raiz com o prefixo exato do cliente são incluídos. Pastas com apelido e registros em outros locais precisam de atribuição explícita em `--materials .local/materiais.json`: objeto `{ "cliente": [{"path": "tmp/apelido", "area": "fontes"}] }`. Áreas aceitas: `fontes`, `assets`, `historico/legado`. Para acrescentar materiais a clientes já migrados sem reescrever suas fichas, usar `plan --materials-only --materials .local/materiais.json --output .local/complemento.json`. Todas as atribuições e hashes ficam no manifesto, com backup e verificação.

O mapa privado `.local/client-path-map.json` resolve caminhos antigos por correspondência exata com `scripts/client_paths.py`. Os arquivos históricos, inclusive delivery/review assinados, mantêm seus bytes. Para leitura direta de uma referência antiga, resolver primeiro pelo mapa. Não reescrever hashes ou fontes históricas para adequar caminhos.

Se não houver estado atual, usar ficha existente com atenção a correções posteriores. Não aplicar Express quando a única base é contraditória. A migração preserva o arquivo original e torna conflitos explícitos; não resolve por adivinhação.

## Atualização

Editar a visão atual quando surgir decisão confirmada. Preservar o histórico e registrar anterior→novo, motivo, fonte, data, escopo. Não acumular duas regras opostas como igualmente ativas. Diferenciar empresa/pessoa, produto, canal, formato e campanha.

Campos: identidade/produto; público; voz com amostras; fatos/promessas; restrições ativas; preferências por formato; hipóteses; validade/pendências; referências às campanhas. Restrições têm id, regra, escopo, origem, data, status e substituição. Regra global vem da política, sem copiá-la 12 vezes.

Campanhas: decisões e versão aprovada ficam em sua pasta. Registro de feedback inclui quem aprovou (gestor/cliente), versão/hash, motivo literal e aprendizado interpretado separado. Aprovado, publicado e performance medida são estados diferentes.

## Exemplos

Manter `final.md` na versão da campanha como copy canônica; aprovação é registrada em `feedback.md`, sem duplicar o texto. `referencias/curadas/` contém seleção anotada, com compatibilidade e limite de uso. `examples/approved/`, `examples/rejected/` e `examples/curated/` permanecem como layout legado para clientes não migrados. Os índices antigos são resolvidos pelo mapa local. Nenhum texto aprovado é automaticamente um exemplo de excelência.

## Permissões e confidencialidade

Fichas e casos reais permanecem locais e ignorados no Git. Salvar feedback de campanha foi autorizado pelo fluxo; isso não autoriza atualizar memórias pessoais globais do Codex, publicar, enviar mensagem nem registrar aprovação não dada. Uma tarefa com limite “não salve arquivos” prevalece: trabalhar no chat e informar a limitação de persistência/verificação.
