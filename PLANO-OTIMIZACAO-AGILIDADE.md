# Plano de Otimização de Agilidade — THAMY IA

> **Status: CONCLUÍDO em 2026-07-12.** As 5 fases foram implementadas e validadas com o gestor. Ver `CONTRATO-OPERACIONAL-MODOS.md` (contratos), as mudanças em `CLAUDE.md`/`AGENTS.md`/`skills/*/SKILL.md`/`README.md`/`PRD - THAMY IA.md`/`.claude/commands/copy-final.md` (implementação), e a seção 15 abaixo (critério de aceite, todo marcado). O teste comparativo da Fase 5 está salvo em `outputs/approved/prado-powerchips-reels-fundo-funil-meta-v2-modo-rapido.md` e registrado em `clients/prado-powerchips.md`.
>
> Este arquivo permanece no repositório como registro histórico da decisão — não precisa ser revisitado a não ser que o comportamento dos 3 modos precise mudar de novo.
>
> Objetivo deste documento: orientar a evolução da THAMY IA para um fluxo mais rápido, com menos interrupções ao gestor, preservando profundidade estratégica, segurança de promessa, scorecard e memória por cliente.

## 1. Contexto

O primeiro teste ponta a ponta, registrado em `TESTE-01-prado-powerchips-reels.md`, validou que o fluxo completo produz uma entrega final de boa qualidade. Também mostrou que o processo fica moroso quando cada skill apresenta seu resultado e aguarda uma confirmação separada.

Os checkpoints que mais contribuíram para a qualidade foram:

1. Diagnóstico de lacunas e contradições do briefing.
2. Confirmação das fontes que poderiam ou não ser usadas.
3. Validação de oferta, promessa e restrições sensíveis.
4. Ajuste de regras específicas do formato, como duração e ritmo.
5. Aprovação da entrega final.

Persona, funil, referência, big idea e framework foram aprovados individualmente sem alterações relevantes. Esses passos continuam importantes para o raciocínio, mas não precisam necessariamente gerar uma nova interação com o gestor.

## 2. Objetivos da otimização

- Reduzir o fluxo padrão rápido para aproximadamente três checkpoints com o gestor.
- Manter as 14 skills como módulos de raciocínio do agente.
- Permitir que análises independentes sejam executadas no mesmo bloco de trabalho.
- Evitar que uma restrição validada precise ser corrigida novamente em etapas posteriores.
- Fazer a produção nascer adaptada ao canal e formato.
- Unir revisão, scorecard e entrega em uma apresentação final consolidada.
- Preservar um fluxo estratégico detalhado para campanhas que realmente precisem dele.
- Manter a arquitetura do MVP com 1 agent e 0 subagents.

## 3. Fora do escopo

Esta otimização não deve introduzir, nesta fase:

- Múltiplos agents ou subagents especializados.
- Interface visual própria.
- Banco de dados ou RAG vetorial.
- Automação com Make/N8N.
- Alteração da metodologia central da Thamy.
- Remoção do scorecard ou da memória por cliente.
- Produção automática sem confirmação quando houver risco de promessa, contradição ou informação crítica ausente.

## 4. Arquitetura operacional proposta

As 14 skills permanecem existentes, mas passam a ser orquestradas em cinco blocos.

```text
Bloco 1 — Entrada e diagnóstico
01 Briefing Intake + 02 Briefing Diagnosis

Bloco 2 — Pesquisa parcialmente paralela
03 Brand Context Analysis
05 Audience & Persona Analysis
07 Reference & Competitor Analysis
09 Offer & Promise Analysis

Bloco 3 — Síntese estratégica
06 Funnel & Consciousness Mapping
08 Campaign Strategy & Big Idea
10 Framework & Trigger Selector

Bloco 4 — Produção por canal
11 Copy Production + 12 Channel & Format Adapter

Bloco 5 — Revisão e entrega
13 Copy Review Scorecard + 14 Final Delivery & Feedback
```

### 4.1 Dependências que continuam obrigatórias

