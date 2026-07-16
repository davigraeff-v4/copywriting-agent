# Contrato Operacional — Modos, Checkpoints, Hard Constraints e Canal×Formato

> Saída da Fase 1 do `PLANO-OTIMIZACAO-AGILIDADE.md`. Este documento resolve as ambiguidades antes de editar `CLAUDE.md`, `AGENTS.md` e as 14 `SKILL.md` (Fases 2 e 3). Decisões validadas com o gestor em 2026-07-11.

## 0. Decisões validadas com o gestor

1. **Modo Rápido é o padrão** quando o gestor não especificar nada.
2. **Modo Express mantém 1 checkpoint mínimo** antes de produzir (mapa estratégico resumido), mesmo sem lacuna ou risco — não entrega 100% direto.
3. **Mapa estratégico consolidado mostra todos os campos**, em formato compacto — não corta para "só decisões principais", para preservar rastreabilidade com o scorecard e com `clients/{cliente}.md`.
4. **Nenhuma elevação automática para o modo Estratégico.** O gestor pede `--estrategico` explicitamente. A segurança para cliente novo/oferta sensível/contradição continua garantida pelo Checkpoint 1 (bloqueio por lacuna crítica) e pelo bloco `HARD CONSTRAINTS` (bloqueio por promessa sensível), que valem nos três modos.
5. Nomes dos modos mantidos: `rápido`, `express`, `estratégico`.
6. Limites padrão por canal/formato quando o briefing não informar: ver seção 4.

## 1. Matriz de campos — crítico, inferível, condicional

| Campo | Classificação | Regra |
|---|---|---|
| Cliente | Crítico | Bloqueia produção se ausente ou ambíguo |
| Objetivo | Crítico | Bloqueia produção se ausente |
| Canal | Crítico | Bloqueia produção se ausente |
| Formato | Crítico | Bloqueia produção se ausente |
| Campanha/ideia central | Crítico | Bloqueia produção se ausente |
| Público | Crítico | Bloqueia produção se ausente ou contraditório |
| Oferta | Crítico | Bloqueia produção se ausente — sem oferta não há promessa para traduzir em benefício (skill 09) |
| Restrições | Crítico | Se não informado, perguntar explicitamente "existe alguma restrição?" antes de produzir — nunca assumir "sem restrições" silenciosamente |
| Referência visual | Condicional | Crítico apenas se o formato exigir referência obrigatória (ex.: vídeo/Reels); se ausente, seguir com a limitação registrada (skill 07) |
| Persona | Inferível | Gerar `[H]` a partir de público + marca; nunca bloqueia |
| Tom de voz | Inferível (ou herdado de `clients/{cliente}.md`) | Gerar `[H]` se ausente e cliente novo |
| Nível de consciência | Inferível | Gerar hipótese preliminar; refinar no mapa estratégico |
| Framework/gatilho/figura de linguagem/CTA | Inferível | Sempre decidido pelo agent, nunca perguntado como campo obrigatório do briefing |
| Duração/ritmo (formato vídeo) | Condicional | Se ausente, usar padrão de canal×formato (seção 4) e marcar como hipótese apenas se o padrão não se aplicar ao caso |

Regra geral: **campo crítico ausente = pausa obrigatória nos três modos.** Campo inferível ausente = segue com hipótese `[H]`, nunca pausa.

## 2. Definição final dos três modos

### 2.1 Rápido (padrão)
- Quando: gestor não especifica modo, briefing razoavelmente completo, sem sinalização de "quero ver passo a passo".
- Checkpoints: até 3 (diagnóstico+fontes / mapa estratégico consolidado / entrega revisada).
- Skills executadas: as 14, mas agrupadas em blocos — ver seção 3.

### 2.2 Express
- Quando: `clients/{cliente}.md` já existe e está com marca/público/restrições consolidados, e a demanda é semelhante a campanhas anteriores.
- Checkpoints: 1 mínimo obrigatório (mapa estratégico resumido, mesmo sem lacuna) + aprovação final = 2 no total.
- Não repete perguntas já respondidas na ficha do cliente. Só pausa fora do checkpoint mínimo se aparecer contradição, oferta nova, promessa sensível ou campo crítico ausente/alterado frente à ficha.

### 2.3 Estratégico
- Quando: o gestor pede explicitamente (`--estrategico`, "quero ver passo a passo", "quero construir junto").
- Checkpoints: até 14 (um por skill), como o fluxo padrão completo usado no Teste 01.
- Esse modo substitui o antigo "fluxo padrão completo" do `CLAUDE.md` atual.

