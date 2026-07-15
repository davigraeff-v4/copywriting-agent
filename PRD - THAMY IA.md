# **PRD — THAMY IA**

## **1\. Visão geral**

**Nome do produto:** THAMY IA  
 **Tipo:** Agent de copywriting com skills modulares  
 **Usuários iniciais:** Gestores de projeto da V4  
 **Objetivo principal:** Ganhar velocidade e padronizar qualidade na criação de copies finais  
 **Modo de uso inicial:** Briefing colado direto no chat, com possibilidade futura de uso via arquivos em repositório  
 **Ambientes previstos:** Claude Code e Codex  
 **Arquitetura recomendada:** 1 agent principal \+ 14 skills

A **THAMY IA** será um agent de copywriting estratégico inspirado no método de trabalho da Thamy, copywriter da V4. O agent deve transformar um briefing de campanha em uma entrega final de copy com alto nível de qualidade, variações, explicação estratégica, orientação para design/tráfego e revisão crítica.

A metodologia-base da Thamy se organiza em quatro grandes etapas: **pesquisa e estratégia, ideação, escrita e revisão**. O documento enviado também reforça que a copy deve considerar público, dores, estilo de vida desejado, premissa, big idea, oferta, jornada do comprador, ganchos, benefícios e CTAs.

---

# **2\. Problema**

Hoje, a produção de copy depende muito da qualidade do briefing, da interpretação do gestor e da capacidade individual de quem escreve. Isso gera alguns riscos:

```
1. Variação grande na qualidade das entregas.
2. Copies genéricas quando feitas por IA sem método.
3. Dependência da copywriter para manter o padrão.
4. Falta de padronização entre canais, clientes e campanhas.
5. Briefings completos, mas nem sempre traduzidos em boas ideias.
6. Dificuldade de transformar referência, concorrência e contexto em copy final.
7. Pouco reaproveitamento estruturado de aprendizados anteriores.
```

A THAMY IA resolve isso criando uma esteira padronizada de raciocínio, escrita e revisão.

---

# **3\. Objetivo do produto**

Criar um agent capaz de receber um briefing de campanha e entregar **copy final pronta para uso**, com qualidade superior a uma IA genérica.

A THAMY IA deve:

```
1. Ler e organizar o briefing.
2. Identificar objetivo, canal, formato, público, oferta e restrições.
3. Entender o contexto da marca.
4. Analisar público, persona, dores, desejos e objeções.
5. Mapear funil e nível de consciência.
6. Analisar referências visuais, site, Instagram, LP e materiais auxiliares.
7. Definir big idea, gancho e linha criativa.
8. Escolher framework, gatilho, figura de linguagem e CTA.
9. Produzir copy final.
10. Gerar variações.
11. Adaptar a entrega ao canal/formato.
12. Revisar com scorecard.
13. Explicar a lógica estratégica da copy.
14. Registrar feedback para melhoria futura.
```

---

# **4\. Princípio central**

A THAMY IA não deve “escrever bonito”. Ela deve **escrever com intenção estratégica**.

O princípio central do produto será:

```
Não vender apenas produto.
Vender uma solução para um problema.
```

Isso está alinhado ao material da Thamy, que reforça Jobs To Be Done, copywriting conversacional, simplicidade, voz ativa, conexão emocional e tradução de características em benefícios reais.

---

# **5\. Usuários**

## **Usuário principal**

**Gestor de projeto da V4**

Características:

```
1. Conhecimento médio a alto de marketing.
2. Entende campanha, cliente e objetivo.
3. Nem sempre é especialista em copy.
4. Precisa ganhar velocidade.
5. Precisa entregar demandas para design, tráfego ou cliente.
6. Pode colar briefing diretamente no chat.
7. Não necessariamente sabe usar GitHub com profundidade.
```

## **Usuários futuros**

```
1. Copywriters.
2. Estrategistas.
3. Designers.
4. Gestores de tráfego.
5. Lideranças de operação.
6. Time comercial, em casos de copy para prospecção.
```

---

# **6\. Escopo do MVP**

## **Dentro do escopo**

O MVP deve permitir:

```
1. Receber briefing colado no chat.
2. Diagnosticar o briefing.
3. Usar metodologia da Thamy.
4. Consultar base de frameworks, exemplos e padrões.
5. Gerar copy final para múltiplos canais.
6. Gerar variações.
7. Explicar a estratégia por trás da copy.
8. Dar orientações para design/tráfego.
9. Revisar a própria entrega.
10. Gerar output estruturado.
11. Registrar aprovação/reprovação e feedback.
12. Criar memória operacional por cliente em arquivo Markdown.
```