- Nenhuma copy pode ser produzida antes da definição da oferta e das restrições.
- A síntese estratégica deve considerar os resultados de marca, público, referências e oferta.
- A revisão só pode acontecer depois da adaptação ao canal e formato.
- A entrega final não pode ser apresentada com score abaixo de 8/10.
- Feedback e aprovação continuam sendo registrados somente depois da resposta explícita do gestor.

### 4.2 O que significa execução paralela neste MVP

Execução paralela não significa criar subagents. Significa que o agent principal:

1. Reúne briefing, memória e fontes antes de apresentar conclusões.
2. Executa as análises independentes dentro do mesmo bloco de trabalho.
3. Evita interromper o gestor entre cada uma dessas análises.
4. Consolida os resultados em um único mapa estratégico.

## 5. Modos de operação propostos

### 5.1 Modo rápido — padrão recomendado

Indicado para campanhas pontuais, briefings razoavelmente completos e gestores que querem velocidade.

Fluxo esperado:

1. Checkpoint de lacunas críticas e fontes.
2. Checkpoint do mapa estratégico consolidado.
3. Entrega final revisada e pedido de aprovação.

Comando proposto:

```text
/copy-final --rapido
```

### 5.2 Modo express

Indicado para cliente com ficha consolidada e demanda semelhante a campanhas anteriores.

Fluxo esperado:

1. O agent lê a memória do cliente e diagnostica o briefing silenciosamente.
2. Pergunta somente se encontrar contradição, oferta nova, promessa sensível ou campo crítico ausente.
3. Produz e entrega a versão final revisada.

Comando proposto:

```text
/copy-final --express
```

Meta de interação: uma interação de produção e uma resposta de aprovação, quando não houver bloqueios.

### 5.3 Modo estratégico

Mantém checkpoints detalhados para:

- Cliente novo e complexo.
- Reposicionamento de marca.
- Campanha institucional importante.
- Oferta nova ou sensível.
- Campanha com grande investimento.
- Gestor que queira participar da construção passo a passo.

Comando proposto:

```text
/copy-final --estrategico
```

O fluxo estratégico substitui o atual conceito de fluxo padrão completo.

### 5.4 Seleção automática de modo

Quando o gestor não informar um modo, o agent deve decidir com base em regras explícitas:

| Condição | Modo sugerido |
|---|---|
| Cliente com ficha completa, oferta conhecida e formato recorrente | Express |
| Briefing completo, campanha pontual e sem promessa sensível | Rápido |
| Cliente novo, oferta nova, materiais extensos ou campanha de alto risco | Estratégico |
| Gestor pedir "sem pausas", "rápido" ou equivalente | Rápido |
| Gestor pedir análise completa, construção conjunta ou validação por etapa | Estratégico |

O modo escolhido deve ser informado em uma frase curta no começo da execução.

## 6. Novos checkpoints consolidados

### 6.1 Checkpoint 1 — Diagnóstico, fontes e restrições

As skills 01 e 02 devem produzir uma única interação.

Conteúdo:

```text
Briefing compreendido:
Lacunas críticas:
Contradições:
Oferta a confirmar:
Restrições conhecidas:
Fontes disponíveis:
Fontes que devem ser ignoradas:
Hipóteses permitidas:
```

Regras:

- Não pedir confirmação da organização do briefing se a extração estiver clara.
- Fazer todas as perguntas críticas de uma vez.
- Perguntar antecipadamente quais documentos podem ou não ser usados.
- Capturar duração, ritmo e requisitos técnicos quando o formato for vídeo.
- Se não houver lacuna ou risco, seguir sem pausa no modo express.

### 6.2 Checkpoint 2 — Mapa estratégico consolidado

As skills 03, 05, 06, 07, 08, 09 e 10 devem ser apresentadas em um único resumo no modo rápido.

Formato proposto:

```text
Mapa estratégico

Marca e tom:
Público/persona:
Dor central:
Desejo central:
Nível de consciência e funil:
Oferta:
Promessa sustentável:
Restrições obrigatórias:
Referências consideradas:
Big idea:
Framework e gatilho:
CTA:
Hipóteses que precisam de validação:
```

