---
name: 14-final-delivery-feedback
description: "Entrega a versão validada e registra feedback humano, aprovação parcial e aprendizado por escopo."
---

# 14-final-delivery-feedback

## Dados necessários

Ler o SKILL.md integralmente. Modos e checkpoints seguem `CONTRATO-OPERACIONAL-MODOS.md`; caminhos relativos à raiz do projeto.

- `quality/approval-checklist.md`
- `quality/feedback-template.md`
- `knowledge/memoria-clientes.md`
- `quality/FORMATO-ENTREGA.md`

## Execução e auto-validação

Receber delivery.json + review.json da 13. Usar `scripts/copycheck.py --review ... --render ...` para gerar texto exato em caminho novo. O render bloqueia revisão ausente/desatualizada; nunca reescrever a copy depois dele.

Apresentar texto, orientação pertinente, justificativa breve, HARD CONSTRAINTS, scores calculados, pontos fracos e hipóteses fora da copy. Perguntar “A copy foi aprovada, reprovada ou precisa de ajuste?”. No Rápido/Express, revisão e entrega são uma apresentação.

Aprovação: registrar quem aprovou, versão/hash, data, motivo e escopo. Copiar a versão exata para outputs/approved e registrar exemplo histórico. Cliente final/público/performance são estados separados. Aprovação parcial não promove peças rejeitadas.

Reprovação: registrar mesmo sem score; não exigir revisão para aceitar crítica humana. Usar motivo já informado; perguntar apenas se ausente. Ajuste: identificar se é argumento, fato, voz ou forma; voltar à skill correspondente e invalidar revisão.

Atualizar visão atual e histórico pela 04, com feedback literal separado da interpretação. Não rotular correção do agent como revisão da Thamy. Arquivos de clientes/campanhas permanecem locais. Não enviar, publicar, commitar ou fazer push sem autorização específica.

Saída: caminhos reais e status correto. Não iniciar outra campanha ou fazer pergunta comercial de continuação sem necessidade.