## **Fora do escopo do MVP**

Não entra agora:

```
1. Interface visual própria.
2. Banco de dados.
3. RAG avançado.
4. API conectada ao Drive.
5. Automação com Make/N8N.
6. Dashboard de performance.
7. Treinamento fino de modelo.
8. Múltiplos agents especializados.
9. Compliance jurídico avançado.
10. Integração automática com CRM.
```

---

# **7\. Arquitetura do sistema**

## **Decisão principal**

```
1 agent principal
14 skills
0 subagents no MVP
```

## **Agent principal**

```
Nome: THAMY IA
Função: Orquestrar o processo completo de copywriting.
```

A THAMY IA será responsável por:

```
1. Receber briefing.
2. Entender o tipo de demanda.
3. Acionar as skills necessárias.
4. Organizar o raciocínio estratégico.
5. Produzir a copy final.
6. Revisar a entrega.
7. Solicitar aprovação ou feedback.
```

## **Por que não criar vários agents agora?**

Porque o usuário inicial será gestor de projeto. A operação precisa ser simples.

Se criarmos vários agents, a operação fica mais difícil de explicar, manter e escalar. No MVP, o gestor deve interagir com apenas uma entidade:

```
THAMY IA
```

Por trás, ela aciona as skills.

---

# **8\. Skills da THAMY IA**

## **Skill 1 — `briefing-intake`**

**Função:** receber o briefing colado no chat e transformar em estrutura organizada.

Entrada:

```
Briefing de criativo geral.
Links auxiliares.
Observações do gestor.
Contexto adicional.
```

Saída:

```
Cliente:
Campanha:
Objetivo:
Canal:
Formato:
Público:
Persona:
Oferta:
Referências:
Restrições:
Links auxiliares:
Pontos faltantes:
```

---

## **Skill 2 — `briefing-diagnosis`**

**Função:** avaliar se o briefing tem informação suficiente para produzir copy final.

Deve classificar lacunas em:

```
1. Críticas.
2. Importantes.
3. Não críticas.
```

Regra:

```
Se faltar informação crítica, perguntar antes de produzir.
Se faltar informação não crítica, seguir com hipótese explícita.
```

Informações críticas sugeridas:

```
cliente
campanha
objetivo
canal
formato
público
ideia/estratégia da campanha
referência visual
restrições
```

---

## **Skill 3 — `brand-context-analysis`**

**Função:** entender a marca antes da copy.

Deve analisar:

```
produto/serviço
tom de voz
posicionamento
diferenciais
promessas permitidas
promessas sensíveis
linguagem atual
estilo comercial
```

Essa skill se conecta às informações essenciais da marca no documento da Thamy: entender produto/serviço, público-alvo e tom de voz.

---

## **Skill 4 — `client-memory-builder`**

**Função:** criar e atualizar ficha operacional do cliente.

Arquivo sugerido:

```
/clients/nome-do-cliente.md
```

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

Essa skill permite que a THAMY IA melhore com o tempo sem depender de memória solta no chat.

---

## **Skill 5 — `audience-persona-analysis`**

**Função:** transformar público-alvo em leitura estratégica.

Deve mapear:

```
persona operacional
dores
desejos
objeções
medos
motivadores
nível de consciência
linguagem provável
estilo de vida desejado
```

A metodologia da Thamy começa justamente por conhecer público, dores e estilo de vida desejado.

---

## **Skill 6 — `funnel-consciousness-mapping`**

**Função:** definir etapa do funil e nível de consciência.

Deve classificar:

```
Topo
Meio
Fundo
```

E conectar com:

```
objetivo
framework sugerido
gatilho
figura de linguagem
CTA
```

O documento da Thamy traz uma planilha guia relacionando etapa do funil, objetivo, framework, gatilho, figura de linguagem e CTA.

---

## **Skill 7 — `reference-competitor-analysis`**

**Função:** analisar referência visual, concorrentes e materiais auxiliares.

Deve responder:

```
O que aproveitar?
O que evitar?
Qual tom seguir?
Qual estrutura parece funcionar?
Qual tipo de promessa aparece?
Qual padrão visual/comercial a referência usa?
Como superar a comunicação genérica?
```