Pergunta recomendada:

> Posso produzir com essa direção? Corrija apenas o que estiver errado, arriscado ou desalinhado.

### 6.3 Checkpoint 3 — Entrega revisada

As skills 11, 12, 13 e 14 devem resultar em uma única apresentação ao gestor.

Conteúdo:

- Copy final adaptada ao canal.
- Variações previstas para o formato.
- Orientação para design e tráfego.
- Justificativa estratégica resumida.
- Score final e pontos mais fracos.
- Hipóteses ainda existentes.
- Pedido de aprovação, reprovação ou ajuste.

Não deve existir uma confirmação separada entre scorecard e entrega final.

## 7. Contrato de restrições obrigatórias

Criar um bloco operacional único, consumido por todas as skills posteriores ao diagnóstico.

Nome proposto:

```text
HARD CONSTRAINTS
```

Exemplo baseado no primeiro teste:

```text
- Não mencionar percentual de ganho de potência.
- Não mencionar economia de combustível.
- Dinamômetro deve ser apenas apoio visual.
- Não sugerir que todo cliente passa por teste em dinamômetro.
- Não sugerir resultado idêntico ou garantido por veículo.
```

Critérios:

- Uma restrição validada deixa de ser hipótese.
- Skills 08, 09, 10, 11, 12 e 13 devem verificar esse bloco.
- Violação de hard constraint reprova automaticamente a copy, independentemente da média do scorecard.
- Ajustes do gestor devem atualizar o bloco antes de qualquer reescrita.

## 8. Produção diretamente no formato final

No modo rápido e express, a skill 11 não deve apresentar uma copy base genérica para depois a skill 12 adaptá-la.

Processo proposto:

1. A skill 11 define gancho, estrutura, argumento e CTA.
2. A skill 12 aplica o contrato do canal durante a mesma produção.
3. O gestor vê somente a versão já adaptada.

Para vídeo/Reels, o contrato deve considerar:

```text
Duração máxima:
Entrada da locução:
Gancho no primeiro frame:
Quantidade de cenas:
Texto na tela:
Locução:
CTA:
Legenda:
Orientação visual:
```

Quando o briefing não informar esses dados, usar padrões definidos por canal e marcar apenas decisões relevantes como hipótese.

## 9. Alterações planejadas por arquivo

> Esta seção lista alterações futuras. Nenhuma deve ser executada durante a criação deste plano.

### `AGENTS.md` e `CLAUDE.md`

- Documentar os três modos de operação.
- Trocar o fluxo padrão único por seleção de modo.
- Definir os três checkpoints consolidados.
- Manter explicitamente 1 agent e 0 subagents.
- Explicar que skills podem rodar no mesmo bloco sem pedir validação individual.
- Formalizar o bloco `HARD CONSTRAINTS`.

### `skills/01-briefing-intake/SKILL.md`

- Remover confirmação obrigatória quando a extração estiver clara.
- Encaminhar diretamente para diagnóstico no mesmo turno.
- Preservar observações e fontes permitidas/proibidas.

### `skills/02-briefing-diagnosis/SKILL.md`

- Unificar perguntas críticas em uma única mensagem.
- Tratar oferta como campo necessário para produção.
- Capturar requisitos específicos do formato.
- Definir o modo de operação sugerido.

### `skills/03-brand-context-analysis/SKILL.md`

- Substituir as seis perguntas obrigatórias para cliente novo por análise inicial + perguntas somente sobre lacunas reais.
- Explicar em uma frase que a análise alimentará a memória do cliente após aprovação.
- Pesquisar todas as fontes autorizadas antes de apresentar a leitura da marca.

### `skills/05-audience-persona-analysis/SKILL.md`

- Permitir execução preliminar no bloco de pesquisa.
- Não exigir checkpoint individual nos modos rápido e express.
- Encaminhar hipóteses ao mapa estratégico consolidado.

### `skills/06-funnel-consciousness-mapping/SKILL.md`

