---
name: 04-client-memory-builder
description: "Atualiza estado atual e histórico de cliente com fatos e feedbacks confirmados, preservando versões."
---

# 04-client-memory-builder

## Dados necessários

Ler o SKILL.md integralmente. Modos e checkpoints seguem `CONTRATO-OPERACIONAL-MODOS.md`; caminhos relativos à raiz do projeto.

- `knowledge/memoria-clientes.md`
- `clients/cliente-template.md`
- `quality/feedback-template.md`

## Execução e auto-validação

Pode executar quando houver informação confirmada. Ler estado atual e ficha original antes de editar. Criar/atualizar `clients/current/{cliente}.md`; manter `clients/{cliente}.md` como ponto de entrada e histórico, com referência à visão atual.

Atualizar campo vigente e registrar mudança datada no histórico. Escopar restrições por pessoa, produto, formato e campanha. Preferência global vive na política; não propagá-la copiando para toda ficha. Nunca manter decisão superada como atual.

Feedback literal e interpretação do agent são campos diferentes. Registrar aprovador, versão/hash, motivo e limite de aprendizado. Aprovação não implica publicação nem performance. Em aprovação parcial, identificar peças exatas; não promover lote inteiro.

Se houver migração de ficha contraditória, registrar o conflito e resolver apenas com correção explícita documentada. Preservar arquivos antigos. Saída: visão atual e histórico rastreável; confirmar brevemente o que mudou, sem checkpoint de permissão redundante.
