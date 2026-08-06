---
name: 04-client-memory-builder
description: "Cria ou atualiza a ficha operacional do cliente em clients/{cliente}.md. Use sempre que houver informação nova de marca, público ou feedback para registrar, ou quando o gestor pedir explicitamente 'salvar/atualizar ficha do cliente'. Não bloqueia o fluxo principal — pode rodar em paralelo/a qualquer momento."
dependencies: []
outputs: ["clients/{cliente}.md"]
week: 1
estimated_time: "5 min"
---

# Client Memory Builder

Cria e mantém a memória operacional do cliente — é o que permite ao Copywriting Agent melhorar com o tempo sem depender de memória solta no chat. Sem essa skill, cada conversa começaria do zero.

## Dados necessários

1. `clients/cliente-template.md` — modelo de campos.
2. `clients/{cliente}.md`, se já existir — para atualizar, não recriar do zero.
3. Outputs relevantes desta conversa (análise de marca, persona, feedback de aprovação/reprovação) que devem virar memória permanente.

## Checkpoint único — Criar ou atualizar ficha

Se `clients/{cliente}.md` **não existir**: crie a partir de `clients/cliente-template.md`, preenchendo com o que já se sabe desta conversa.

Se **existir**: atualize apenas os campos com informação nova ou mudada. Nunca sobrescreva o histórico de campanhas — sempre acrescente uma nova entrada.

Campos:
```
Cliente:
Segmento:
Produto/serviço:
Público:
Tom de voz:
Promessas permitidas:
Promessas proibidas:
Campanhas anteriores:
Copies aprovadas:
Copies rejeitadas:
Preferências do cliente:
Restrições:
Observações do gestor:
Aprendizados:
```

O bloco `HARD CONSTRAINTS` desta conversa (ver `CONTRATO-OPERACIONAL-MODOS.md` seção 4) alimenta diretamente os campos `Promessas proibidas` e `Restrições` — toda restrição validada nesta conversa deve estar refletida na ficha, não só na memória de curto prazo da conversa. Preferências de processo do gestor (ex.: ritmo de vídeo, como tratar um asset visual, modo de operação preferido) entram em `Preferências do cliente` e/ou `Aprendizados`, com data — são o que evita repetir a mesma correção na próxima campanha desse cliente.

Este é um passo operacional — normalmente não precisa de aprovação explícita do gestor, apenas confirme brevemente o que foi salvo.

**Informe:**
- "Ficha de {cliente} atualizada: [resuma o que mudou]."

## Auto-validação

- [ ] Não sobrescreveu histórico anterior?
- [ ] Só adicionou/atualizou o que é fato desta conversa (não hipótese)?
- [ ] Data registrada em qualquer entrada de histórico de campanha?

Se falhou → corrija silenciosamente.

## Finalização

1. Salve/atualize `clients/{cliente}.md`.
2. Volte ao fluxo principal de onde essa skill foi chamada.
