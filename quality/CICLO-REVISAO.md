# Ciclo de revisão antes da aprovação humana

Contrato: seção 7 de `CONTRATO-OPERACIONAL-MODOS.md`. Um agent conduz escrita e julgamento. `scripts/review_cycle.py` registra tentativas e aplica limites; não chama modelos, não autentica julgamentos humanos e não publica.

## Entrada e orçamento

Uma entrega com direção autorizada inicia um ciclo. São permitidas a versão inicial e até duas reescritas por direção. Mudanças de argumento dentro da direção autorizada consomem o mesmo orçamento. Trocar o nome da versão ou direção não reinicia a contagem. Ao esgotar, apresentar uma alternativa concreta; nova direção exige decisão explícita do gestor, salvo autorização específica já existente. Não encadear ciclos automaticamente.

Erros do próprio registro da revisão têm orçamento separado de até duas correções no ciclo inteiro. Corrigir revisão significa preservar texto/contexto; se mudar matéria-prima ou copy, é reescrita. Nunca repetir julgamento até obter uma nota conveniente.

## Execução pelo agent

1. Produzir a primeira versão, revisar pela skill 13 e executar o verificador real com essa versão e revisão. O revisor recebe as mesmas fontes, excertos e ressalvas disponíveis ao escritor. Referências editoriais não comprovam fatos de cliente.
2. Se passar, registrar `ready_for_human_approval`, renderizar a versão exata pela skill 14 e solicitar aprovação. O ciclo não registra aprovação humana.
3. Se bloquear, diagnosticar com trecho/critério e próxima ação: escrita, direção, evidência/contexto ou revisão. Registrar o problema, ids afetados, mudanças propostas e se o contexto disponível permite resolver. Dados ausentes precisam ser nomeados.
4. Escrita/formato: corrigir os campos afetados; direção: rever tese/função/sequência antes do corpo, preservando o escopo autorizado. Evidência: consultar a fonte específica, limitar ou retirar claim quando possível. Revisão: conferir o aparente falso positivo antes de mudar texto correto.
5. Criar nova versão, preservar anteriores, renovar revisão e assinatura e executar novamente o gate. Não elevar nota por ter realizado uma tentativa. Conferir regressões, inclusive nos campos preservados.
6. Executar até duas reescritas. Se o mesmo defeito permanecer, não insistir em sinônimos: reconsiderar argumento dentro do orçamento. Dado indispensável ou decisão fora do escopo interrompe imediatamente as tentativas dependentes, com encaminhamento concreto.

`blocked` é resultado de uma tentativa, não encerramento sem resposta. O ciclo retorna `needs_revision`, `needs_review_repair`, `needs_input`, `needs_direction`, `needs_review_decision` ou `ready_for_human_approval`. `needs_input` identifica o dado/fonte; `needs_direction` apresenta o impedimento e a alternativa sustentada; `needs_review_decision` apresenta a evidência divergente. Somente o último estado de prontidão libera render final.

## Registro local

Usar uma pasta `review-cycle/` da campanha ou ensaio. Primeira chamada:

```sh
python3 scripts/review_cycle.py CAMINHO/review-cycle --case-id IDENTIFICADOR --direction-id DIRECAO-AUTORIZADA --delivery CAMINHO/v1/delivery.json --review CAMINHO/v1/review.json --diagnosis CAMINHO/v1/diagnosis.json
```

Em tentativa que passou, omitir diagnóstico. Em bloqueio, `diagnosis.json` registra `category` (`writing`, `direction`, `evidence`, `context`, `review`), `reason`, `field_ids`, `changes`, `next_step`, `can_fix_with_available_context` e `missing_information`. É diagnóstico editorial explícito, não inferência automática de causalidade pelo código.

Nas próximas chamadas, reutilizar a mesma pasta, sem recriar o ciclo. O script lê o estado mais recente. Cada `attempt-NN/` preserva delivery, review, diagnóstico, resultado recalculado e estado; hashes encadeiam o histórico e detectam alteração dos snapshots. O agente executa a próxima ação retornada, sem pedir confirmação para uma correção já autorizada. Nenhum daemon ou chamada de modelo é instalado pelo script.

Revisão ausente/desatualizada exige reparo; arquivo com nota maior não basta para provar melhora. O controlador garante orçamento e rastreabilidade, não a validade do julgamento. Preservar a versão reprovada mesmo quando houver aprovação posterior.

## Saída após esgotamento ou lacuna

Mostrar: última versão como rascunho, critério/claim ainda pendente, tentativas e mudanças realizadas, dado/decisão necessário e proposta concreta de continuação. Não promover o rascunho a entrega final. No benchmark, relatar também sucesso na primeira tentativa, falhas recorrentes, falsos positivos, consultas ao banco/RAG e pendências de assets. Aprovação técnica e aprovação humana permanecem separadas.

## Retomada quando o dado chega

`needs_input` pode ser retomado na mesma pasta quando houver fonte nova/atualizada preservada e orçamento restante. Passar `--resolution CAMINHO/resolution.json`, com `kind: new_information`, `reason` concreto e `source_ids` existentes no novo delivery. O controlador exige mudança de contexto/texto, confere que a fonte foi acrescentada/atualizada e consome uma reescrita do orçamento já existente. Mantém histórico e contador; não aceita fonte idêntica ou desconhecida como pretexto para reavaliar a mesma peça.

Orçamento já esgotado ou mudança de direção não é liberado por esse recurso. Requer encaminhamento e decisão explícita para novo trabalho; não iniciar outro ciclo automaticamente. Hash detecta mudança de registro, não autentica verdade nem aprovação do gestor.

Antes de consumir uma reescrita, confrontar o diagnóstico com os erros efetivos do gate. Se a revisão editorial não aponta falha material e o erro é de mapeamento/representação do artefato, corrigir essa representação e renovar a assinatura, preservando texto e evidências. Não mandar o escritor lapidar uma frase por causa de uma contagem incorreta do adaptador. Registrar erros de infraestrutura separados de falhas editoriais.