Essa skill é importante porque a Thamy trabalha com referência, concorrente, site, Instagram e materiais do cliente antes de escrever.

---

## **Skill 8 — `campaign-strategy-big-idea`**

**Função:** definir a estratégia criativa da campanha.

Deve gerar:

```
premissa
big idea
ângulo narrativo
mensagem central
linha criativa
papel da campanha
hipótese de impacto
```

Essa skill representa a etapa de **ideação**, onde a Thamy entende premissa, big idea, conteúdo, oferta, estrutura, fluxo e gatilhos emocionais.

---

## **Skill 9 — `offer-promise-analysis`**

**Função:** analisar oferta, promessa e transformação.

Deve responder:

```
Qual é a oferta?
Qual é a promessa central?
Qual problema a oferta resolve?
Qual desejo a oferta ativa?
Quais características precisam virar benefícios?
Qual transformação a copy deve vender?
```

Regra obrigatória:

```
Não listar só características.
Traduzir características em benefícios reais.
```

O documento da Thamy reforça que a copy deve focar no valor, no problema resolvido e em como a pessoa vai se sentir depois de usar o produto ou serviço.

---

## **Skill 10 — `framework-trigger-selector`**

**Função:** escolher a estrutura estratégica da copy.

Deve definir:

```
framework principal
framework secundário, se necessário
gatilho emocional
figura de linguagem
CTA
tipo de conteúdo
```

Frameworks iniciais:

```
AIDA
PAS
BAB
4Us
Storytelling
Punchline / One Liner
Jobs To Be Done
```

Critério de escolha:

```
objetivo
funil
persona
canal
gatilho
nível de consciência
oferta
```

---

## **Skill 11 — `copy-production`**

**Função:** escrever a copy final.

Deve produzir a versão final com base em:

```
briefing
marca
público
funil
objetivo
canal
formato
big idea
oferta
framework
gatilho
CTA
tom de voz
```

A copy deve ser:

```
clara
humana
conversacional
específica
orientada a benefício
conectada com o público
não genérica
não excessivamente funcional
```

---

## **Skill 12 — `channel-format-adapter`**

**Função:** adaptar a copy ao canal e formato.

Formatos iniciais suportados:

```
criativo estático
carrossel
banner
Meta Ads
Google Ads
LinkedIn Ads
WhatsApp
E-mail
Landing Page
roteiro de vídeo/Reels
```

Essa skill garante que a entrega não saia igual para todos os canais.

---

## **Skill 13 — `copy-review-scorecard`**

**Função:** revisar a copy antes da entrega final.

Critérios baseados na revisão pós-copy da Thamy:

```
headline chamativa
headline clara
headline conversa com o público certo
subheadline clara e explicativa
CTA claro
CTA direciona para o objetivo certo
comunicação atraente
evita termos repelentes
```

Esses critérios aparecem diretamente no checklist de revisão pós-copy do documento da Thamy.

Score mínimo sugerido:

```
Nota mínima para entrega: 8/10
Se abaixo de 8: revisar automaticamente antes de entregar.
```

---

## **Skill 14 — `final-delivery-feedback`**

**Função:** organizar a entrega final e coletar feedback do usuário.

Deve entregar:

```
copy final
variações
justificativa estratégica
orientação para design
orientação para tráfego, quando fizer sentido
pontos de validação
score da copy
pergunta de aprovação
```

Também deve permitir:

```
aprovar copy
reprovar copy
pedir ajuste
registrar feedback
sugerir atualização da base
```

---

# **9\. Fluxo operacional completo**

> Atualizado após o Teste 01 (`TESTE-01-prado-powerchips-reels.md`) e o `PLANO-OTIMIZACAO-AGILIDADE.md`. As 14 skills e suas responsabilidades continuam as mesmas — o que mudou é a orquestração: quantas interrupções o gestor recebe. Detalhamento completo em `CONTRATO-OPERACIONAL-MODOS.md`.

As 14 skills passam a ser executadas em um de três **modos de operação**, escolhidos automaticamente (ou pelo gestor via `--rapido`/`--express`/`--estrategico`):

## **Modo Rápido (padrão)**

Até 3 checkpoints com o gestor. As 14 skills continuam rodando como módulos de raciocínio, mas agrupadas em 3 blocos de interação:

