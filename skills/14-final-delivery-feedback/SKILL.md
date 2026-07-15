---
name: 14-final-delivery-feedback
description: "Organiza a entrega final (copy + variações + justificativa + orientações + score) e coleta aprovação/reprovação/ajuste do gestor. Use como última skill de qualquer fluxo, após 13-copy-review-scorecard, e também para os comandos /aprovar-copy e /reprovar-copy."
dependencies: ["13-copy-review-scorecard"]
outputs: ["outputs/approved/*.md ou outputs/revised/*.md", "clients/{cliente}.md (atualizado)", "examples/approved|rejected/*.md"]
week: 1
estimated_time: "10 min"
---

# Final Delivery & Feedback

Fecha o ciclo: entrega organizada + captura de feedback, que é o que faz a THAMY IA melhorar com o tempo.

## Dados necessários

1. Copy revisada e nota (skill `13`) — OBRIGATÓRIO.
2. Big idea, oferta, framework das skills anteriores — para montar a justificativa estratégica.
3. `clients/{cliente}.md`.

## Modo de operação

- **Estratégico:** este é o 14º checkpoint isolado do fluxo, como descrito abaixo.
- **Rápido/Express:** esta skill se funde com `13-copy-review-scorecard` no Checkpoint 3 ("Entrega revisada") — não existe uma mensagem de scorecard seguida de uma segunda mensagem de entrega. Score, pontos fracos, copy final e pedido de aprovação saem juntos, na mesma apresentação.

## Checkpoint 1 — Entrega final

Monte a entrega com:
```
Copy final:
Variações:
Justificativa estratégica (por que essa big idea, framework, ângulo):
Orientação para design:
Orientação para tráfego (quando fizer sentido):
Score da copy e pontos mais fracos:
Hipóteses ainda existentes:
```

**Pergunte:**
- "A copy foi aprovada, reprovada ou precisa de ajuste?"

Aguarde resposta.

## Checkpoint 2 — Tratamento da resposta

**Se aprovada:**
Registre em `clients/{cliente}.md` (via lógica de `04-client-memory-builder`): cliente, campanha, canal, formato, copy aprovada, motivo da aprovação, aprendizados. Salve a copy em `outputs/approved/{cliente}-{campanha}-{canal}.md` e um exemplo em `examples/approved/`.

**Se reprovada:**
Pergunte o motivo, oferecendo as opções:
```
[ ] tom inadequado
[ ] promessa fraca
[ ] copy genérica
[ ] desalinhada com briefing
[ ] desalinhada com cliente
[ ] muito longa
[ ] muito agressiva
[ ] faltou clareza
[ ] CTA fraco
[ ] outro
```
Registre em `clients/{cliente}.md` e salve em `examples/rejected/{cliente}-{campanha}-{canal}.md`.

**Se pedir ajuste:**
Pergunte o que precisa mudar, gere nova versão (retornando à skill relevante — produção, adaptação ou revisão, conforme o tipo de ajuste), e registre: feedback recebido, ajuste feito, nova versão, aprendizado. Salve em `outputs/revised/{cliente}-{campanha}-{canal}-v{n}.md`.

## Auto-validação

- [ ] A entrega final cita o cliente e a campanha pelo nome?
- [ ] Justificativa estratégica conecta com big idea/framework reais desta conversa, não é genérica?
- [ ] O tipo de resposta do gestor (aprovado/reprovado/ajuste) foi corretamente registrado em `clients/{cliente}.md`?
- [ ] Se rodou como parte de `/aprovar-copy` ou `/reprovar-copy` direto (sem passar pelo fluxo completo), ainda assim registrou em `clients/{cliente}.md`?

Se falhou → corrija silenciosamente.

## Finalização

1. Confirme ao gestor onde tudo foi salvo (`outputs/...`, `examples/...`, `clients/{cliente}.md`).
2. Pergunte se ele quer produzir a próxima peça (nova variação, outro canal, ou nova campanha).
