---
name: 12-channel-format-adapter
description: "Define os campos publicáveis e requisitos do canal durante a produção, sem aplicar template universal."
---

# 12-channel-format-adapter

## Dados necessários

Ler o SKILL.md integralmente. Modos e checkpoints seguem `CONTRATO-OPERACIONAL-MODOS.md`; caminhos relativos à raiz do projeto.

- `quality/FORMATO-ENTREGA.md`
- `knowledge/regras-por-canal.md`
- `knowledge/politica-editorial.md`

## Execução e auto-validação

Executar junto da 11, usando rota e requisitos extraídos do briefing. Aplicar quantidade de peças/dobras, posição/campos de formulário, duração e espaço. Instrução específica prevalece sobre exemplo histórico.

LP usa outline por pergunta; social usa cartão por pauta; anúncios separam arte e plataforma; e-mail/WhatsApp usam campos pertinentes. Não importar template de anúncio para calendário orgânico. Não impor subheadline, rodapé, FAQ, bônus ou A/B/C.

Vídeo: distinguir locução, tela e nota visual; verificar se o texto cabe no tempo com leitura/estimativa e se há assets. Formulário: rótulos na ordem solicitada, sem campos adicionais silenciosos. Variações e CTAs conforme direção.

Toda frase publicável, inclusive legenda, formulário, selo e texto de tela, deve estar em fields do artefato. Notas internas não são publicadas. Limites técnicos críticos precisam de fonte atual.

Saída: delivery.json completo no formato da rota. A revisão considera a peça inteira, não apenas campos isolados.

Em ajuste, distinguir formato de campo. `Somente feed` retira seções Story, mantendo todos os campos solicitados do Feed. `Somente headline` não autoriza remover apoio/CTA quando a frase significa alvo da edição; seguir os exemplos e a regra de ambiguidade em `knowledge/ajustes-incrementais.md`.