```
Checkpoint 1 — Diagnóstico, fontes e restrições
  briefing-intake + briefing-diagnosis (uma única mensagem)

Checkpoint 2 — Mapa estratégico consolidado
  brand-context-analysis + audience-persona-analysis + funnel-consciousness-mapping
  + reference-competitor-analysis + campaign-strategy-big-idea + offer-promise-analysis
  + framework-trigger-selector (rodam em sequência, sem pausa individual)

Checkpoint 3 — Entrega revisada
  copy-production + channel-format-adapter + copy-review-scorecard
  + final-delivery-feedback (copy já no formato final, com score, direto para aprovação)
```

`client-memory-builder` roda em paralelo, sem gerar checkpoint próprio, sempre que houver informação nova de marca/cliente a registrar.

## **Modo Express**

Para cliente com `clients/{cliente}.md` já consolidado (marca, público, restrições) e demanda semelhante a campanha anterior. 1 checkpoint mínimo (mapa estratégico resumido) + aprovação final = 2 interações no total quando não houver bloqueio novo.

## **Modo Estratégico**

Substitui o antigo "fluxo padrão de 21 passos" — um checkpoint por skill, até 14 no total. Usado quando o gestor pede explicitamente (cliente novo complexo, reposicionamento de marca, campanha institucional grande, oferta sensível, ou preferência de acompanhar passo a passo):

```
briefing-intake
briefing-diagnosis
brand-context-analysis
client-memory-builder
audience-persona-analysis
funnel-consciousness-mapping
reference-competitor-analysis
campaign-strategy-big-idea
offer-promise-analysis
framework-trigger-selector
copy-production
channel-format-adapter
copy-review-scorecard
final-delivery-feedback
```

## **Hard Constraints**

Restrições identificadas em qualquer ponto do fluxo (briefing, memória do cliente, correção do gestor) entram em um bloco único `HARD CONSTRAINTS`, consultado pelas skills de estratégia e produção. Violar uma restrição desse bloco reprova a copy automaticamente, independentemente da nota do scorecard.

## **Métricas de eficiência do processo**

Acompanhadas a partir do Teste 01 e dos testes comparativos do `PLANO-OTIMIZACAO-AGILIDADE.md` (seção 12 lá tem a tabela completa):

```
Checkpoints com o gestor (meta: ≤ 3 no modo Rápido, ≤ 2 no Express)
Perguntas críticas consolidadas em 1 rodada (não distribuídas)
Reescritas por restrição já conhecida (meta: 0)
Reescritas por adaptação de formato (meta: 0 ou 1)
Score final do scorecard (meta: ≥ 8,0)
Violação de hard constraint na entrega (meta: 0)
```

---

# **10\. Template de briefing usado como entrada**

O briefing atual será mantido como base, mas a THAMY IA deve reestruturar a informação internamente.

## **Campos atuais**

```
Doc de copy
Descrição da campanha e estratégia
Quantidade de designs
Tipo do criativo
Formato do criativo
Canal de tráfego
Objetivo
Público-alvo
Persona
Referência visual obrigatória
Restrições para o time criativo
Instagram
Site
LP
ID visual
Pasta do Drive
Notion
```

## **Campos mínimos para produção**

```
cliente
campanha
objetivo
canal
formato
público
estratégia da campanha
referência visual
links auxiliares
restrições
```

## **Campo normalmente faltante**

```
persona
```

Regra sugerida:

```
Se faltar persona, a THAMY IA cria uma persona operacional inferida com base no briefing, público e materiais disponíveis, sinalizando que é uma hipótese.
```

---

# **11\. Padrões de output por canal**

## **11.1 Criativo estático**

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

## **11.2 Carrossel**

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

## **11.3 Meta Ads**

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

## **11.4 Google Ads**

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

## **11.5 Landing Page**

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

## **11.6 WhatsApp**

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

## **11.7 E-mail**

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

## **11.8 Roteiro de vídeo/Reels**

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

---

# **12\. Estrutura do repositório**

