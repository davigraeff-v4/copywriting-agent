# Memória: estado atual, campanha e histórico

## Leitura

1. `clients/current/{cliente}.md`: estado atual consolidado com fonte e data.
2. `clients/{cliente}.md`: compatibilidade e histórico original. Não tratar resumo antigo conflitante como vigente.
3. `campaigns/{cliente}/{campanha}/`: briefing, contexto, versões, revisão e feedback daquela campanha.

Se não houver estado atual, usar ficha existente com atenção a correções posteriores. Não aplicar Express quando a única base é contraditória. A migração preserva o arquivo original e torna conflitos explícitos; não resolve por adivinhação.

## Atualização

Editar a visão atual quando surgir decisão confirmada. Preservar o histórico e registrar anterior→novo, motivo, fonte, data, escopo. Não acumular duas regras opostas como igualmente ativas. Diferenciar empresa/pessoa, produto, canal, formato e campanha.

Campos: identidade/produto; público; voz com amostras; fatos/promessas; restrições ativas; preferências por formato; hipóteses; validade/pendências; referências às campanhas. Restrições têm id, regra, escopo, origem, data, status e substituição. Regra global vem da política, sem copiá-la 12 vezes.

Campanhas: decisões e versão aprovada ficam em sua pasta. Registro de feedback inclui quem aprovou (gestor/cliente), versão/hash, motivo literal e aprendizado interpretado separado. Aprovado, publicado e performance medida são estados diferentes.

## Exemplos

`examples/approved/` e `examples/rejected/` são histórico. `examples/curated/` contém seleção anotada, com compatibilidade e limite de uso. Nenhum texto aprovado é automaticamente um exemplo de excelência.

## Permissões e confidencialidade

Fichas e casos reais permanecem locais e ignorados no Git. Salvar feedback de campanha foi autorizado pelo fluxo; isso não autoriza atualizar memórias pessoais globais do Codex, publicar, enviar mensagem nem registrar aprovação não dada. Uma tarefa com limite “não salve arquivos” prevalece: trabalhar no chat e informar a limitação de persistência/verificação.
