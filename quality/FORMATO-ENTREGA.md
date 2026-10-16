# Artefato de entrega e verificação

Python 3.10+; somente biblioteca padrão. O gestor continua recebendo copy legível. Estrutura JSON é interna, em `clients/{cliente}/campanhas/{campanha}/vN/`, ignorada no Git.

## Arquivos

- delivery.json: briefing/contexto, campos publicáveis, fontes/fatos/claims, restrições, requisitos e outline.
- review.json: assinatura da entrega, avaliações por trecho, checks, recibos e limitações.
- readings.json: recibos emitidos ao ler fontes. Copiar array para readings da revisão.
- final.md: texto exato renderizado após aprovação técnica; ainda depende de feedback humano.
- feedback.md: decisões humanas, versão e escopo.

Versões derivadas podem ter `revision` com hashes da entrega/revisão-pai, tipo da mudança, instrução literal e ids removidos/alterados. Para ajuste de escopo ou campo, seguir `knowledge/ajustes-incrementais.md`; o script cria `review.pending.json` e `review-delta.json` para evitar reescrever a revisão inteira.

`tests/fixtures/valid-delivery.json` é um exemplo técnico fictício de estrutura; não é referência de excelência editorial nem campanha real. Pode ser copiado e preenchido, retirando todos os dados fictícios.

## Campos

schema_version=2; client/campaign/version/route (`lp`, `social`, `ads`, `direct`). context tem objective, audience, barrier, value, voice, offer (necessária em lp/ads), hypotheses (lista), constraints_confirmed (boolean). Em LP, registrar também buyer_insights, narrative_thesis e title_ladder conforme `knowledge/narrativa-lp.md`; são campos internos e não aparecem automaticamente como texto publicável. buyer_insights é um objeto com current_situation, trigger, desired_outcome, alternative, barrier, decision_criteria e observed_language; cada item contém status (`confirmed`, `inferred` ou `missing`), text e source_ids. title_ladder lista os ids das headlines na ordem das dobras.

fields: lista não vazia de {id, section, role, text, max_chars?}. Todos os textos que vão para a peça precisam estar aqui, inclusive labels do formulário, CTA e legenda. role=form_label identifica rótulo do formulário; role=cta identifica ação. section é dobra/post/peça. max_chars só quando requisito real foi definido.

Nas novas produções, `context.editorial_plan` guarda o plano curto de `quality/DESENVOLVIMENTO-EDITORIAL.md`: argumento/valor, sustentação por ids existentes, voz e papéis dos campos ou peças. Objeto livre, sem duplicar outline, fontes ou fatos. É convenção de trabalho, não campo obrigatório do schema/verificador; não exige migração de entregas antigas. O hash de todo o contexto também o inclui. Ajustes localizados preservam a direção válida e não precisam preencher esse plano retroativamente.

sources: {id, locator, excerpt}; registrar data/localização adicional quando disponível. facts: {id, statement, status: confirmed|hypothesis|superseded, source_ids}. claims: {id, field_id, quote, fact_ids, limit}. quote é trecho literal do campo, fact_ids só apontam para fatos confirmados. Revisar também afirmações não numéricas; script não descobre todas as afirmações.

constraints: {id, rule, scope, source, forbidden_terms?, required_terms?, applies_to?}. `applies_to` seleciona `field_ids`, `sections`, `roles` ou `piece_ids` (listas de ids exatos, combinadas por interseção). Se houver termos e escopo diferente de global/cliente/campanha/entrega, o seletor é obrigatório. Termo obrigatório precisa aparecer em cada campo selecionado por id/role, ou ao menos uma vez em cada seção/peça selecionada. Sem seletor, termos globais valem para a entrega. Alvo inexistente bloqueia. Restrições semânticas continuam exigindo revisão.

outline: {id: section, question, new_information}. Obrigatório em LP/social. Em LP, registrar também function, evidence, transition e action para impedir dobras isoladas; social acrescenta source_ids, audience_value, asset e feasibility. requirements: sections opcional, forms opcional (objeto section→lista de rótulos na ordem). Em LP, prose_word_budget registra o máximo de palavras publicáveis, excluindo CTA, labels e opções de formulário; o padrão é 300. Valor maior exige prose_word_budget_reason. Condição de formulário/dobras deve vir do briefing, não ser alterada para o teste passar.

## Comandos internos