```
thamy-ia/
│
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── CONTRATO-OPERACIONAL-MODOS.md
│
├── /briefings/
│   ├── briefing-template.md
│   ├── briefing-example-completo.md
│   └── briefing-example-incompleto.md
│
├── /knowledge/
│   ├── metodologia-thamy.md
│   ├── frameworks-copy.md
│   ├── padroes-copy-v4.md
│   ├── regras-por-canal.md
│   ├── banco-de-angulos.md
│   ├── banco-de-headlines.md
│   ├── termos-a-evitar.md
│   ├── exemplos-de-estruturas.md
│   └── erros-comuns.md
│
├── /clients/
│   ├── cliente-template.md
│   └── exemplos/
│
├── /skills/
│   ├── 01-briefing-intake/
│   │   └── SKILL.md
│   ├── 02-briefing-diagnosis/
│   │   └── SKILL.md
│   ├── 03-brand-context-analysis/
│   │   └── SKILL.md
│   ├── 04-client-memory-builder/
│   │   └── SKILL.md
│   ├── 05-audience-persona-analysis/
│   │   └── SKILL.md
│   ├── 06-funnel-consciousness-mapping/
│   │   └── SKILL.md
│   ├── 07-reference-competitor-analysis/
│   │   └── SKILL.md
│   ├── 08-campaign-strategy-big-idea/
│   │   └── SKILL.md
│   ├── 09-offer-promise-analysis/
│   │   └── SKILL.md
│   ├── 10-framework-trigger-selector/
│   │   └── SKILL.md
│   ├── 11-copy-production/
│   │   └── SKILL.md
│   ├── 12-channel-format-adapter/
│   │   └── SKILL.md
│   ├── 13-copy-review-scorecard/
│   │   └── SKILL.md
│   └── 14-final-delivery-feedback/
│       └── SKILL.md
│
├── /examples/
│   ├── approved/
│   ├── rejected/
│   ├── ai-vs-thamy/
│   ├── before-after/
│   ├── by-channel/
│   └── by-segment/
│
├── /outputs/
│   ├── drafts/
│   ├── approved/
│   └── revised/
│
└── /quality/
   ├── scorecard.md
   ├── approval-checklist.md
   ├── review-criteria.md
   └── feedback-template.md
```

---

# **13\. Arquivos principais**

## **`AGENTS.md`**

Usado para Codex.

Deve conter:

```
identidade da THAMY IA
objetivo
regras globais
fluxo operacional
lista de skills
critérios de qualidade
formato de entrega
regras de feedback
```

## **`CLAUDE.md`**

Usado para Claude Code.

Deve conter conteúdo semelhante ao `AGENTS.md`, adaptado como memória/instrução persistente do projeto.

## **`README.md`**

Deve ser simples para gestores.

Exemplo de uso:

```
1. Abra o projeto no Claude Code ou Codex.
2. Cole o briefing completo.
3. Use o comando /copy-final.
4. A THAMY IA vai diagnosticar, produzir e revisar a copy.
5. Aprove, reprove ou peça ajuste.
6. Quando aprovado, salve em /outputs/approved.
```

---

# **14\. Comandos recomendados**

## **Comando principal do MVP**

```
/copy-final
/copy-final --rapido
/copy-final --express
/copy-final --estrategico
```

Função:

```
Executa o fluxo da THAMY IA a partir do briefing colado no chat, no modo de operação indicado
(ou no modo Rápido por padrão, se nenhum for informado — ver seção 9).
```

## **Comandos secundários**

```
/copy-criativo
/copy-carrossel
/copy-meta
/copy-google
/copy-lp
/copy-whatsapp
/copy-email
/copy-video
/revisar-copy
/aprovar-copy
/reprovar-copy
```

Recomendação: no MVP, documentar todos, mas operacionalizar primeiro:

```
/copy-final
/revisar-copy
/aprovar-copy
/reprovar-copy
```

---

# **15\. Regras de decisão**

## **Quando perguntar antes de produzir**

A THAMY IA deve perguntar se faltar:

```
cliente
objetivo
canal
formato
campanha/ideia central
público
restrições
```

## **Quando pode inferir**

Pode inferir, sinalizando hipótese:

```
persona
tom de voz
dores
desejos
objeções
nível de consciência
framework
gatilho
figura de linguagem
CTA
```

## **Quando bloquear produção**

Deve bloquear ou pedir confirmação se:

```
a oferta estiver confusa
o objetivo estiver ausente
o canal não estiver definido
houver restrição sensível sem contexto
a promessa depender de dado não informado
o briefing estiver contraditório
```

---

# **16\. Scorecard de qualidade**

Cada copy deve ser avaliada de 0 a 10 nos critérios:

```
1. Clareza da headline
2. Força da headline
3. Aderência ao público
4. Clareza da subheadline
5. Força da promessa
6. Tradução de característica em benefício
7. Aderência ao canal
8. CTA claro
9. Tom de voz do cliente
10. Nível de especificidade
11. Conexão emocional
12. Risco de promessa exagerada
```

