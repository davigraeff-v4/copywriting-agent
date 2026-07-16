# Scorecard de Qualidade — THAMY IA

Usado pela skill `13-copy-review-scorecard`. Baseado no checklist de revisão pós-copy da Thamy. A revisão gera **dois scores independentes e obrigatórios**: Score Geral e Score de Humanização/Anti-Vícios de IA. A média geral nunca compensa uma copy com sinais fortes de escrita artificial.

## 1. Score Geral — 12 critérios (0 a 10 cada)

1. **Clareza da headline**
2. **Força da headline**
3. **Aderência ao público** — a persona certa se reconheceria nessa copy?
4. **Clareza da subheadline**
5. **Força da promessa**
6. **Tradução de característica em benefício** — nenhuma característica ficou solta sem virar benefício
7. **Aderência ao canal** — respeita a lógica/limite do formato
8. **CTA claro**
9. **Tom de voz do cliente** — coerente com `clients/{cliente}.md` / `03-brand-context-analysis`
10. **Nível de especificidade** — cita produto, público e dor reais, não é intercambiável com outra marca
11. **Conexão emocional**
12. **Risco de promessa exagerada** — nota alta = baixo risco; validar claims com `knowledge/provas-e-claims.md` quando aplicável

**Cálculo:** média aritmética dos 12 critérios.

## 2. Score de Humanização/Anti-Vícios de IA — 8 dimensões

Antes de pontuar, releia integralmente `knowledge/vicios-ia-humanizacao.md`. Avalie cada dimensão com a régua `0 = falha clara`, `5 = parcial/inconsistente`, `10 = atende`:

1. **Ponto de vista** — a copy se posiciona, sem neutralidade ou evasivas artificiais.
2. **Especificidade ancorada** — usa produto, situação, dado ou exemplo real do briefing; nunca inventa evidência.
3. **Substância acima de adjetivos** — troca adjetivos vagos e hipérboles por benefício, prova ou cena concreta.
4. **Conectores naturais** — não empilha "além disso", "portanto", "ou seja" ou estruturas repetidas.
5. **Entrada direta** — começa pelo gancho, tensão, benefício ou promessa, sem aquecimento.
6. **Oralidade humana** — lida em voz alta, soa como uma pessoa daquele público e daquela marca.
7. **Ausência de palavras-bandeira** — não usa a lista negra nem clichês estruturais como muleta.
8. **Ritmo e variedade** — alterna tamanho/estrutura de frases e evita circularidade, listas excessivas e cadência mecânica.

**Cálculo:** média aritmética das 8 dimensões. O score deve ser apresentado separadamente; não entra na média do Score Geral.

## 3. Vícios críticos — reprovação automática

Reprove e reescreva a versão, independentemente dos scores, quando houver:

- dado, prova, resultado ou exemplo inventado para gerar falsa especificidade;
- abertura inteira de aquecimento antes de entregar valor;
- palavra/expressão da lista negra usada como muleta central da peça;
- dois ou mais dos 12 vícios de `knowledge/vicios-ia-humanizacao.md` aparecendo de forma recorrente.

## Régua de aprovação

| Nota | Decisão |
|---|---|
| 9 a 10 | Aprovado |
| 8 a 8,9 | Aprovado com ajustes leves |
| 7 a 7,9 | Revisar antes de entregar |
| Abaixo de 7 | Refazer |

## Gates de entrega e aprovação

A versão só pode ser entregue ou aprovada quando cumprir **todos** os gates:

- Score Geral ≥ 8/10;
- Score de Humanização/Anti-Vícios de IA ≥ 8/10;
- zero vício crítico;
- zero violação de `HARD CONSTRAINTS`;
- Knowledge Gate concluído para a versão atual.

Falhou em qualquer gate → reescreva internamente e recalcule os dois scores antes de mostrar ao gestor.

## Checklist headline/subheadline/CTA (base da revisão pós-copy da Thamy)

- [ ] Headline chamativa
- [ ] Headline clara
- [ ] Headline conversa com o público certo
- [ ] Subheadline clara e explicativa
- [ ] CTA claro
- [ ] CTA direciona para o objetivo certo
- [ ] Comunicação atraente
- [ ] Evita termos repelentes (ver `knowledge/termos-a-evitar.md`)