### 2.4 Seleção automática quando o gestor não informar o modo

| Condição | Modo |
|---|---|
| Gestor não diz nada, briefing tem os campos críticos ou pode preenchê-los rápido | Rápido |
| `clients/{cliente}.md` completo (marca, público, restrições) e demanda recorrente | Express |
| Gestor pede explicitamente "sem pausas"/"rápido" | Rápido |
| Gestor pede explicitamente "passo a passo"/"quero validar tudo"/`--estrategico` | Estratégico |

Não há elevação automática por tipo de cliente/oferta (decisão 4 da seção 0) — a segurança fica com o Checkpoint 1 e os Hard Constraints, não com a escolha de modo.

O modo escolhido deve ser informado em uma frase curta no início da execução (ex.: "Sem indicação sua, vou seguir no modo Rápido — até 3 checkpoints.").

## 3. Os três checkpoints consolidados (modo Rápido)

### Checkpoint 1 — Diagnóstico, fontes e restrições (skills 01+02)
```
Briefing compreendido:
Lacunas críticas:
Contradições:
Oferta a confirmar:
Restrições conhecidas:
Fontes disponíveis:
Fontes que devem ser ignoradas:
Hipóteses permitidas:
```
Regras: uma única mensagem; todas as perguntas críticas juntas; pergunta explícita sobre quais documentos podem/não podem ser usados quando houver mais de uma fonte disponível; captura duração/ritmo/requisitos técnicos quando o formato for vídeo.

### Checkpoint 2 — Mapa estratégico consolidado (skills 03+05+06+07+08+09+10)
```
Mapa estratégico

Marca e tom:
Público/persona:
Dor central:
Desejo central:
Nível de consciência e funil:
Oferta:
Promessa sustentável:
Restrições obrigatórias (= HARD CONSTRAINTS vigente):
Referências consideradas:
Big idea:
Framework e gatilho:
CTA:
Hipóteses que precisam de validação:
```
Pergunta padrão: "Posso produzir com essa direção? Corrija apenas o que estiver errado, arriscado ou desalinhado."

Todos os campos aparecem (decisão 3 da seção 0) — formato compacto, não telegráfico a ponto de perder rastreabilidade (cada linha deve continuar permitindo saber qual skill gerou o quê, para uso posterior em `clients/{cliente}.md` e no scorecard).

### Checkpoint 3 — Entrega revisada (skills 11+12+13+14)
```
Copy final adaptada ao canal
Variações previstas para o formato
Orientação para design e tráfego
Justificativa estratégica resumida
Score Geral + Score de Humanização/Anti-Vícios de IA
Pontos mais fracos
Hipóteses ainda existentes
Pedido de aprovação, reprovação ou ajuste
```
Não existe confirmação separada entre scorecard e entrega final — sai tudo junto.

Antes deste checkpoint, as skills `11` e `13` cumprem o Knowledge Gate de forma silenciosa: ambas leem integralmente `knowledge/vicios-ia-humanizacao.md`, em momentos independentes. A entrega só avança se Score Geral ≥ 8, Score de Humanização/Anti-Vícios de IA ≥ 8, zero vício crítico, zero violação de `HARD CONSTRAINTS` e todas as leituras obrigatórias concluídas.

No modo **Express**, os Checkpoints 1 e 2 colapsam em um único checkpoint mínimo (mapa estratégico resumido, já com o diagnóstico silencioso embutido), e o Checkpoint 3 permanece igual.

No modo **Estratégico**, os checkpoints voltam a ser um por skill (14 no total), como hoje.

## 4. Contrato de Hard Constraints

Bloco único, gerado no Checkpoint 1 (a partir de restrições explícitas do briefing) e atualizado a qualquer momento que o gestor corrigir algo — nunca fica só na skill onde apareceu.

```
HARD CONSTRAINTS — {cliente} — {campanha}
- [restrição 1]
- [restrição 2]
- ...
```

Regras:
- Uma restrição validada deixa de ser hipótese e entra direto neste bloco.
- Skills 08, 09, 10, 11, 12 e 13 devem consultar este bloco antes de produzir/validar qualquer trecho.
- Violação de hard constraint = **reprovação automática**, independentemente da média do scorecard (mesmo que a média dê ≥ 8).
- Ajuste do gestor sobre uma restrição atualiza o bloco imediatamente, antes de qualquer reescrita — nunca corrige só o trecho pontual sem propagar pro bloco.
- O bloco é exibido no Checkpoint 2 (mapa estratégico) e na entrega final (Checkpoint 3), para o gestor sempre ver o que está valendo.