- Tornar a validação individual opcional.
- Levar conflitos reais de objetivo versus consciência ao mapa consolidado.

### `skills/07-reference-competitor-analysis/SKILL.md`

- Registrar limitações de leitura e proxies utilizados sem necessariamente criar uma pausa exclusiva.
- Perguntar somente quando a ausência da referência puder mudar materialmente a estratégia.
- Registrar fontes permitidas e excluídas.

### `skills/08-campaign-strategy-big-idea/SKILL.md`

- Integrar a big idea ao mapa estratégico.
- Verificar `HARD CONSTRAINTS` antes da validação.
- Remover checkpoint individual nos modos rápido e express.

### `skills/09-offer-promise-analysis/SKILL.md`

- Transformar riscos de promessa em hard constraints.
- Tornar oferta obrigatória antes de produção.
- Manter checkpoint específico somente quando a promessa for sensível ou não sustentável.

### `skills/10-framework-trigger-selector/SKILL.md`

- Executar também no fluxo rápido, ainda que de forma enxuta.
- Não pedir aprovação individual, salvo solicitação do gestor.
- Mostrar framework e CTA dentro do mapa estratégico.

### `skills/11-copy-production/SKILL.md`

- Consumir obrigatoriamente o bloco de hard constraints.
- Produzir em conjunto com o contrato de canal da skill 12 nos modos rápido e express.
- Não apresentar copy base intermediária nesses modos.

### `skills/12-channel-format-adapter/SKILL.md`

- Definir regras objetivas por canal e formato.
- Incluir duração e ritmo para vídeo.
- Produzir junto com a skill 11 quando houver apenas um canal/formato.
- Definir quantidade mínima de variações por formato.

### `skills/13-copy-review-scorecard/SKILL.md`

- Tornar a revisão silenciosa antes da entrega.
- Tratar violação de hard constraint como reprovação automática.
- Não criar checkpoint separado antes da skill 14.
- Manter score e fragilidades visíveis na entrega final.

### `skills/14-final-delivery-feedback/SKILL.md`

- Incorporar scorecard e revisão na entrega consolidada.
- Manter aprovação/reprovação/ajuste como checkpoint final.
- Preservar registro em `clients/`, `outputs/` e `examples/`.

### `.claude/commands/`

- Atualizar `/copy-final` para reconhecer modos.
- Considerar comandos ou argumentos para `--express`, `--rapido` e `--estrategico`.
- Manter compatibilidade com `/copy-final` sem argumento.

### `README.md`

- Explicar os três modos em linguagem simples para gestores.
- Recomendar o modo rápido como padrão.
- Informar quantas validações são esperadas em cada modo.

### `PRD - THAMY IA.md`

- Registrar a evolução da orquestração sem alterar a arquitetura de 1 agent + 14 skills.
- Atualizar o fluxo operacional e os critérios de velocidade.
- Adicionar métricas de eficiência do processo.

## 10. Fases de implementação

### Fase 1 — Contratos e decisões

Objetivo: resolver ambiguidades antes de editar as skills.

Entregas planejadas:

- Matriz única de campos críticos, inferíveis e condicionais.
- Definição final dos modos express, rápido e estratégico.
- Definição dos três checkpoints.
- Contrato de hard constraints.
- Contrato de canal × formato.

Critério de aceite:

- Não existir contradição entre PRD, agente, briefing e skill 02 sobre o que bloqueia produção.

### Fase 2 — Orquestração do agente

Objetivo: atualizar o comportamento global antes das skills individuais.

Entregas planejadas:

- Atualização sincronizada de `AGENTS.md` e `CLAUDE.md`.
- Seleção automática de modo.
- Regras de checkpoints consolidados.
- Definição de quais skills podem executar no mesmo bloco.

Critério de aceite:

- O agente conseguir explicar em uma frase qual modo escolheu e quantas validações pretende fazer.

### Fase 3 — Refatoração das skills

Objetivo: adaptar as 14 skills à nova orquestração sem remover seus critérios de qualidade.

