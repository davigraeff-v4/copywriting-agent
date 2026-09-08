# Copywriting Agent

Agent inspirado na metodologia da Thamy para produzir copy específica a partir de briefing, contexto do cliente e evidências. Funciona no Claude Code e no Codex, com **1 agent + 14 skills** e quatro rotas: landing page, social orgânico, anúncios e mensagens/e-mail.

A versão de 2026-09-08 reduz etapas obrigatórias, separa memória vigente de histórico e acrescenta revisão verificável. Frameworks ajudam a organizar um argumento quando necessário; não determinam a estrutura de toda peça.

## Requisitos e instalação

- Claude Code ou Codex configurado.
- Python 3.10+ para os verificadores locais; somente biblioteca padrão, sem instalação de pacotes, banco ou build.
- Fontes de cliente locais ou integração de Drive disponível no ambiente. O projeto não instala nem autentica um conector.

```bash
git clone https://github.com/davigraeff-v4/copywriting-agent.git
cd copywriting-agent
python3 -m unittest discover -s tests -v
```

Abra a pasta no Claude Code ou Codex. Eles usam respectivamente `CLAUDE.md` e `AGENTS.md`. Sem Python, o agent pode diagnosticar e rascunhar, mas deve indicar que a verificação objetiva está pendente.

## Uso diário

Cole o briefing ou peça a peça desejada. O agent consulta o estado do cliente, informa modo e rota, reúne lacunas materiais e propõe uma direção com o argumento e a função de cada seção ou pauta. Após autorização, entrega a copy revisada e registra seu feedback.

Exemplos de pedidos:

- “LP de cinco dobras, formulário na primeira, para cadastro de oficinas que ainda não conhecem a marca.”
- “Calendário de seis posts para seguidores. Use os bastidores disponíveis e explique o valor de cada pauta.”
- “Criativo estático com headline única. Preserve a restrição de nomenclatura do cliente.”
- “Revise esta copy e aponte o trecho e o motivo de cada problema.”

Você continua recebendo texto legível. Arquivos de contexto, revisões e verificações são trabalho interno do agent.

## Modos

| Modo | Quando usar | Interação |
|---|---|---|
| Rápido | Padrão | Até três checkpoints: lacunas, direção e entrega |
| Express | Cliente conhecido e demanda recorrente | Direção compacta e entrega |
| Estratégico | Quando você pedir construção passo a passo | Decisões pertinentes detalhadas |

As 14 skills são capacidades, não 14 pausas obrigatórias. Uma autorização explícita para executar sem pausa dispensa reconfirmação da direção naquela tarefa. Informação indispensável ausente ainda precisa ser resolvida. O contrato completo fica em `CONTRATO-OPERACIONAL-MODOS.md`.

## Comandos

| Comando | Comportamento |
|---|---|
| `/copy-final` | Inicia a partir do briefing; aceita `--rapido`, `--express`, `--estrategico` |
| `/copy-lp` | Argumentação de landing page |
| `/copy-social` ou `/calendario` | Pauta ou calendário orgânico |
| `/revisar-copy` | Crítica da versão atual, linguagem, argumento e fatos |
| `/aprovar-copy` | Registra aprovação expressa da versão revisada |
| `/reprovar-copy` | Registra motivo e aprendizado |

Esses comandos têm arquivos em `.claude/commands/`. No Codex funcionam como convenções de texto. `/copy-meta`, `/copy-google`, `/copy-criativo`, `/copy-carrossel`, `/copy-video`, `/copy-whatsapp` e `/copy-email` são convenções adicionais; canal e formato não determinam sozinhos o objetivo.

## Memória e contexto

- `clients/current/{cliente}.md`: estado consolidado, restrições com escopo e pendências de validade.
- `clients/{cliente}.md`: ficha legada e histórico preservado. Correções recentes prevalecem sobre um resumo desatualizado.
- `campaigns/{cliente}/{campanha}/vN/`: contexto, copy, revisão e feedback daquela versão.
- `examples/curated/`: referências anotadas por aspecto aproveitável; aprovação histórica não significa excelência ou performance comprovada.

Arquivos reais ficam locais, ignorados no Git. Um clone novo contém estrutura, templates e exemplos técnicos fictícios; não contém fichas e curadoria privadas desta máquina. Ver `clients/cliente-template.md` e `knowledge/memoria-clientes.md`.

## Como a qualidade é verificada

1. Argumento e pauta partem do briefing e de fatos selecionados. Cada dobra responde a uma pergunta; cada post precisa ter valor específico e produção viável.
2. `quality/editorial-policy.json` define bloqueios literais e alertas: abreviações coloquiais, travessões, falso contraste, sequências telegráficas e repetição entre campos.
3. `scripts/copycheck.py` confere estrutura, claims ligados a fontes, restrições, limites por campo e formulários. A revisão editorial precisa citar trechos exatos e registrar conferência factual.
4. O código calcula os scores. Mudança na copy, contexto, política ou rubrica invalida a revisão anterior. O texto final é renderizado da mesma versão revisada.
5. Aprovação humana, publicação e resultado de campanha são estados separados.

O verificador não certifica verdade, gramática completa ou preferência humana. O chat ainda depende de o agent cumprir o fluxo. Detalhes em `quality/FORMATO-ENTREGA.md` e `quality/scorecard.md`.

## Base de conhecimento e recuperação

`knowledge/README.md` roteia o núcleo atual, a metodologia original Thamy/V4, referências de mercado e convenções do agent. As fontes originais permanecem identificadas; escolhas editoriais atuais não são atribuídas à Thamy sem confirmação.

`scripts/retrieve.py` faz busca lexical em metadados, com filtro de cliente, rota e uso da referência. Não há banco vetorial nem sincronização automática do Drive. A consulta devolve caminhos relevantes para leitura, sem carregar toda a base ou transformar outro cliente em prova factual.

## Validação e avaliação

```bash
python3 scripts/validate_project.py
python3 -m unittest discover -s tests -v
```

`evals/README.md` documenta a comparação entre LLM simples, agent anterior e v2. Há 12 briefings sintéticos e ferramentas de embaralhamento e apuração humana. Testes técnicos aprovados não demonstram, por si, copy melhor. A comparação com o mesmo modelo e esforço e a calibração com avaliações humanas são a próxima validação editorial.

## Estrutura principal

```
AGENTS.md / CLAUDE.md           instruções sincronizadas
CONTRATO-OPERACIONAL-MODOS.md   decisões operacionais
skills/                        14 capacidades
knowledge/                     metodologia, rotas e recuperação
quality/                       política, rubrica e artefatos
scripts/                       verificação, leitura, busca e avaliação
tests/                         regressões e fixtures fictícias
evals/                         protocolo e casos controlados
clients/ campaigns/ examples/  contexto e histórico locais
.claude/commands/              atalhos do Claude Code
```

Não há interface própria, automação de publicação, múltiplos agents ou RAG vetorial. O projeto continua sem licença definida; considere todos os direitos reservados até sua inclusão.
