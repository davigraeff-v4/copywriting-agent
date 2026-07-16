---
name: 03-brand-context-analysis
description: "Analisa a marca antes de qualquer produção de copy: produto/serviço, tom de voz, posicionamento, diferenciais, promessas permitidas e sensíveis. Use após 02-briefing-diagnosis ter liberado o briefing, ou sempre que o gestor pedir 'entender a marca' ou 'contexto do cliente'."
dependencies: ["02-briefing-diagnosis"]
outputs: ["análise de marca (em memória de conversa)"]
week: 1
estimated_time: "10-15 min"
---

# Brand Context Analysis

Entende a marca antes da copy — essencial para não produzir texto genérico. Se conecta às informações essenciais da marca no método da Thamy: produto/serviço, público-alvo e tom de voz.

## Dados necessários

1. Estrutura organizada e diagnóstico das skills `01` e `02` — OBRIGATÓRIO.
2. `clients/{cliente}.md`, se existir — OBRIGATÓRIO checar antes de perguntar.
3. Links auxiliares do briefing (Instagram, site, LP) — se fornecidos, considere o que está descrito/observável a partir deles; não invente conteúdo que não foi visto.
4. `knowledge/padroes-copy-v4.md` — padrão de tom quando o cliente não especifica (ainda placeholder).
5. `knowledge/estrategia-de-marca.md` — frameworks de branding para organizar a leitura (genérico de mercado, usar como estrutura enquanto `padroes-copy-v4.md` não estiver preenchido).
6. `knowledge/processo-kickoff-cliente.md` — real, V4: as 6 perguntas de kickoff e os critérios de análise de redes sociais/site/LP. Se o cliente for novo (sem `clients/{cliente}.md`), use as 6 perguntas de kickoff antes de inferir qualquer coisa.
7. `knowledge/canais-por-modelo-de-negocio.md` — para identificar o modelo de negócio do cliente e checar coerência com os canais do briefing.
8. `knowledge/pesquisa-voz-do-cliente.md` — quando houver entrevistas, reviews, comentários, tickets ou outras fontes de linguagem real; separar fato, síntese e hipótese.

## Checkpoint único — Análise de marca

Produza a análise cobrindo:

```
Produto/serviço:
Tom de voz:
Posicionamento:
Diferenciais:
Promessas permitidas:
Promessas sensíveis:
Linguagem atual (como a marca já se comunica):
Estilo comercial (agressivo, consultivo, educativo, etc.):
```

Regra: se `clients/{cliente}.md` já tiver esses campos, use como base e só pergunte o que estiver em conflito com o briefing atual ou ausente.

Para cliente novo (sem `clients/{cliente}.md`): não faça as 6 perguntas de kickoff cruas uma a uma. Pesquise antes todas as fontes autorizadas (links do briefing, Drive quando o gestor autorizar, docs indicados) e monte uma leitura inicial com hipóteses `[H]` claramente marcadas nos pontos que as fontes não cobriram — só pergunte sobre as lacunas reais que restarem. Se, ao apresentar essa leitura, o gestor perguntar o motivo, explique em uma frase que essa análise vai alimentar a memória permanente do cliente (`clients/{cliente}.md`) depois de aprovada.

## Modo de operação

- **Estratégico:** apresente a análise isoladamente e pergunte, como abaixo.
- **Rápido/Express:** não pause aqui. Rode esta skill silenciosamente junto com `05`, `06`, `07`, `08`, `09`, `10`, e leve o resultado consolidado para o Checkpoint 2 ("Mapa estratégico"). Só interrompa fora do checkpoint consolidado se encontrar uma promessa sensível/insustentável (vira `HARD CONSTRAINTS` e pode exigir confirmação pontual) ou uma contradição real com `clients/{cliente}.md`.

**Apresente a análise e pergunte (checkpoint isolado, modo Estratégico; ou dentro do Mapa estratégico, modos Rápido/Express):**
- "Essa leitura da marca está correta? Tem alguma promessa que NÃO podemos fazer e que eu não sinalizei?"
- "O tom de voz está alinhado com o que o cliente espera?"

Aguarde aprovação antes de avançar.

## Auto-validação

- [ ] Mencionou o cliente pelo nome?
- [ ] Diferenciou promessas permitidas de sensíveis, não misturou?
- [ ] Usou dado real do briefing/`clients/{cliente}.md`, não genérico de mercado?
- [ ] Se inferiu algo, sinalizou "[H]"?

Se falhou → regenere silenciosamente.

## Finalização

1. Se houver informação nova de marca (não estava em `clients/{cliente}.md`), sugira rodar `04-client-memory-builder` para registrar.
2. Informe: "Análise de marca concluída. Próximo passo depende do fluxo: `05-audience-persona-analysis` (fluxo estratégico) ou `09-offer-promise-analysis` (fluxo simples)."
