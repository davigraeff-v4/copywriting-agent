# Piloto editorial antes da rodada completa

Plano de desenvolvimento de 16/10/2026: quatro briefings, duas condições, uma execução por condição, oito saídas. Cobre ads, LP, social e direct com `pilot-plan.json`. Três casos vêm da suíte já conhecida; o quarto é sintético novo. Não apresentar o piloto como validação inédita, amostra representativa ou ganho comprovado.

## Preparação

Resolver os ids de `existing_case_ids` em `evals/cases.json` e juntar `additional_cases`. Congelar prompts, fatos, restrições e instruções efetivamente usadas em um diretório novo em `evals/runs/`. Guardar hashes e cópias; não substituir resultados antigos. Os dados são fictícios e a voz fica provisória quando não há amostra. Não inventar dados reais para dar substância.

Condições: instrução simples e agent atual. O baseline de setembro pode entrar numa rodada posterior; o primeiro piloto não depende dele. Usar mesmo modelo exato e esforço nas condições, escolhidos/registrados na execução. Nenhum modelo foi escolhido neste plano. Não instalar, contratar nem enviar dados a API por causa da existência deste documento.

Instrução simples sugerida: “Escreva a peça solicitada em português brasileiro, usando os fatos e limites do briefing. Entregue somente os campos publicáveis pedidos, sem inventar informação.” O agent atual usa as instruções e skills vigentes. Manter sessões independentes, sem ver as outras saídas; não usar subagents neste projeto. Execução sem pausa, quando autorizada para o teste, dispensa a aprovação intermediária fictícia, mas não elimina fatos ou restrições.

Primeira leitura: comparar matéria-prima idêntica. Se o agent usar repertório adicional, registrar consultas, fontes lidas e decisões; a comparação passa a incluir essa seleção. Não chamar isso de ablação isolada da escrita. Recuperação já instalada permanece disponível, sem recalibração.

## Produção e apresentação

Salvar o texto exato de cada condição e seus metadados em `records.json`, conforme `evals/README.md`. Na condição agent, preservar também delivery, revisão e render no diretório local do experimento, com cliente explicitamente fictício. Usar a mesma apresentação de campos publicáveis nas duas condições; esconder planos, scores e rótulos de sistema do avaliador. Registrar que a formatação pode revelar a condição, sem prometer cegamento perfeito.

Executar `scripts/evaluate.py prepare` em diretório novo. Enviar ao avaliador apenas `blind.json` e o formulário de votos, com briefing e rota. Manter `key-private.json` separado. A ausência de saídas reais impede preparar a comparação; não preencher placeholders como se fossem gerações.

## Julgamento

Escolher a versão preferida ou empate e explicar com trechos. Quando útil, anotar as seis dimensões humanas de `evals/README.md`, tempo real de edição e etapa provável da falha. Valores ausentes ficam ausentes. Não usar as notas dadas pelo próprio agent como votos humanos.

O objetivo do piloto é encontrar problemas e verificar se o protocolo é utilizável. Não fixar taxa de vitória para aprovar a estrutura com quatro casos; relatar preferência, empates, falhas e limitações. Se o julgamento revelar gargalo de contexto, direção, escrita ou revisão, corrigir a causa observada. Dificuldades de recuperação são registradas para a etapa posterior do RAG, salvo lacuna central que impeça a tarefa.

O protocolo amplo permanece disponível. Teste técnico aprovado, ensaio feito pelo próprio agent e comparação humana independente são estados distintos.
