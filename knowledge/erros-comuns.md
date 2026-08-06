# Erros Comuns de Copy — Diagnóstico e Correção

> Baseline operacional do Copywriting Agent. Deve evoluir com feedback real registrado nas skills `13` e `14`. Não atribuir à Thamy um erro que não esteja documentado em fonte real.

## Erros de estratégia

| Erro | Sintoma | Correção |
|---|---|---|
| Pular pesquisa | Copy serviria para qualquer marca | Voltar às skills `03`, `05` e às fontes do cliente |
| Misturar objetivos | Peça tenta gerar awareness, lead e venda ao mesmo tempo | Definir um objetivo e um CTA principal |
| Confundir ângulo com framework | Escolher AIDA como se fosse a ideia da campanha | Definir tensão/ângulo primeiro; framework organiza a sequência |
| Falar com "todo mundo" | Linguagem neutra e benefícios amplos | Escolher persona operacional e situação específica |
| Ignorar consciência | Explicar o básico para quem já compara ofertas, ou vender cedo demais | Ajustar mensagem ao que o público já sabe |
| Criar oferta implícita | Leitor não entende o que recebe ou em quais condições | Explicitar objeto, condição e próximo passo |

## Erros de promessa e prova

| Erro | Sintoma | Correção |
|---|---|---|
| Feature sem benefício | Lista de funções | Completar: `isso permite que [público] [resultado]` |
| Benefício sem mecanismo | Promessa parece mágica | Explicar por que a oferta pode gerar o resultado |
| Prova decorativa | Selo, gráfico ou equipamento visual vira garantia implícita | Delimitar o que a prova demonstra e o que não demonstra |
| Extrapolar case | Um resultado vira promessa para todos | Usar linguagem de caso e informar contexto |
| Número sem fonte | Percentual/prazo não existe no briefing | Remover ou marcar `[DADO A CONFIRMAR]` |
| Escassez falsa | "Últimas vagas" sem limite real | Usar somente condição verificável |

## Erros de escrita

- Aquecimento antes do gancho.
- Headline e subheadline redundantes.
- Frases longas com muitas ideias e conectores.
- Adjetivos que substituem evidência.
- Falso contraste repetido (`não é X, é Y`).
- Tom neutro, sem ponto de vista.
- Repetição da mesma ideia em três formatos.
- Gíria inventada ou aplicada fora do público.
- Metáfora que exige mais esforço do que a mensagem literal.
- CTA genérico que não informa o próximo passo.

Usar `vicios-ia-humanizacao.md` para a avaliação completa de linguagem artificial.

## Erros de variação

- Trocar sinônimos e chamar de A/B/C.
- Mudar simultaneamente ângulo, oferta, CTA e formato, impossibilitando aprendizado.
- Criar uma variação deliberadamente fraca só para completar quantidade.
- Repetir a mesma headline em texto principal, título e criativo.
- Não identificar a hipótese testada.

Correção: usar `matriz-de-variacoes-e-testes.md`.

## Erros por canal/formato

### Estático

- Texto demais dentro da arte.
- Headline sem contexto mínimo e legenda incapaz de completar.
- CTA incompatível com o botão/destino.
- Mesmo dado repetido entre campos diferentes do criativo (ex.: subheadline e bullet 1 dizendo "emergencial em até 24h" com palavras diferentes) — cada campo (headline, subheadline, bullets, selo) precisa carregar informação nova; releia todos os campos juntos, como um bloco único, antes de apresentar.

### Carrossel

- Slide 1 genérico.
- Cada slide funciona isoladamente, mas não existe progressão.
- Repetir a mesma ideia em cinco telas.
- Último slide introduzir oferta que não foi preparada.

### Vídeo/Reels

- Silêncio ou contexto longo antes da fala.
- Locução descrever literalmente tudo que já aparece na tela.
- Roteiro incompatível com a duração.
- Prova visual narrada como garantia universal.
- CTA falado depois de o vídeo já parecer encerrado.

### Meta Ads

- Texto principal não acrescenta informação ao criativo.
- Variações sem diferença estratégica.
- Promessa forte demais para público frio.

### Google Ads

- Headline sem intenção de busca.
- Títulos que não funcionam em combinações diferentes.
- Claim sem correspondência na página de destino.

### E-mail

- Assunto promete algo que o corpo não entrega.
- Múltiplos CTAs concorrentes.
- Introdução longa antes do motivo do envio.

### WhatsApp

- Mensagem com aparência de disparo genérico.
- Parágrafo longo sem contexto ou permissão.
- CTA aberto demais (`me avisa`) quando o próximo passo poderia ser claro.

### Landing Page

- Hero não explica para quem é e qual valor entrega.
- Prova aparece sem ligação com a promessa.
- FAQ descreve recurso em vez de responder objeção.
- Seções repetem benefícios sem avançar a decisão.

## Erros de processo

- Produzir com campo crítico ausente.
- Esquecer de atualizar `HARD CONSTRAINTS` após correção do gestor.
- Alterar a copy depois do score e manter a nota anterior.
- Aprovar sem o Score de Humanização.
- Consultar arquivo placeholder como se fosse fonte real.
- Misturar hipótese `[H]` com fato validado.

## Como registrar um novo erro

```
Erro:
Etapa/skill:
Canal/formato:
Como apareceu:
Impacto:
Correção aplicada:
Regra preventiva:
Fonte: feedback do gestor | cliente | performance | revisão interna
```

## Registro — redundância entre campos de criativo estático

```
Erro: subheadline e bullet repetindo o mesmo dado com palavras diferentes ("Atendimento emergencial em até 24h" no subhead + "Emergencial em laboratório fixo ou móvel, em até 24h" no bullet 1)
Etapa/skill: 11-copy-production / 13-copy-review-scorecard
Canal/formato: criativo estático (Meta/LinkedIn), mas o princípio vale para qualquer formato com campos estruturados (headline/subheadline/bullets/selo)
Como apareceu: cada campo foi escrito "limpo" isoladamente, mas o mesmo fato (emergencial, 24h) foi comunicado duas vezes em campos diferentes — só ficou visível ao ler o criativo inteiro como um bloco único
Impacto: peça soou repetitiva mesmo sem nenhum vício de escrita dentro de cada campo individual; gestor reprovou pedindo explicitamente "sempre verifique antes a copy para não ser redundante"
Correção aplicada: bullet reescrito para trazer informação nova (opção fixo/móvel) em vez de repetir o dado do subhead
Regra preventiva: antes de apresentar qualquer criativo com campos separados, ler headline + subheadline + bullets + selo como texto corrido e perguntar "algum número, prazo, certificação ou característica aparece mais de uma vez com palavras diferentes?" — isso é checagem de redundância ENTRE campos, distinta da checagem de vício #6 (redundância dentro de um mesmo parágrafo) de `vicios-ia-humanizacao.md`. Repetir essa checagem a cada nova versão do criativo, não só na primeira escrita.
Fonte: feedback do gestor (Power Test, 2026-07-27) — ver `examples/rejected/powertest-topo-funil-calibracao-locacao-linkedin-meta-criativo1-v2.md`
```