Exemplo ilustrativo (baseado num teste real de campanha automotiva, cliente anonimizado):
```
HARD CONSTRAINTS — Cliente X — Reels Fundo de Funil
- Não mencionar percentual de ganho de performance.
- Não mencionar economia de recursos.
- Ativo visual de prova é apoio apenas — nunca citado em locução/texto.
- Não sugerir que todo cliente passa pelo mesmo teste/processo.
- Não sugerir resultado idêntico ou garantido por caso.
```

## 4.1 Contrato de Knowledge Gate e humanização

- `knowledge/README.md` e `knowledge/metodologia-thamy.md` são leitura obrigatória no início de toda campanha ou revisão avulsa.
- Cada skill lê os arquivos de `knowledge/` listados em seus dados necessários antes de agir.
- A skill `11` lê integralmente `knowledge/vicios-ia-humanizacao.md` imediatamente antes de escrever.
- A skill `13` relê integralmente o mesmo arquivo antes de pontuar e calcula um score separado de humanização.
- Alterar a copy invalida os scores anteriores; a nova versão volta à skill `13`.
- A skill `14` e o comando `/aprovar-copy` bloqueiam registro de aprovação sem scores válidos da versão atual.

## 5. Contrato de canal × formato

A skill 12 aplica este contrato **durante** a produção da skill 11 nos modos Rápido e Express (não existe mais copy base genérica intermediária nesses dois modos — só no Estratégico, onde a skill 11 ainda entrega uma copy base antes da 12 adaptar).

### Vídeo / Reels (formato curto, ex.: Meta Reels, TikTok, Stories)
```
Duração máxima padrão: 9-12s quando o briefing não informar
Entrada da locução: colada no primeiro frame — sem silêncio inicial
Gancho no primeiro frame: obrigatório
Quantidade de cenas: 3-4 blocos (hook / corpo / prova-autoridade / CTA, podendo fundir os dois últimos)
Texto na tela: sincronizado com a locução, frases curtas
Locução: tom definido pelo mapa estratégico (skill 03/10)
CTA: alinhado ao objetivo de campanha (ex.: "Enviar mensagem" para objetivo Mensagem)
Legenda: 1-2 frases + CTA, emoji conforme tom da marca
Orientação visual: notas de corte/prova visual, sem repetir o texto da locução
```

### Vídeo institucional / educativo mais longo (ex.: YouTube Shorts educativo, vídeo de topo de funil)
```
Duração máxima padrão: 30-60s quando o briefing não informar
Entrada da locução: pode ter até 2s de contexto visual antes da fala, nunca mais que isso
Estrutura: hook → contexto/educação → prova/diferencial → CTA
```

### Estático (Meta/Google, imagem única)
```
Convenção real V4: 3 variações (A/B/C) por peça, para uso do gestor escolher/testar
Headline + subheadline + CTA + rodapé sempre presentes
```

### Carrossel
```
5-8 slides quando o briefing não informar quantidade
Slide 1 sempre é o hook/headline de abertura
Último slide sempre é CTA
```

### Landing Page / WhatsApp / E-mail / Google Ads
Seguem os templates já existentes na skill 12 atual (sem alteração de estrutura nesta fase — só passam a ser produzidos direto no formato final, sem copy base intermediária, nos modos Rápido/Express).

Quando o briefing não informar esses dados e o padrão acima não se aplicar ao caso (ex.: cliente pede explicitamente vídeo de 30s no feed de Reels), o agent aplica o padrão do canal mas sinaliza a decisão como algo a confirmar no Checkpoint 1, não como fato consolidado.

## 6. Critério de aceite da Fase 1

- [x] Não existe contradição entre este contrato, o `PLANO-OTIMIZACAO-AGILIDADE.md` e as decisões do gestor.
- [x] Os três modos, os três checkpoints, o bloco de hard constraints e o contrato de canal×formato estão definidos de forma que a Fase 2 (atualizar `CLAUDE.md`/`AGENTS.md`) e a Fase 3 (refatorar as 14 skills) possam ser executadas sem reabrir essas decisões.

## 7. Próximo passo

Fase 2 — atualizar `AGENTS.md` e `CLAUDE.md` com os três modos, a seleção automática, os checkpoints consolidados e o bloco `HARD CONSTRAINTS`.
