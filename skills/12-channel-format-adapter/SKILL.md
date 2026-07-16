---
name: 12-channel-format-adapter
description: "Adapta a copy base ao canal e formato definidos no briefing (criativo estático, carrossel, Meta Ads, Google Ads, LinkedIn Ads, WhatsApp, e-mail, landing page, roteiro de vídeo/Reels). Use imediatamente após 11-copy-production."
dependencies: ["11-copy-production"]
outputs: ["copy adaptada por canal (pronta para revisão)"]
week: 1
estimated_time: "15-25 min"
---

# Channel & Format Adapter

Garante que a entrega não saia igual para todos os canais — cada formato tem estrutura, limite e lógica próprios.

## Dados necessários

1. Copy base da skill `11` (modo Estratégico) ou produção conjunta com a `11` (modos Rápido/Express) — OBRIGATÓRIO.
2. Canal(is)/formato(s) do briefing (skill `01`) — OBRIGATÓRIO.
3. `knowledge/regras-por-canal.md` — regras e boas práticas por canal (Google/Meta Ads, e-mail, landing page, LinkedIn, vídeo, SEO), referência de mercado.
4. `knowledge/exemplos-de-estruturas.md` — templates REAIS da V4 para Meta Ads (criativo estático/carrossel, com convenção de 3 variações A/B/C "para uso do gestor") e Landing Page. **Estes templates reais têm prioridade sobre os genéricos abaixo quando o formato bater** — a estrutura de Meta Ads/LP desta skill deve seguir a convenção real sempre que possível.
5. `CONTRATO-OPERACIONAL-MODOS.md` seção 5 — limites padrão de duração/ritmo/quantidade por canal×formato quando o briefing não informar (ex.: Reels sem duração informada = 9-12s, locução colada no primeiro frame).
6. `knowledge/matriz-de-variacoes-e-testes.md` — quando houver variações, preservar a hipótese ao adaptar e evitar mudar múltiplas variáveis sem identificação.

## Checkpoint único — Adaptação por canal

Use o template correspondente ao canal do briefing. Se houver mais de um canal, gere um bloco por canal.

### Criativo estático
```
Contexto da campanha:
Objetivo:
Ângulo escolhido:
Conceito do criativo:
Headline principal:
Subheadline:
Texto de apoio:
Oferta/selo:
CTA:
Rodapé:
Orientação para design:
Variações:
Justificativa estratégica:
Score da copy:
Pontos de validação:
```

### Carrossel
```
Contexto:
Objetivo:
Ângulo:
Estrutura narrativa:
Slide 1 — Headline de abertura:
Slide 2 — Desenvolvimento:
Slide 3 — Problema/desejo:
Slide 4 — Solução/benefício:
Slide 5 — Prova/oferta:
Slide 6 — CTA:
Legenda sugerida:
Orientação para design:
Variações de headline:
Justificativa:
Score:
```

### Meta Ads
```
Objetivo:
Público:
Etapa do funil:
Ângulo:
Framework usado:
Texto principal 1:
Texto principal 2:
Texto principal 3:
Headline 1:
Headline 2:
Headline 3:
Descrição:
CTA recomendado:
Observações para tráfego:
Hipótese de teste A/B:
```

### Google Ads
```
Objetivo:
Intenção de busca:
Grupo de palavras-chave:
Promessa central:
Títulos:
Descrições:
Extensões/sitelinks:
Callouts:
Snippet estruturado:
Observações:
```

### Landing Page
```
Objetivo da LP:
Público:
Nível de consciência:
Promessa central:
Oferta:
Hero section:
Subheadline:
Bullets de benefício:
Seção de problema:
Seção de solução:
Seção de diferenciais:
Provas:
Quebra de objeções:
FAQ:
CTA principal:
CTAs secundários:
Observações de CRO:
```

### WhatsApp
```
Contexto:
Objetivo da mensagem:
Etapa da conversa:
Mensagem curta:
Mensagem média:
Mensagem consultiva:
Follow-up 1:
Follow-up 2:
Quebra de objeção:
CTA:
```

### E-mail
```
Objetivo:
Segmento da base:
Etapa do funil:
Assunto 1:
Assunto 2:
Pré-header:
Corpo do e-mail:
CTA:
Variação mais direta:
Variação mais narrativa:
Observações:
```

### Roteiro de vídeo/Reels
```
Objetivo:
Formato:
Duração estimada:
Gancho inicial:
Cena 1:
Cena 2:
Cena 3:
Cena 4:
CTA:
Texto na tela:
Legenda:
Orientações visuais:
```

(LinkedIn Ads segue a estrutura de Meta Ads, ajustando tom para B2B/profissional quando aplicável — sinalize a adaptação.)

Se o briefing não informar duração/ritmo/quantidade de variações, aplique o padrão de `CONTRATO-OPERACIONAL-MODOS.md` seção 5 e sinalize a decisão (não é hipótese `[H]` de conteúdo, é uma decisão operacional padrão — registre como tal).

## Modo de operação

- **Estratégico:** apresente a adaptação isoladamente e pergunte, como abaixo. Checkpoint separado da skill `11`.
- **Rápido/Express:** produza junto com a skill `11` quando houver um único canal/formato — o gestor só vê a versão já adaptada, dentro do Checkpoint 3 ("Entrega revisada"), com scorecard e entrega juntos. Se houver mais de um canal, gere um bloco por canal, ainda dentro do mesmo Checkpoint 3.

**Apresente a(s) adaptação(ões) e pergunte (checkpoint isolado só no modo Estratégico; nos modos Rápido/Express, a pergunta some para dentro do Checkpoint 3):**
- "A adaptação para [canal] está no formato que o time de tráfego/design precisa?"

No modo Estratégico, aguarde aprovação antes de avançar para a revisão.

## Auto-validação

- [ ] Usou o template correto do canal informado no briefing?
- [ ] Cada canal tem "Justificativa"/"Score" preenchido ou reservado para a skill 13?
- [ ] Orientação para design/tráfego está presente quando o template pede?
- [ ] Não copiou a copy base 1:1 sem adaptar ao limite/lógica do canal?

Se falhou → regenere silenciosamente.

## Finalização

1. Informe: "Copy adaptada para [canal(is)]. Próximo passo: `13-copy-review-scorecard`."
