# Artefato de entrega e verificação

Python 3.10+; somente biblioteca padrão. O gestor continua recebendo copy legível. Estrutura JSON é interna, em `campaigns/{cliente}/{campanha}/vN/`, ignorada no Git.

## Arquivos

- delivery.json: briefing/contexto, campos publicáveis, fontes/fatos/claims, restrições, requisitos e outline.
- review.json: assinatura da entrega, avaliações por trecho, checks, recibos e limitações.
- readings.json: recibos emitidos ao ler fontes. Copiar array para readings da revisão.
- final.md: texto exato renderizado após aprovação técnica; ainda depende de feedback humano.
- feedback.md: decisões humanas, versão e escopo.

`tests/fixtures/valid-delivery.json` é um exemplo técnico fictício de estrutura; não é referência de excelência editorial nem campanha real. Pode ser copiado e preenchido, retirando todos os dados fictícios.

## Campos

schema_version=2; client/campaign/version/route (`lp`, `social`, `ads`, `direct`). context tem objective, audience, barrier, value, voice, offer (necessária em lp/ads), hypotheses (lista), constraints_confirmed (boolean). Contexto nunca aparece automaticamente como texto publicável.

fields: lista não vazia de {id, section, role, text, max_chars?}. Todos os textos que vão para a peça precisam estar aqui, inclusive labels do formulário, CTA e legenda. role=form_label identifica rótulo do formulário; role=cta identifica ação. section é dobra/post/peça. max_chars só quando requisito real foi definido.

sources: {id, locator, excerpt}; registrar data/localização adicional quando disponível. facts: {id, statement, status: confirmed|hypothesis|superseded, source_ids}. claims: {id, field_id, quote, fact_ids, limit}. quote é trecho literal do campo, fact_ids só apontam para fatos confirmados. Revisar também afirmações não numéricas; script não descobre todas as afirmações.

constraints: {id, rule, scope, source, forbidden_terms?, required_terms?}. Termos automáticos valem para toda a entrega; restrição contextual precisa de check semântico, não termo amplo proibido indevidamente.

outline: {id: section, question, new_information}. Obrigatório em LP/social; social acrescenta source_ids, audience_value, asset e feasibility. requirements: sections opcional, forms opcional (objeto section→lista de rótulos na ordem). Condição de formulário/dobras deve vir do briefing, não ser alterada para o teste passar.

## Comandos internos

```bash
python3 scripts/read_context.py knowledge/README.md knowledge/metodologia-thamy.md knowledge/rotas/lp.md --phase context --receipts campaigns/cliente/campanha/v1/readings.json
python3 scripts/read_context.py knowledge/vicios-ia-humanizacao.md --phase production --receipts campaigns/cliente/campanha/v1/readings.json
# Escrever delivery.json; depois reler antes de revisar:
python3 scripts/read_context.py knowledge/vicios-ia-humanizacao.md --phase review --receipts campaigns/cliente/campanha/v1/readings.json
python3 scripts/copycheck.py campaigns/cliente/campanha/v1/delivery.json
python3 scripts/copycheck.py campaigns/cliente/campanha/v1/delivery.json --review-template
# Salvar/preencher saída como review.json com notas reais, trechos, checks e readings.
python3 scripts/copycheck.py campaigns/cliente/campanha/v1/delivery.json --review campaigns/cliente/campanha/v1/review.json --render campaigns/cliente/campanha/v1/final.md
```

O template sai pendente, nunca aprovado. A assinatura é SHA-256 da serialização canônica de TODO delivery, incluindo fatos, requisitos e contexto. Campos/claims alterados invalidam review. A revisão também registra hashes da rubrica e da política editorial; mudança em qualquer uma exige nova avaliação. O render exige arquivo de destino novo e não sobrescreve versão existente.

## Limites honestos

needs_editorial_review significa apenas que não houve bloqueio objetivo; não autoriza entrega final. ready_for_human_approval exige revisão registrada válida, mas não comprova que a avaliação semântica foi correta. O script não autentica quem revisou, não verifica a verdade no Drive, não substitui revisão de português nem certifica que um arquivo foi compreendido. O fluxo instrui o agent a usar o render; o chat do Codex/Claude não possui bloqueio técnico externo contra texto produzido fora desse caminho.

Se o usuário proibir salvar arquivos, fazer a análise no chat e não alegar gate técnico executado sem tê-lo feito. Não enviar JSON, hashes ou instruções internas ao público da campanha.