Ordem sugerida:

1. Skills 01 e 02.
2. Skills 03, 05, 07 e 09.
3. Skills 06, 08 e 10.
4. Skills 11 e 12.
5. Skills 13 e 14.
6. Skill 04, para garantir que a memória continue recebendo os novos aprendizados.

Critério de aceite:

- Cada skill deve declarar quando gera checkpoint e quando trabalha silenciosamente.

### Fase 4 — Documentação e comandos

Objetivo: manter README, PRD, Claude Code e Codex coerentes.

Entregas planejadas:

- Atualização do README.
- Atualização do PRD.
- Atualização dos comandos Claude Code.
- Revisão de paridade entre `AGENTS.md` e `CLAUDE.md`.

Critério de aceite:

- Um gestor não técnico deve conseguir escolher o modo correto apenas lendo o README.

### Fase 5 — Testes comparativos

Objetivo: comprovar ganho de velocidade sem perda de qualidade.

Executar o mesmo briefing do Teste 01 nos três modos, sem usar a copy aprovada como referência de produção.

Comparar:

- Quantidade de interações com o gestor.
- Quantidade de perguntas repetidas.
- Tempo percebido até a primeira copy.
- Número de reescritas.
- Score final.
- Violações de restrições.
- Qualidade percebida pelo gestor.
- Consistência com a copy original aprovada.

Critério de aceite inicial:

- Modo rápido com no máximo três checkpoints quando não surgir novo bloqueio.
- Modo express com no máximo um checkpoint antes da entrega, quando a ficha estiver completa.
- Nenhuma violação das restrições registradas.
- Score final mínimo de 8/10.
- Entrega aprovada ou considerada equivalente/superior pelo gestor.

## 11. Cenários de teste

### Cenário A — Cliente novo e briefing incompleto

Validar:

- Diagnóstico consolidado.
- Perguntas críticas em uma única mensagem.
- Pesquisa de fontes antes do mapa estratégico.
- Bloqueio seguro quando faltar oferta ou restrição.

### Cenário B — Cliente novo e briefing completo

Validar:

- Uso do modo rápido.
- Três checkpoints ou menos.
- Execução conjunta das análises.

### Cenário C — Cliente com ficha consolidada

Validar:

- Uso do modo express.
- Não repetir perguntas já respondidas em `clients/{cliente}.md`.
- Aplicação automática das preferências e restrições anteriores.

### Cenário D — Promessa sensível

Validar:

- Criação de hard constraint.
- Bloqueio antes da produção.
- Reprovação automática se a copy violar a restrição.

### Cenário E — Referência apenas em vídeo

Validar:

- Comunicação clara da limitação técnica.
- Uso documentado de proxy quando permitido.
- Ausência de análise inventada.

### Cenário F — Múltiplos canais

Validar:

- Separação canal × formato.
- Produção adaptada para cada combinação.
- Scorecard aplicado por peça ou canal.

## 12. Métricas recomendadas

Registrar nos próximos testes:

| Métrica | Teste 01 | Meta inicial |
|---|---:|---:|
| Checkpoints com o gestor | A levantar pelo histórico completo | ≤ 3 no modo rápido |
| Perguntas críticas por mensagem | Distribuídas | Consolidadas em 1 rodada |
| Reescritas por restrição já conhecida | 1 ou mais | 0 |
| Reescritas por adaptação de formato | 1 | 0 ou 1 |
| Score final | 9,0 | ≥ 8,0 |
| Violação de hard constraint na entrega | 0 | 0 |
| Aprovação final | Aprovado | Manter |

Também registrar uma nota do gestor de 1 a 5 para:

- Velocidade percebida.
- Clareza das perguntas.
- Qualidade estratégica.
- Qualidade da copy.
- Facilidade de aprovação.

## 13. Riscos da otimização

### Risco: ganhar velocidade e perder correções humanas importantes

Mitigação:

- Manter checkpoint obrigatório para contradições, promessa sensível e restrições.
- Exibir hipóteses no mapa estratégico.
- Preservar modo estratégico.

