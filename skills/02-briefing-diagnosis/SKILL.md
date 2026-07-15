---
name: 02-briefing-diagnosis
description: "Avalia se o briefing organizado tem informação suficiente para produzir copy final. Use logo após 01-briefing-intake, sempre antes de qualquer skill de estratégia ou produção."
dependencies: ["01-briefing-intake"]
outputs: ["diagnóstico de lacunas (em memória de conversa)"]
week: 1
estimated_time: "5 min"
---

# Briefing Diagnosis

Classifica as lacunas do briefing organizado em críticas, importantes e não críticas, e decide se pode seguir ou se precisa perguntar antes.

## Dados necessários

1. Estrutura organizada da skill `01-briefing-intake` — OBRIGATÓRIO.
2. `clients/{cliente}.md`, se existir.

## Checkpoint único — Classificação de lacunas

Classifique cada campo faltante ("Pontos faltantes" da skill 01) em:

1. **Críticas** — bloqueiam produção. Lista de referência (ver `CONTRATO-OPERACIONAL-MODOS.md` seção 1): cliente, campanha, objetivo, canal, formato, público, oferta, ideia/estratégia da campanha, referência visual (quando obrigatória pelo formato), restrições. **Oferta é crítica em qualquer modo** — nunca produza sem ela.
2. **Importantes** — não bloqueiam, mas reduzem qualidade se ausentes (ex.: persona, links auxiliares).
3. **Não críticas** — apoio operacional (ex.: Notion, pasta do Drive, ID visual).

Se o formato for vídeo/Reels, capture também: duração esperada, ritmo desejado, quantidade de peças — se ausente, aplique o padrão de `CONTRATO-OPERACIONAL-MODOS.md` seção 5 e sinalize como decisão a confirmar, não como lacuna crítica.

Regra:
- Se houver qualquer lacuna **crítica**, pare e pergunte ao gestor antes de seguir — em qualquer modo, inclusive Express.
- Se só houver lacunas **importantes** ou **não críticas**, siga com hipótese explícita (sinalizada como "[H]") para o que faltar, e informe ao gestor o que está sendo assumido.
- Toda restrição identificada (do briefing, de `clients/{cliente}.md` ou de resposta do gestor) entra imediatamente no bloco `HARD CONSTRAINTS` — não fica solta no diagnóstico.

## Modo de operação

- **Estratégico:** este checkpoint é isolado, como descrito abaixo.
- **Rápido/Express:** una esta skill com `01-briefing-intake` em uma única mensagem (Checkpoint 1: "Diagnóstico, fontes e restrições" — ver `CONTRATO-OPERACIONAL-MODOS.md` seção 3). Inclua também: quais fontes/documentos podem ser usados e quais devem ser ignorados (pergunte se houver mais de uma fonte disponível e não estiver claro). Se não houver lacuna crítica nem contradição, e o modo for Rápido, siga direto para o bloco de pesquisa (skills 03/05/06/07/08/09/10) sem esperar confirmação separada da organização do briefing.
- Ao final deste checkpoint, declare o modo de operação escolhido em uma frase curta (ex.: "Sem indicação sua, vou seguir no modo Rápido — até 3 checkpoints.").

**Se houver lacuna crítica, pergunte (uma única mensagem, todas as perguntas críticas juntas):**
- "Antes de seguir, preciso confirmar: [liste as lacunas críticas, uma pergunta objetiva por lacuna]."

**Se não houver lacuna crítica, informe e pergunte:**
- "O briefing tem o essencial. Vou seguir assumindo [liste hipóteses] — confirma ou ajusta algum ponto antes de eu continuar?"

Aguarde resposta antes de avançar para o bloco de pesquisa (`03-brand-context-analysis` e seguintes).

## Auto-validação

- [ ] Toda lacuna crítica da lista de referência foi checada (mesmo que preenchida)?
- [ ] Nenhuma lacuna crítica foi tratada como hipótese silenciosa?
- [ ] Hipóteses estão sinalizadas com "[H]"?

Se falhou → regenere silenciosamente.

## Finalização

1. Registre o diagnóstico (lacunas + hipóteses assumidas) para uso pelas próximas skills.
2. Informe: "Diagnóstico concluído. Próximo passo: `03-brand-context-analysis`."
