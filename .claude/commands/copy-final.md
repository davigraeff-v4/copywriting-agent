Execute o fluxo da THAMY IA a partir do briefing colado nesta conversa (ou peça o briefing se ainda não foi colado).

Escolha o modo de operação conforme `CLAUDE.md` (seção "Modos de operação") e `CONTRATO-OPERACIONAL-MODOS.md`:

- Se o comando vier com `--rapido`, use o modo Rápido (até 3 checkpoints).
- Se vier com `--express`, use o modo Express (1 checkpoint mínimo + aprovação final) — só faz sentido se `clients/{cliente}.md` já estiver consolidado para esse cliente.
- Se vier com `--estrategico`, use o modo Estratégico (checkpoint por skill, até 14).
- Sem nenhum modificador, decida pela tabela de seleção automática do `CLAUDE.md` — na ausência de qualquer sinal, use o modo **Rápido** (padrão).

Declare o modo escolhido em uma frase curta antes de começar.

Acione as skills em `skills/` respeitando os checkpoints do modo escolhido (ver `CONTRATO-OPERACIONAL-MODOS.md` seção 3) e o bloco `HARD CONSTRAINTS`, até chegar à entrega final via `14-final-delivery-feedback`.