## **Regra de aprovação**

```
9 a 10: aprovado
8 a 8,9: aprovado com ajustes leves
7 a 7,9: revisar antes de entregar
abaixo de 7: refazer
```

Regra operacional:

```
A THAMY IA não deve entregar versão final com nota abaixo de 8.
```

---

# **17\. Sistema de feedback**

Após entregar a copy, a THAMY IA deve perguntar:

```
A copy foi aprovada, reprovada ou precisa de ajuste?
```

## **Se aprovada**

Registrar:

```
cliente
campanha
canal
formato
copy aprovada
motivo da aprovação
aprendizados
```

## **Se reprovada**

Perguntar motivo:

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

## **Se ajuste**

Gerar nova versão e registrar:

```
feedback recebido
ajuste feito
nova versão
aprendizado
```

---

# **18\. Base de conhecimento**

A base da THAMY IA deve conter:

```
1. Metodologia da Thamy.
2. Frameworks de copy.
3. Exemplos de copy boa.
4. Exemplos de copy ruim/genérica.
5. Comparativos IA antes vs Thamy depois.
6. Regras por canal.
7. Regras por formato.
8. Banco de headlines.
9. Banco de ângulos.
10. Termos a evitar.
11. Erros comuns.
12. Fichas por cliente.
```

## **Materiais prioritários para adicionar**

```
1. Documento cérebro da Thamy.
2. Workflow/processo dela.
3. Padrões de copy.
4. Frameworks usados.
5. Copies feitas pela Thamy.
6. Copies antigas feitas por IA.
7. Comparativos antes/depois.
8. Regras por canal/formato.
```

---

# **19\. Governança**

## **Responsável pela base**

```
Davi
```

## **Frequência de revisão**

```
quinzenal ou mensal
```

## **O que revisar**

```
1. Copies aprovadas.
2. Copies reprovadas.
3. Feedbacks dos gestores.
4. Novos padrões da Thamy.
5. Erros recorrentes.
6. Ajustes de scorecard.
7. Novos clientes.
8. Novas restrições.
```

---

# **20\. Critérios de sucesso do MVP**

O MVP será considerado bem-sucedido se:

```
1. Gestores conseguirem usar sem depender de conhecimento técnico avançado.
2. A THAMY IA gerar copy final com qualidade utilizável.
3. A entrega vier com variações e explicações.
4. A copy for mais específica do que uma IA genérica.
5. A metodologia da Thamy estiver visível no raciocínio.
6. A revisão reduzir erros antes da entrega.
7. O sistema conseguir aprender com aprovações/reprovações.
8. A operação ganhar velocidade.
9. A qualidade entre gestores ficar mais padronizada.
```

---

# **21\. Roadmap**

## **V1 — MVP operacional**

```
1 agent
14 skills
briefing via chat
base em Markdown
outputs manuais
feedback manual
memória por cliente em Markdown
```

## **V2 — Padronização avançada**

```
templates por canal
mais exemplos reais
fichas completas por cliente
comandos específicos por formato
comparativo IA vs Thamy
scorecard calibrado com feedback real
```

## **V3 — Automação e escala**

```
integração com Drive
consulta automática a materiais
base vetorial/RAG
interface simples para gestores
dashboard de aprovações
histórico de performance por copy
integração com processos internos
```

---

# **22\. Definição final do MVP**

```
Nome: THAMY IA
Tipo: Agent de copywriting estratégico
Arquitetura: 1 agent + 14 skills
Usuário inicial: gestor de projeto
Entrada: briefing colado no chat
Saída: copy final + variações + explicação + revisão
Base: metodologia da Thamy + frameworks + exemplos + memória por cliente
Ambiente: Claude Code e Codex
Governança: feedback dos usuários + revisão quinzenal/mensal
```

## **Resumo executivo**

A **THAMY IA** será um agent único, simples de usar e robusto por trás. O gestor cola o briefing, a IA organiza a demanda, entende marca, público, funil, referência, oferta e big idea, escolhe framework/gatilho/CTA, produz a copy final, adapta ao canal, revisa com scorecard e entrega variações com explicação.

A decisão mais importante do PRD é manter o MVP com **1 agent orquestrador e 14 skills modulares**, evitando complexidade técnica desnecessária e garantindo que o sistema seja utilizável por gestores de projeto desde o início.