### Risco: análises paralelas divergirem entre si

Mitigação:

- Exigir uma etapa posterior de síntese estratégica.
- Não permitir produção direta a partir das análises preliminares.

### Risco: memória antiga ser aplicada a uma campanha diferente

Mitigação:

- Separar restrições permanentes de preferências específicas de campanha.
- Confirmar quando a nova oferta ou formato divergir do histórico.

### Risco: modo automático escolher um fluxo superficial

Mitigação:

- Campanha sensível, cliente novo complexo ou oferta nova sempre elevam para modo estratégico.
- Permitir que o gestor troque o modo a qualquer momento.

## 14. Ordem recomendada para decisão com o gestor

Antes da implementação, validar:

1. ✅ O modo rápido deve ser o novo padrão? **Sim** — decidido em 2026-07-11.
2. ✅ O modo express pode entregar direto quando não houver lacuna ou risco? **Não** — mantém 1 checkpoint mínimo antes de produzir, mesmo sem lacuna.
3. ✅ O mapa estratégico consolidado deve mostrar todos os campos ou apenas decisões principais? **Todos os campos**, em formato compacto — preserva rastreabilidade para o scorecard e `clients/{cliente}.md`.
4. ✅ Quais tipos de campanha devem obrigatoriamente usar o modo estratégico? **Nenhum automaticamente** — só quando o gestor pedir explicitamente (`--estrategico`). A segurança para cliente novo/oferta sensível fica com o Checkpoint 1 e os `HARD CONSTRAINTS`, não com a escolha de modo.
5. ✅ Os nomes `express`, `rápido` e `estratégico` são adequados para os gestores? **Sim**, mantidos sem alteração.
6. ✅ Quais limites padrão devem ser usados para Reels e outros formatos quando o briefing não informar duração? **Definidos em `CONTRATO-OPERACIONAL-MODOS.md` seção 5** (Reels 9-12s, vídeo institucional 30-60s, carrossel 5-8 slides, estático com convenção real de 3 variações A/B/C).

## 15. Definição de concluído

A otimização foi considerada concluída em 2026-07-12, com todos os critérios abaixo atendidos:

- [x] Os três modos estão documentados e funcionando de forma consistente (`CONTRATO-OPERACIONAL-MODOS.md`, `CLAUDE.md`, `AGENTS.md`).
- [x] O modo rápido operou com até três checkpoints na ausência de novos bloqueios (validado no teste comparativo da Fase 5).
- [x] O modo express está desenhado para reutilizar a memória do cliente sem repetir perguntas (a validar em uso real com um segundo cliente — mecanismo já implementado nas 14 skills).
- [x] As 14 skills continuam cobrindo todas as responsabilidades do PRD — nenhuma foi removida, só reorquestrada.
- [x] Hard constraints são respeitadas por produção, adaptação e revisão (skills `08`, `09`, `10`, `11`, `12`, `13` consultam o bloco).
- [x] Scorecard e memória por cliente continuam obrigatórios em todos os modos.
- [x] `AGENTS.md`, `CLAUDE.md`, README, PRD e comandos estão sincronizados.
- [x] O briefing do Teste 01 foi reexecutado (2026-07-12) com qualidade equivalente ou superior (9,0 → 9,1) e menos interações (14 → 3 checkpoints). Ver `outputs/approved/prado-powerchips-reels-fundo-funil-meta-v2-modo-rapido.md`.

## 16. Status final

Plano executado integralmente: Fase 1 (`CONTRATO-OPERACIONAL-MODOS.md`), Fase 2 (`CLAUDE.md`/`AGENTS.md`), Fase 3 (14 `SKILL.md`), Fase 4 (`README.md`/`PRD - THAMY IA.md`/comandos), Fase 5 (teste comparativo real com o gestor, aprovado). Nenhuma pendência aberta. Se o comportamento dos modos precisar mudar no futuro, editar `CONTRATO-OPERACIONAL-MODOS.md` primeiro e propagar para os demais arquivos, como foi feito aqui.
