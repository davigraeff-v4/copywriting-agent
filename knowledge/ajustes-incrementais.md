# Ajustes incrementais de copy

Usar quando já existe uma versão da campanha e o gestor pede correção, corte ou mudança localizada. O objetivo é preservar decisões válidas e revisar somente o impacto real da alteração.

## Interpretar antes de executar

Converter a instrução mais recente em quatro itens internos:

1. Formatos ou peças mantidos.
2. Formatos ou peças removidos.
3. Campos que podem mudar.
4. Campos que devem permanecer idênticos.

Exemplos de interpretação:

- `somente feed, stories não são necessários`: remover as seções de Story; manter os campos de Feed e o texto de plataforma, salvo instrução contrária.
- `ajuste somente a headline`: modificar a headline indicada; preservar apoio, selo, CTA e texto de plataforma.
- `deixe somente a headline na arte`: remover da arte apoio, selo e demais campos; não remover automaticamente o texto da plataforma.
- `somente headline`: se o contexto não mostrar se é alvo da edição ou único campo da entrega, perguntar uma vez antes de alterar.

Antes de agir, responder em uma linha: `Ajuste entendido: [mudança]; [conteúdo preservado].` Isso é confirmação de entendimento, não pedido de aprovação.

## Classificação

### Escopo

Remove formato, peça ou campo sem alterar os textos mantidos. Exemplos: retirar Stories, entregar só Feed, remover uma variação. Não refazer pesquisa, estratégia, pacote de contexto ou leitura integral da base. Derivar a nova versão com `scripts/revise_delivery.py`.

### Campo localizado

Altera texto de campos identificados sem mudar público, oferta, fatos, argumento central ou restrições. Reutilizar contexto e revisar o campo alterado, seus claims e a coerência com a peça. Não reescrever campos fora do alvo.

### Estratégico ou factual

Muda objetivo, público, oferta, argumento, fonte, claim, restrição ou direção criativa. Voltar às skills pertinentes e executar revisão completa. Não chamar de ajuste simples para evitar o gate.

Feedback como `genérica`, `argumento fraco`, `tom errado` ou `não representa o cliente` indica problema editorial amplo, mesmo quando o gestor aponta uma frase como exemplo. Reavaliar a direção antes de fazer troca cosmética.

## Revisão derivada

O script aceita somente uma versão-pai cuja revisão atual esteja válida. Ele cria nova entrega, revisão pendente e delta pequeno. Campos mantidos precisam ser byte a byte idênticos. Critérios cuja evidência sumiu e critérios globais afetados ficam pendentes; os demais são herdados da revisão válida.

Fluxo:

```bash
python3 scripts/revise_delivery.py inspect campaigns/cliente/campanha/v1/delivery.json
python3 scripts/revise_delivery.py prepare campaigns/cliente/campanha/v1/delivery.json campaigns/cliente/campanha/v1/review.json change.json campaigns/cliente/campanha/v2
# preencher somente review-delta.json
python3 scripts/revise_delivery.py merge campaigns/cliente/campanha/v2/review.pending.json campaigns/cliente/campanha/v2/review-delta.json campaigns/cliente/campanha/v2/review.json
python3 scripts/copycheck.py campaigns/cliente/campanha/v2/delivery.json --review campaigns/cliente/campanha/v2/review.json --render campaigns/cliente/campanha/v2/final.md
```

`change.json` para corte de escopo:

```json
{
  "kind": "scope",
  "version": "v2",
  "instruction": "Somente Feed; remover Stories",
  "remove_sections": ["conceito-1-story-9x16", "conceito-2-story-9x16"]
}
```

Para texto localizado, usar `kind: "field"` e `replace_fields` como objeto `field_id: novo texto`. Se o campo tiver claim cujo trecho deixou de existir, informar `claim_updates` ou classificar a mudança como factual/estratégica. O script nunca escolhe novo fato por conta própria.

## Limites

- Só usar na mesma conversa ou quando a instrução de ajuste e a versão-pai estiverem inequívocas.
- Política ou rubrica alterada invalida a herança e exige revisão completa.
- Não registrar nova memória do cliente para remoção técnica de formato. Registrar apenas decisão persistente confirmada, com escopo.
- Não reler Drive, internet ou toda a base para corte de escopo ou correção localizada sem fato novo.
- Não apresentar novamente estratégia, fontes e justificativas que não mudaram. Entregar o resultado alterado e uma nota curta do que foi preservado.
