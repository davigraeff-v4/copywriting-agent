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

- `quality/CICLO-REVISAO.md` (diagnóstico, reescrita limitada e encaminhamento)

## Execução e auto-validação

Receber delivery.json + review.json da 13. Usar `scripts/copycheck.py --review ... --render ...` para gerar texto exato em caminho novo. O render bloqueia revisão ausente/desatualizada; nunca reescrever a copy depois dele.

Quando pertinente, explicar a referência que orientou a construção com origem e trecho aplicado, sem alegar conversão ou ganho causal não medido. Apresentar texto, orientação pertinente, justificativa breve, HARD CONSTRAINTS, scores calculados, pontos fracos e hipóteses fora da copy. Perguntar “A copy foi aprovada, reprovada ou precisa de ajuste?”. No Rápido/Express, revisão e entrega são uma apresentação.

Aprovação: registrar quem aprovou, versão/hash, data, motivo e escopo em `clients/{cliente}/campanhas/{campanha}/vN/feedback.md`, referenciando a versão exata de `final.md`. Manter uma copy canônica, sem duplicar em outputs/approved e examples/approved. Referência de curadoria, quando selecionada, fica em `clients/{cliente}/referencias/` e aponta para a versão e o aspecto aproveitável. Cliente final/público/performance são estados separados. Aprovação parcial não promove peças rejeitadas.

Reprovação: registrar mesmo sem score; não exigir revisão para aceitar crítica humana. Usar motivo já informado; perguntar apenas se ausente. Ajuste: identificar se é argumento, fato, voz ou forma; voltar à skill correspondente e invalidar revisão.

Quando o feedback revelar falha de contexto/evidência, recuperação, direção, escrita ou revisão, registrar a observação e a classificação como interpretação separada. Causa incerta fica indeterminada. Não transformar preferência de uma peça em regra global nem retomar otimização do RAG automaticamente.

Atualizar visão atual e histórico pela 04, com feedback literal separado da interpretação. Não rotular correção do agent como revisão da Thamy. Arquivos de clientes/campanhas permanecem locais. Não enviar, publicar, commitar ou fazer push sem autorização específica.

Saída: caminhos reais e status correto. Não iniciar outra campanha ou fazer pergunta comercial de continuação sem necessidade.

Em ajuste incremental, mostrar primeiro o resultado alterado e resumir em uma frase o que foi preservado. Não repetir pesquisa, direção e justificativas idênticas. Corte de formato isolado fica na campanha; não atualizar a visão atual do cliente salvo se o gestor definir preferência persistente.

Bloqueio corrigível segue o ciclo registrado por `scripts/review_cycle.py`, na mesma pasta entre tentativas. Executar a próxima ação autorizada; preservar texto e revisão de cada tentativa. Ao esgotar, apresentar a falha e o encaminhamento concreto. Nunca tratar tentativa interna como aprovação humana.