```bash
python3 scripts/read_context.py knowledge/README.md knowledge/metodologia-thamy.md knowledge/rotas/lp.md knowledge/narrativa-lp.md --phase context --receipts clients/cliente/campanhas/campanha/v1/readings.json
python3 scripts/read_context.py knowledge/vicios-ia-humanizacao.md --phase production --receipts clients/cliente/campanhas/campanha/v1/readings.json
# Escrever delivery.json; depois reler antes de revisar:
python3 scripts/read_context.py knowledge/vicios-ia-humanizacao.md --phase review --receipts clients/cliente/campanhas/campanha/v1/readings.json
python3 scripts/copycheck.py clients/cliente/campanhas/campanha/v1/delivery.json
python3 scripts/copycheck.py clients/cliente/campanhas/campanha/v1/delivery.json --review-template
# Salvar/preencher saída como review.json com notas reais, trechos, checks e readings.
python3 scripts/copycheck.py clients/cliente/campanhas/campanha/v1/delivery.json --review clients/cliente/campanhas/campanha/v1/review.json --render clients/cliente/campanhas/campanha/v1/final.md
```

Em ajuste incremental, primeiro executar `scripts/revise_delivery.py inspect`. A nova versão herda somente uma revisão-pai que ainda retorna `ready_for_human_approval`. Preencher o delta gerado e usar `merge`; o `copycheck.py` continua sendo a autoridade final de liberação e renderização.

O template sai pendente, nunca aprovado. A assinatura é SHA-256 da serialização canônica de TODO delivery, incluindo fatos, requisitos e contexto. Campos/claims alterados invalidam review. A revisão também registra hashes da rubrica e da política editorial; mudança em qualquer uma exige nova avaliação. O render exige arquivo de destino novo e não sobrescreve versão existente.

## Gate objetivo de 2026-10-09

- `gate_version` e `validator_sha256` identificam o verificador exato. Revisões antigas são preservadas como histórico; não autorizam novo render/ajuste sem revalidação atual. Nenhuma aprovação humana antiga é apagada ou recriada.
- O orçamento da LP conta TODOS os campos publicáveis, inclusive bullets, tabelas, passos, provas, transições e papéis novos. As únicas exclusões são `cta`, `form_label` e `form_option`. Não mudar o orçamento só para liberar uma página antiga.
- `field_checks` cobre todos os ids de fields. Cada decisão tem `status` (`mapped` ou `no_factual_claim`), `claim_ids` e justificativa. `mapped` lista exatamente os claims daquele campo. `no_factual_claim` só serve a campos sem claims e exige motivo específico. Um inventário vazio não dispensa revisar cada campo.
- `source_checks` cobre todos os ids de sources: `{status: pass, path, sha256, reason}`. `path` aponta para fonte textual UTF-8 preservada ou snapshot/extrato local; o hash precisa conferir e o excerto deve estar no texto, aceitando apenas normalização de espaços e caixa. Para PDF/imagem/Drive/web, preservar extrato legível, origem, data e localização; não fabricar snapshot como se fosse a fonte original.
- Integridade do arquivo não comprova origem, atualidade ou sustentação do claim. Esses pontos continuam sendo conferidos pelo revisor. Fontes não acessíveis deixam o gate pendente, em vez de receber uma comprovação inventada.
- A revisão incremental herda checks de fontes e campos intactos; campos alterados precisam de novo `field_checks` no delta. Mudança de fonte invalida a herança.

## Limites honestos

needs_editorial_review significa apenas que não houve bloqueio objetivo; não autoriza entrega final. ready_for_human_approval exige revisão registrada válida, mas não comprova que a avaliação semântica foi correta. O script não autentica quem revisou, não verifica a verdade no Drive, não substitui revisão de português nem certifica que um arquivo foi compreendido. O fluxo instrui o agent a usar o render; o chat do Codex/Claude não possui bloqueio técnico externo contra texto produzido fora desse caminho.

Se o usuário proibir salvar arquivos, fazer a análise no chat e não alegar gate técnico executado sem tê-lo feito. Não enviar JSON, hashes ou instruções internas ao público da campanha.

## Histórico de recuperação

O ciclo de `quality/CICLO-REVISAO.md` mantém snapshots novos em `review-cycle/attempt-NN/`. Cada tentativa inclui delivery, revisão, diagnóstico, resultado do gate recalculado e estado com hashes. `scripts/review_cycle.py` não modifica versões antigas nem registra aprovação humana. Diagnóstico é separado da copy publicável; somente a versão validada segue ao render.
