EXAMPLES=[]
def e(sid,title,route,tags,quote,locator,observation,reason,transfer,check,limits,kind='public_page',routes=None):
    EXAMPLES.append(dict(id=sid,title=title,kind='exemplo',primary_route=route,routes=routes or [route],tags=tags.split('|'),source_ids=[sid],quote=quote,locator=locator,observation=observation,reason=reason,transfer=transfer,check=check,limits=limits,evidence_kind=kind))

e('e01','Basecamp: mostrar a tarefa dentro do produto','lp','demonstração|software|mecanismo|tarefas|projeto',
'Manage projects, coordinate teams, and master your company with Basecamp.','Abertura e projeto demonstrativo Website Redesign Project',
'A página apresenta um projeto demonstrativo com quadros de mensagens, tarefas e responsáveis. A abertura nomeia gestão de projetos e coordenação de equipes. O objeto de uso aparece no próprio conteúdo da página, além da promessa comercial.',
'O aspecto aproveitável é a passagem da categoria para um trabalho reconhecível. Um comprador pode examinar onde uma tarefa, discussão ou prazo ficaria. Isso fornece matéria para explicar funcionamento sem depender de adjetivos. A demonstração pode responder perguntas que uma coleção de benefícios abstratos deixa em aberto.',
'Adaptação autoral: em uma LP de serviço de organização documental, mostrar um dossiê fictício com responsáveis, pendências e entregáveis. A primeira dobra identifica o serviço; a segunda apresenta um caso de uso; a terceira esclarece implantação e limites. O exemplo deve conter apenas recursos e etapas confirmados. Uma tela organizada demonstra organização da informação, sem provar redução de prazo ou erro.',
'Antes de usar, verificar se a demonstração corresponde ao produto vendido e se sua leitura depende de conhecimento prévio. Cada legenda precisa explicar uma ação real. O teste editorial é perguntar onde o interessado colocaria uma tarefa concreta depois de ver o exemplo.',
'Não importar superlativos, volumes de uso ou voz da Basecamp. A página foi observada em 09/10/2026; não houve acesso a resultados de conversão. Este é um recorte positivo de mecanismo, sem aprovação integral da página.')

e('e02','HEY: uma função explicada por uma escolha cotidiana','lp','mecanismo|email|controle|analogia|feature',
'Screen emails like you screen your calls','Seção The Screener',
'A página explica que o primeiro e-mail de um remetente passa pelo Screener e que o usuário decide se deseja recebê-lo. O título usa uma ação conhecida para apresentar uma função do produto.',
'A analogia escolhida reduz a distância entre o nome proprietário do recurso e uma decisão prática. O apoio descreve quem toma a decisão e quando. O aspecto útil é esse pequeno mecanismo completo, que permite imaginar uso, em vez de apenas declarar controle ou produtividade.',
'Adaptação autoral: para um sistema de aprovação de orçamento, explicar a ordem entre recebimento, avaliação e liberação. Uma comparação cotidiana pode ajudar quando corresponde à operação, mas o texto deve preservar quem aprova e o que permanece pendente. Se o recurso apenas encaminha pedidos, não escrever que ele decide ou impede toda compra incorreta.',
'O leitor deve conseguir descrever a função com suas palavras após o título e apoio. Revise se a analogia simplifica demais uma condição relevante. Se o termo proprietário ainda precisa de várias frases abstratas, mostrar um caso concreto costuma ser mais útil.',
'Não adotar os ataques a concorrentes nem tratar depoimentos selecionados como prova independente. Condições de teste gratuito e recursos da marca não se transferem para outro cliente. Análise textual, sem teste de eficácia.')

e('e03','Shopify: expansão comercial por contextos de venda','lp','ecommerce|canais|contexto|venda|arquitetura',
'Venda onde as pessoas compram. Online e presencialmente.','Bloco de canais de venda',
'A página brasileira desenvolve a venda em diferentes canais e traz blocos para operação internacional, checkout e públicos de portes diferentes. O trecho selecionado identifica dois contextos de uso antes de detalhar soluções.',
'O ponto aproveitável é desdobrar uma promessa ampla em lugares ou situações onde ela acontece. Para uma pessoa que já vende presencialmente, a conexão com outros canais tem um significado diferente da primeira loja. Esses contextos podem orientar páginas específicas e a escolha de exemplos.',
'Adaptação autoral: uma distribuidora com retirada local e entrega pode organizar a página por modalidades confirmadas de atendimento. Uma seção responde como retirar; outra explica onde e em que condições recebe pedidos para entrega. Em anúncios, cada modalidade ganha mensagem compatível com o destino. Não transformar a presença de vários canais em promessa de aumento de vendas.',
'Confira se cada contexto tem uma resposta própria e um próximo passo pertinente. Se todas as seções terminam com o mesmo parágrafo genérico sobre crescer, falta explicar a operação. Verifique também se o anúncio está levando ao contexto que prometeu.',
'A abertura e recursos podem mudar. Não reutilizar números, tecnologias ou benefícios internacionais da Shopify como fatos do cliente. Fragmentação de frases é observada na fonte, mas a adaptação precisa respeitar a cadência e o português do projeto.')

e('e04','Notion: casos de uso tornam IA mais concreta','lp','IA|casos de uso|tarefas|demonstração|conhecimento',
'Automatize os relatórios semanais','Lista Veja o que o Notion pode fazer',
'A página combina uma apresentação de espaço de trabalho com IA com tarefas como triagem de feedbacks, tickets de suporte e relatórios semanais. O recorte observado é a lista de trabalhos concretos, não a headline geral.',
'Nomear uma tarefa reconhecível ajuda o público a avaliar onde um produto abstrato entraria na rotina. O verbo sozinho, como automatizar, é insuficiente; o objeto da ação torna a ideia examinável. Uma lista desse tipo pode abrir caminhos diferentes de demonstração, sem exigir que cada visitante deseje todos os recursos.',
'Adaptação autoral: uma ferramenta de atendimento pode mostrar a preparação de um resumo de chamados para a reunião semanal. A explicação distingue o que é extraído, o que é revisado por uma pessoa e qual informação entra no relatório. Esse recorte oferece um argumento verificável; “IA que revoluciona seu negócio” não explica nenhuma dessas etapas.',
'Para cada tarefa citada, confirme se há capacidade real, condições de uso e amostra autorizada. Pergunte o que o usuário precisa fornecer e como confere a saída. A presença de IA não permite assumir precisão factual, disponibilidade ilimitada ou autonomia total.',
'Não importar rankings, depoimentos ou funcionamento do Notion. O exemplo ensina concreção de tarefa, sem recomendar reproduzir a voz ou promessa de funcionamento contínuo da marca. Performance comercial não foi medida.')

e('e05','Conta Azul: colaboração descrita por dados e destinatário','lp','ERP|contador|financeiro|colaboração|especificidade',
'Compartilhe dados com o contador em tempo real.','Recurso Conexão com Contador',
'A página apresenta gestão financeira e módulos de operação. O trecho escolhido nomeia a informação compartilhada e quem a recebe. Esse detalhe é mais examinável que uma promessa isolada de gestão eficiente.',
'A colaboração ganha significado porque há objeto e interlocutor. Um dono de empresa pode relacionar o recurso à troca de informações com a contabilidade. O aprendizado editorial é explicar a interação que a funcionalidade permite, mantendo o alcance exato do que está documentado.',
'Adaptação autoral: em uma LP de portal de fornecedores, indicar quais documentos podem ser enviados e quem os consulta. O título pode apresentar a troca; o apoio explica acesso, responsáveis e atualização conforme o produto. Uma imagem fictícia pode mostrar um envio. Não concluir que o contador deixará de precisar de outros documentos ou que conformidade fiscal está garantida.',
'Conferir o que significa tempo real no produto, quais permissões são necessárias e se o recurso pertence ao plano anunciado. O agent precisa encontrar o limite operacional, não apenas repetir a frase mais simpática. A revisão também separa recurso de eventual resultado financeiro.',
'Não importar relatos de clientes, condições fiscais ou afirmações abrangentes da página. O recorte positivo é uma descrição de interação. Os benefícios da marca continuam declarações do anunciante, sem auditoria independente.')

e('e06','RD Station CRM: contexto de trabalho e ação reconhecível','lp','CRM|WhatsApp|mecanismo|adoção|rotina',
'Envie propostas, crie tarefas e acompanhe suas negociações sem sair do WhatsApp.','Bloco de CRM para WhatsApp',
'O bloco situa o CRM dentro do WhatsApp Web e nomeia ações de negociação, como proposta e tarefa. A página tem também seções de funil, planos e integrações.',
'O trecho aproveitável responde a uma questão de adoção: em que lugar o vendedor trabalha com o recurso. As ações tornam a integração mais concreta que uma afirmação genérica de conexão. Isso permite construir um argumento sobre continuidade da rotina sem alegar automaticamente ganho de receita.',
'Adaptação autoral: se um sistema envia pedidos a partir da interface já usada pela equipe, mostre essa sequência. O anúncio pode nomear a tarefa; a LP demonstra entrada, confirmação e registro. Para prometer permanência no mesmo ambiente, confirme todas as etapas necessárias e suas exceções. Não esconder uma configuração obrigatória que muda a experiência.',
'Peça que um leitor identifique onde começa a ação e onde encontra seu histórico. Uma prova por captura deve mostrar exatamente o recurso explicado. Várias funções no mesmo título só ajudam quando formam uma sequência reconhecível; caso contrário, escolha a ação central.',
'Não reutilizar percentuais de vendas, garantias de contexto preservado ou estatísticas de conversão da página. Recorte positivo de mecanismo; o texto da fonte contém escolhas de cadência que não se tornam regra editorial local.')

e('e07','Nuvemshop: caminhos diferentes por ponto de partida','lp','segmentação|migração|ecommerce|origem|jornada',
'Já vende em redes sociais','Navegação Soluções para cada necessidade',
'A navegação diferencia quem começa do zero, migra de plataforma, vende em redes sociais ou já tem loja física. A página também apresenta planos e soluções relacionadas à operação.',
'O aspecto útil é segmentar pela situação atual. Isso produz perguntas de decisão concretas: começar, integrar ou migrar. Uma categoria demográfica genérica de empreendedor não explicaria essas diferenças. O mesmo produto pode ter direções de copy distintas quando o ponto de partida muda.',
'Adaptação autoral: uma assessoria pode criar caminhos para primeira implantação e reorganização de um processo existente. Cada caminho apresenta os dados necessários, o que é aproveitado e o que será analisado. Um anúncio para migração não deveria levar a uma página que só explica como iniciar do zero. A promessa continua dependente da capacidade real do serviço.',
'Confira se os caminhos têm conteúdo diferente e se o formulário registra a situação pertinente. Se a segmentação muda apenas o título, o público ainda terá de descobrir sozinho o que serve para ele. Verificar também o custo e os limites de migração quando relevantes.',
'Não transportar números de marcas atendidas, preços ou promessa de crescimento. A arquitetura é observada, sem acesso à navegação dos usuários ou sua eficácia. Título aspiracional não foi eleito modelo de especificidade.')

e('e08','Airbnb: começar, decidir e entender condições','lp','serviço|onboarding|fricção|FAQ|condições',
'Começar é gratuito. Você define seu preço','Bloco Vale a pena e dúvidas de anfitriões',
'A página para anfitriões explica criação de anúncio, definição de preço, cobrança posterior e perguntas de preparação. Também distingue modalidades de proteção e remete a exclusões.',
'O recorte positivo é responder perguntas do ingresso no serviço: o que custa começar, que decisão permanece com a pessoa e quais condições precisam ser lidas. Uma promessa de renda, isolada, não explica essas etapas. A ordem das respostas pode diminuir incerteza sobre a participação, sem garantir resultado.',
'Adaptação autoral: para um marketplace profissional, separar cadastro, aprovação e eventual cobrança. A headline pode identificar a oportunidade; o apoio explica o primeiro passo; uma seção de condições informa taxas e responsabilidade. Use somente regras reais da oferta. Se há estimativa, descreva sua natureza e condições, mantendo-a fora de uma garantia de receita.',
'O leitor deve distinguir iniciar um cadastro de já operar ou já ganhar dinheiro. Confira se condições materiais ficam perto da promessa pertinente. Campos dinâmicos que não carregaram não são evidência de valor, disponibilidade ou simulação concluída.',
'Não importar projeções de ganho, cifras de proteção ou regras de taxa. Proteção não equivale automaticamente a seguro ou ausência de risco. A análise considera o texto acessível; não houve teste do simulador nem contratação do serviço.')

e('e09','QuintoAndar: entregável tangível perto do cadastro','lp','imóvel|serviço|formulário|entregável|fotografia',
'Fotos profissionais gratuitas para o seu anúncio','Lista Benefícios de anunciar no QuintoAndar',
'A página de proprietários apresenta um cadastro e uma lista de benefícios que inclui fotos profissionais e uma ferramenta de preço. O recorte escolhido é um entregável que o interessado consegue imaginar.',
'Um serviço fica mais concreto quando o texto mostra o que será produzido. Fotos para o anúncio são um objeto verificável; praticidade e segurança exigem explicação adicional. A lista pode ajudar o público a comparar componentes da oferta, desde que condições de cada um permaneçam claras.',
'Adaptação autoral: uma agência de apresentação de imóveis pode nomear os materiais realmente incluídos, como fotografias, planta ou descrição. A copy esclarece quantidade e escopo quando isso faz diferença. Um CTA de envio dos dados do imóvel deve corresponder ao processo confirmado, sem transformar um cadastro inicial em promessa de venda.',
'Conferir se gratuidade depende de contrato, região ou elegibilidade. Identificar separadamente a ação do formulário e a adesão a conteúdos. O texto deve permitir entender o primeiro passo e o que será necessário depois, sem antecipar uma aprovação inexistente.',
'Não importar garantias de aluguel, posição de mercado ou disponibilidade regional. A fonte é comercial e as condições precisam de consulta atual para uso real. A unidade não avalia o desempenho do formulário.')

e('e10','SumUp: escolhas por modalidade de recebimento','lp','pagamento|celular|modalidade|produto|decisão',
'Aceite pagamentos por aproximação usando apenas o celular','Seção Tap to Pay',
'A página organiza soluções para venda presencial e online, incluindo maquininha, Pix e uso do celular. O trecho selecionado associa a modalidade de pagamento a um dispositivo reconhecível.',
'O aspecto útil é explicar uma escolha operacional. Quem vende precisa entender como recebe, quais recursos utiliza e quais condições se aplicam. Um dispositivo específico dá corpo a uma promessa abstrata de facilidade. O texto pode abrir espaço para uma demonstração adequada ao cenário de venda.',
'Adaptação autoral: uma solução de pedidos pode distinguir atendimento no balcão e envio de link remoto. Cada modalidade recebe uma descrição de uso e requisito. A headline de um anúncio deve escolher a modalidade pertinente. Não afirmar que qualquer celular funciona ou que o recurso é gratuito quando isso depende de aparelho, sistema ou condições comerciais.',
'A revisão busca requisitos técnicos e limites da modalidade escolhida. O agent deve separar ausência de compra de um equipamento de ausência de tarifas, porque são afirmações diferentes. CTA, destino e recurso precisam corresponder.',
'Não reutilizar taxas, condições de gratuidade ou atributos de segurança. A análise trata da redação de modalidade e não constitui recomendação financeira. A existência pública da página não prova resultado de campanha.')

e('e11','Wise: utilidade descrita por operações','lp','conta internacional|operações|verbo e objeto|clareza|escopo',
'A conta internacional para enviar, converter e usar dinheiro na moeda local.','Descrição da conta na navegação',
'A descrição identifica uma conta internacional e três operações. A página também inclui condições financeiras e produtos que variam por contexto.',
'O recorte escolhido explica a categoria por ações que a pessoa reconhece. Os verbos têm objeto e situação, permitindo distinguir a conta de uma promessa genérica de liberdade. Essa técnica ajuda quando um produto tem vários usos e precisa de uma apresentação curta sem esconder sua natureza.',
'Adaptação autoral: para um serviço de gestão de documentos, nomear receber, conferir e arquivar documentos por processo. O apoio precisa dizer quais documentos, que conferência é feita e quem pode consultar. Se a função não está disponível em todos os planos, a abertura não deve sugerir acesso irrestrito. O objetivo é tornar a categoria compreensível, sem acumular benefícios imaginados.',
'Teste se a pessoa consegue apontar uma tarefa que faria com a oferta e uma condição que precisa confirmar. A lista de operações deve formar um conjunto coerente. Verificar verbos que ampliam escopo para garantir ou resolver tudo.',
'Não transportar taxas, impostos, rendimentos, autorização regulatória ou comparações econômicas da marca. Este é um estudo de expressão e escopo, sem orientação de investimento e sem prova de conversão.')

e('e12','Slack: recurso apresentado por uma situação de ausência','lp','colaboração|resumo|situação|IA|rotina',
'Receba o resumo de uma conversa da qual você não participou','Lista de usos da IA',
'A página em português apresenta equipe e agentes e detalha ações. O trecho selecionado define o recurso a partir de uma conversa que o usuário não acompanhou.',
'A situação é reconhecível e delimita a utilidade do resumo. O leitor não precisa imaginar sozinho o significado de colaboração inteligente. Esse recorte mostra como transformar uma categoria ampla de tecnologia em uma pergunta concreta de rotina, sem atribuir emoção ao usuário.',
'Adaptação autoral: uma ferramenta de reunião pode mostrar o resumo para quem não esteve presente, incluindo origem das informações e necessidade de revisão. A headline identifica a tarefa; o corpo esclarece como o conteúdo é obtido. Se o sistema não cobre todas as conversas ou não identifica decisões automaticamente, essas condições precisam permanecer claras.',
'Conferir se a demonstração apresenta a origem do resumo e se a promessa sugere uma completude não documentada. A pergunta editorial é quais informações a pessoa pode esperar encontrar, não qual adjetivo faz a IA parecer mais avançada.',
'Não importar estatísticas, recursos futuros, comparações com concorrentes ou confiança atribuída à IA. O recorte não endossa todo o texto, que contém construções de contraste incompatíveis com o padrão local.')

e('e13','Dropbox Replay: nome do produto com tarefa identificada','lp','vídeo|revisão|aprovação|categoria|microcopy',
'Revise e aprove vídeos mais rápido','Descrição do Replay na navegação de produtos',
'A página diferencia produtos por tarefas, incluindo armazenamento, assinatura e revisão de vídeo. O Replay recebe uma descrição de revisar e aprovar vídeos.',
'O aspecto positivo é a identificação da tarefa ao lado de um nome proprietário. Um menu pode ajudar o público a reconhecer qual solução procurar, mesmo antes de ler a página completa. A descrição curta também oferece uma base para a direção: o que será demonstrado deve ser revisão e aprovação, não produtividade abstrata.',
'Adaptação autoral: uma empresa com vários serviços pode nomeá-los por entregável ou uso, como revisão de desenho e organização de documentação. Na página específica, explique quem revisa, o que é registrado e como ocorre a aprovação. Não transformar uma simples descrição do menu em prova de que o processo é mais rápido.',
'Separe a identificação clara da tarefa da alegação comparativa. Revisar e aprovar informa função; mais rápido precisa de base e referência. Em uma adaptação sem evidência de tempo, manter a função e retirar a comparação. Essa distinção é um bom exercício para o gate factual.',
'Não importar a promessa de velocidade, integrações ou condições do produto. Fonte observada na navegação; não houve teste do software. A unidade ensina descrição de tarefa, sem eleger a frase inteira como copy pronta.')

e('e14','Apple acessibilidade: ação específica com opções e limites','lp','acessibilidade|leitura|recurso|condição|explicação',
'Personalize e resuma artigos complexos com facilidade.','Bloco Leitor de Acessibilidade',
'O bloco descreve opções de fonte, cor, espaçamento e leitura em voz alta. A página também inclui observações de disponibilidade por recurso, região e idioma.',
'O aspecto aproveitável é desenvolver uma promessa por escolhas de uso. Opções específicas ajudam o interessado a imaginar a experiência e avaliar se ela atende sua necessidade. A condição de disponibilidade precisa acompanhar a compreensão da oferta; uma descrição geral não deve apagar suas exceções.',
'Adaptação autoral: para uma ferramenta de leitura de documentos, mostrar os controles que existem e o que cada um permite ajustar. A copy não precisa prometer transformação pessoal nem deduzir benefícios clínicos. O apoio pode explicar tipos de arquivo compatíveis, sem afirmar acessibilidade universal a partir de uma única função.',
'A revisão distingue facilidade, que é uma percepção, das funções demonstradas. Verifique também requisitos de aparelho e versão antes de usar a informação em campanha. Um exemplo visual não substitui testes com pessoas que tenham necessidades diferentes.',
'Não reutilizar linguagem de diagnóstico, disponibilidade ou prazos de configuração. Estudo de descrição de recurso, sem aconselhamento médico nem certificação de acessibilidade. O texto da marca não comprova desempenho para outro produto.')

e('e15','Netflix: ação de cadastro explicada ao lado do campo','lp','cadastro|formulário|próximo passo|FAQ|fricção',
'Informe seu email para criar ou reiniciar sua assinatura.','Apoio do formulário de e-mail',
'O apoio do campo explica que o e-mail inicia ou retoma a assinatura. A página contém ainda dúvidas sobre preço, dispositivos e cancelamento.',
'O ponto positivo é esclarecer a função do dado solicitado. Isso é mais informativo que um botão genérico acompanhado por frases de entusiasmo. A explicação pode ajudar o visitante a distinguir o primeiro passo do cadastro de uma compra já concluída.',
'Adaptação autoral: em uma LP que pede modelo de equipamento, informar que o dado será usado para verificar compatibilidade. Em uma página de orçamento, explicar o contato e as informações necessárias, conforme o processo real. O texto junto ao campo deve dizer o que ocorre após enviar, sem inventar tempo de resposta.',
'Pergunte se o visitante entende para que serve o campo e se o botão descreve uma ação compatível. Depois compare o texto com o fluxo real. Um formulário de contato não deve ser apresentado como contratação automática. Dúvidas frequentes precisam esclarecer condições, sem repetir a headline.',
'Não reutilizar preços, catálogo, disponibilidade de download ou política de cancelamento. A frase foi transcrita com a grafia da fonte; adaptações usam o português do projeto. Não houve envio do formulário nem análise de abandono.')

e('e16','Hotmart: portfólio distinguido por objeto de venda','lp','portfólio|produto digital|escopo|categoria|oferta',
'Crie, venda e escale seus produtos digitais, físicos e serviços','Bloco de tipos de produto',
'A página apresenta tipos de oferta e exemplos como cursos, e-books e mentorias, junto de recursos comerciais. O recorte selecionado identifica objetos de venda e desenvolvimento.',
'O aspecto útil é dar materialidade a um portfólio amplo. A enumeração pode ajudar a pessoa a localizar o que pretende oferecer. Para copy específica, porém, o próximo nível é escolher um desses objetos e explicar a operação correspondente, em vez de repetir a abrangência em todas as dobras.',
'Adaptação autoral: uma empresa que atende vários tipos de projeto pode abrir caminhos por entregável. A página de um curso esclarece aulas e suporte; a de uma consultoria, escopo e encontros. Em anúncios, escolher um objeto por peça permite mostrar um mecanismo pertinente. Não concluir que qualquer oferta escalará ou terá vendas desde o primeiro dia.',
'Verifique se a enumeração corresponde ao que o cliente realmente atende e se cada caminho tem condições próprias. Se a headline do anúncio inclui todo o portfólio e o destino só trata de um item, revise a promessa ou o destino.',
'Não importar faturamento, histórias de produtores ou promessas de ganho imediato. A abertura comercial da página não foi adotada como modelo. O recorte positivo é identificação de portfólio, sem validação de performance.')

e('e17','IKEA planejamento: preparativos tornam o serviço concreto','lp','serviço|planejamento|preparação|entregável|orçamento',
'Measure and list.','Etapas How IKEA planning services work',
'A página americana explica escolha do serviço, agendamento, medições e materiais para a conversa. Descreve planos, listas de produtos e estimativas para áreas distintas da casa ou empresa.',
'O recorte mostra que uma LP de serviço pode persuadir explicando o trabalho. Pedir medidas e preferências torna a consulta concreta e indica participação do interessado. Nomear entregáveis ajuda a diferenciar uma conversa inicial de um projeto pronto ou uma compra concluída.',
'Adaptação autoral: um serviço de mobiliário sob medida pode explicar envio de medidas, avaliação do espaço e elaboração de proposta. A copy esclarece o que o interessado leva e o que recebe em cada etapa. Se a medição presencial depende de região ou cobrança, essa condição deve aparecer no lugar pertinente.',
'A revisão procura correspondência entre título, processo e entregável. Um orçamento não pode ser chamado de projeto executivo se isso não integra o serviço. O CTA deve indicar a etapa que inicia, e os materiais pedidos precisam ser necessários para ela.',
'Condições gratuitas, durações e modalidades pertencem ao serviço americano observado. Não se aplicam automaticamente ao Brasil ou a outro cliente. Não houve agendamento nem prova de efeito sobre conversão.')

e('e18','Patagonia: provocação sustentada por ações concretas','ads','campanha|sustentabilidade|coerência|posição|prova',
'Don’t Buy This Jacket','Artigo da marca sobre o anúncio de 25/11/2011',
'A marca contextualiza um anúncio de Black Friday que convidava a consumir com mais atenção. O artigo associa a posição a reduzir, reparar, reutilizar e reciclar, reconhecendo também a tensão de vender produtos.',
'O recorte positivo é a sustentação da provocação. A headline não vive só de surpresa: existe uma posição que orienta ações. Para uma campanha com argumento incomum, o corpo precisa mostrar o que a empresa faz e qual comportamento propõe. A contradição real exige explicação, em vez de uma fórmula de falso contraste.',
'Adaptação autoral: se uma assistência técnica oferece avaliação e reparo antes de uma substituição, pode explicar esse processo e seus limites. A direção pode valorizar a decisão informada, sem copiar a headline negativa. O serviço precisa existir e a comunicação deve esclarecer quando reparar não é adequado ou possível.',
'Confirme se a prática sustenta a posição e se o CTA leva a uma ação existente. Um slogan sustentável sem mecanismo ou evidência vira apenas um adjetivo. A análise deve distinguir relato da marca, interpretação editorial e fatos de impacto ainda não auditados.',
'Fonte histórica, com notas posteriores. Não reproduzir cifras ambientais ou atribuir aumento de vendas à headline. Não recomendar provocação negativa por padrão. Recorte de coerência entre posição e ação, sem certificação ambiental.', 'documented_campaign')

e('e19','Dove Sketches: insight transformado em construção visual','ads','insight|filme|demonstração narrativa|marca|emoção',
'Real Beauty Sketches','Página do trabalho da Ogilvy, equipe São Paulo',
'A agência descreve uma campanha construída sobre diferenças entre a percepção da própria aparência e a percepção de outra pessoa. O insight organiza a construção do filme e sua mensagem de marca.',
'O aspecto aproveitável é transformar uma ideia de pesquisa em uma situação visual, em vez de narrar um benefício genérico por cima de imagens. A construção permite que o público acompanhe uma diferença. Ela não é um teste científico do produto nem uma prova universal sobre autoestima.',
'Adaptação autoral: um produto de organização pode demonstrar duas maneiras reais de localizar um documento, com o mesmo pedido e condições transparentes. O roteiro mostra ações verificáveis e deixa a conclusão limitada à demonstração. Não é necessário inventar insegurança do público ou prometer mudança emocional profunda para ter uma narrativa.',
'O insight precisa estar ligado ao cliente e ao público atuais. Revise se o roteiro permite observar a ideia e se a comparação é justa. Uma encenação não pode ser apresentada como depoimento espontâneo ou pesquisa independente.',
'Não importar o percentual de pesquisa citado, afirmações de impacto cultural ou rankings de visualização. A fonte é da agência responsável. O recorte ensina construção narrativa, sem aprovação integral da mensagem e sem causalidade de vendas.', 'documented_campaign')

e('e20','Mercedes-Benz: tradução de um assunto técnico para outro público','ads','B2B|técnico|mobilidade|participação|insight',
'Engenheiros do Futuro','Ficha Effie 2019, prêmio indicado como Shortlist',
'A ficha descreve o desafio de aproximar chassis de ônibus do público que usa transporte. A campanha recorreu à imaginação de crianças, visualização 3D e participação dos fãs. O registro do prêmio é Shortlist.',
'O aspecto útil é perceber que um atributo conhecido pelo especialista pode ser desconhecido por outro público. Mudar a representação pode ajudar a introduzir o assunto, desde que o produto continue reconhecível. A criatividade aqui organiza a compreensão e a participação, em vez de apenas adornar uma lista de características.',
'Adaptação autoral: uma empresa de componentes pode mostrar onde sua peça aparece em um sistema completo. Para compradores técnicos, preservar especificações; para público institucional, explicar o papel do componente por um uso observável. Não transferir a mesma peça para todos os públicos sem ajustar a pergunta de entrada.',
'Identifique qual público recebe cada conteúdo e o que ele deve compreender. Confirme o componente representado e se a visualização exige produção ainda indisponível. Participação pública precisa de processo real de seleção e uso de contribuições.',
'Os resultados pertencem ao relato submetido, sem auditoria independente ou atribuição isolada à copy. Não chamar a campanha de vencedora. A unidade não comprova superioridade tecnológica nem reaproveita claims do anunciante.', 'documented_campaign', ['ads','social'])

e('e21','AdeS: eixo criativo ligado ao objeto da oferta','ads','campanha|produto|eixo criativo|repertório|alimentos',
'O poder das sementes','Ficha Effie 2019, título do case',
'O relato conecta o lançamento de bebidas vegetais a um eixo de sementes e descreve desafios de categoria e confiança. O registro do case está marcado como Shortlist.',
'O aspecto aproveitável é a escolha de um elemento do próprio produto para organizar a campanha. Um eixo criativo pertinente pode reunir peças distintas sem reduzir todas à repetição de um slogan. O significado emocional, porém, não comprova valor nutricional ou benefício individual.',
'Adaptação autoral: para uma coleção de cerâmica artesanal, um eixo sobre a matéria pode apresentar modelagem, textura e uso das peças, desde que o processo esteja documentado. Cada anúncio desenvolve uma informação própria. Uma imagem de origem natural não autoriza dizer que o produto é mais saudável, seguro ou sustentável.',
'Pergunte se o eixo vem da oferta e se comporta desdobramentos com substância. Se todas as peças apenas repetem a metáfora, falta conteúdo. Revise separadamente qualquer conclusão nutricional, ambiental ou de superioridade introduzida na adaptação.',
'Não importar alegações sobre transgênicos, saúde, crise da marca ou métricas de Brand Lift. A narrativa da inscrição não é evidência científica. Recorte positivo de organização criativa, com reserva factual explícita.', 'documented_campaign')

e('e22','Spotify Wrapped: dado pessoal convertido em história','ads','personalização|campanha|identidade|dados|compartilhamento',
'Minutes Listened','Descrição pública da experiência Wrapped 2025',
'A página de lançamento explica histórias baseadas no histórico de escuta, cartões de compartilhamento e requisitos de elegibilidade. O dado de uso é apresentado em uma experiência personalizada.',
'O aspecto útil é dar significado a uma informação que pertence à experiência da pessoa. A comunicação pode gerar reconhecimento porque mostra um comportamento real, em vez de inserir o nome do destinatário em um texto genérico. A substância está no dado e na maneira de organizá-lo.',
'Adaptação autoral: um aplicativo de estudo pode apresentar uma retrospectiva de atividades efetivamente registradas, com período e critérios claros. A copy explica o que foi contabilizado e oferece compartilhamento opcional. Não inventar conquistas, posições em ranking ou identidade pessoal a partir de dados incompletos. Ausência de informação deve permanecer ausência.',
'Verifique a origem dos dados, o intervalo e a interpretação de cada cartão. Separar engajamento de aprendizado evita exagero: tempo de atividade não comprova domínio de uma matéria. O leitor precisa poder reconhecer o dado e controlar sua exposição.',
'Análise do lançamento 2025, sem previsão sobre edições futuras. A rota ads é usada como repertório de campanha e expressão; não houve observação de um anúncio pago específico. Não transferir métricas de público ou eficácia.', 'documented_campaign', ['ads','social','direct'])

e('e23','Shot on iPhone: resultado visível sustenta uma capacidade','ads','demonstração|câmera|asset|prova visual|campanha',
'One Night on iPhone 7','Apple Newsroom, campanha anunciada em 30/01/2017',
'A Apple descreve fotógrafos que registraram cenas noturnas para uma campanha associada à câmera do iPhone 7. O artigo identifica situações, autores e condições de captura, incluindo recursos auxiliares em alguns registros.',
'O recorte positivo é escolher uma capacidade e mostrá-la em resultados identificáveis. A copy dá contexto ao que a imagem demonstra. Uma fotografia atraente, sem origem e condições, não seria prova suficiente da capacidade de um equipamento específico.',
'Adaptação autoral: uma fabricante de iluminação pode mostrar um ambiente com o produto identificado e condições conhecidas. A legenda informa modelo e configuração pertinente. Se houve edição, luz adicional ou preparação especial, a explicação não pode sugerir que o resultado ocorre automaticamente em qualquer instalação.',
'A revisão precisa rastrear produto, autoria e condições do asset. Não usar uma imagem de banco como demonstração real do cliente. Se o resultado depende de habilidade profissional, não prometer a mesma execução a qualquer usuário apenas por possuir o produto.',
'Campanha histórica; especificações não são recomendações atuais de aparelho. A unidade não importa percentuais de desempenho nem rankings de uso. Nenhuma imagem foi baixada ou reutilizada; análise baseada no relato textual da fabricante.', 'documented_campaign')

e('e24','LEGO Ideas: participação com objetivo e condição definidos','social','comunidade|participação|UGC|regra|pertencimento',
'What is LEGO® Ideas?','Explicação do programa na página oficial',
'A página explica ideias de produtos sugeridas por fãs e caminhos para consideração de produção, como apoio da comunidade ou seleção em desafio. Consideração não significa produção garantida.',
'O aspecto útil é vincular participação a um objeto e um processo. O público entende o que pode criar e qual etapa vem depois. Isso é diferente de pedir interação só para elevar uma métrica. Uma proposta participativa precisa esclarecer regras e expectativas, inclusive o que não está garantido.',
'Adaptação autoral: uma marca pode convidar clientes a enviar usos de um produto para uma seleção editorial. A pauta define o tipo de contribuição, critérios e autorização de uso. O conteúdo posterior apresenta os selecionados com contexto real. Não prometer fabricação, prêmio ou destaque para toda participação se esse resultado não estiver previsto.',
'Confira se a contribuição é viável para o público e se existe capacidade de analisar o material. Regras, autorização e seleção devem estar determinadas antes da chamada. O agent não pode inventar comentários ou histórias para simular comunidade.',
'Os limiares e processos da LEGO pertencem ao programa atual observado e não se transferem. A unidade usa um programa público como repertório social, sem afirmar desempenho de um post específico.', 'public_program', ['social'])

e('e25','IKEA ideias: pauta editorial por uma tarefa doméstica','social','pauta|casa|organização|tutorial|produto em uso',
'Maximize even the smallest of spaces with these tips and tricks','Seção Small spaces na página de ideias',
'A página organiza inspirações por ambiente, armazenamento e espaços pequenos. Também descreve um caso de garagem reorganizada com soluções identificáveis.',
'O recorte positivo é a pauta ligada a uma tarefa cotidiana. O conteúdo pode ter valor porque ajuda a observar espaço e organização, sem depender de uma promoção. Nomear o ambiente dá direção a fotos, explicações e sequência; apenas anunciar um estilo de vida deixaria o trabalho editorial mais vago.',
'Adaptação autoral: uma loja de móveis pode mostrar como comparar dimensões de circulação ao escolher uma peça. O carrossel começa com uma situação, apresenta a medição necessária, mostra um exemplo autorizado e fecha com uma orientação pertinente. Cada slide acrescenta informação. Não prometer ampliar fisicamente o imóvel ou resolver todos os espaços com um produto.',
'Verifique se fotos e medidas sustentam a orientação. Uma dica precisa poder ser executada e ter condições claras. O produto entra quando explica a solução, sem ocupar o lugar da informação em cada slide.',
'A página é um hub editorial, não um post de rede social analisado em performance. Não importar preço de consulta, medidas ou resultados do caso como dados do cliente. Recorte de pauta aplicável à rota social.', 'editorial_page', ['social'])

e('e26','Nubank explica Pix: pergunta que organiza conteúdo','social','educação|pergunta|produto|clareza|conteúdo',
'O que é Pix?','Subtítulo do guia Pix: tudo sobre o meio de pagamentos instantâneos',
'O guia usa perguntas para organizar definição, funcionamento e formas de uso. A página foi atualizada e combina informação educativa com recursos do produto da marca.',
'O aspecto positivo é começar por uma pergunta real de compreensão e avançar para usos. Esse tipo de pauta não precisa transformar dúvida em sofrimento. Uma definição só tem valor editorial quando ajuda a entender a próxima escolha e mantém distinção entre conceito geral e função específica de uma empresa.',
'Adaptação autoral: um negócio de manutenção pode explicar o que é uma inspeção preventiva, quais itens abrange e o que o relatório informa. Um carrossel separa conceito, exemplo de verificação e limite do serviço. A última parte oferece um próximo passo compatível com a informação entregue. Não atribuir resultado garantido ao simples entendimento do conceito.',
'Conferir termos, datas e fontes técnicas quando a explicação for usada em campanha real. Separar a educação geral da oferta evita sugerir que uma funcionalidade de um fornecedor é inerente a toda categoria. A revisão procura informação nova em cada bloco.',
'Análise de organização editorial, sem aconselhamento financeiro. Não importar regras, tarifas ou estatísticas do Pix. Hub e artigo são fontes de pauta; não há prova de desempenho de uma peça social.', 'editorial_page', ['social'])

e('e27','Duolingo: objetivo de hábito com ações executáveis','social','hábito|tutorial|pauta|rotina|educação',
'Keep a record of the new words you learn.','Dica 10 do artigo de manutenção de sequência',
'O artigo reúne sugestões para manter uma rotina de aprendizagem, agrupadas por motivação e contexto. Uma dica propõe registrar palavras aprendidas para acompanhar o percurso.',
'O recorte útil é desenvolver uma intenção ampla por ações executáveis. Incentivar consistência, sozinho, não oferece matéria suficiente para um post. A pauta ganha substância quando apresenta uma atividade e explica seu uso, sem fazer do hábito uma promessa universal de resultado.',
'Adaptação autoral: uma marca de materiais de desenho pode propor um registro de estudos com data, técnica e observação. Um post mostra como organizar esse registro usando um exemplo fictício identificado. A legenda explica por que comparar anotações pode ajudar a acompanhar o trabalho. Não prometer evolução profissional em um prazo fixo.',
'A ação precisa caber na rotina proposta e ser compreensível sem um tutorial oculto. Confira se o asset realmente mostra a atividade. Ao converter em carrossel, escolher uma dica desenvolvida pode ser melhor que condensar uma lista longa em slides sem explicação.',
'O artigo foi publicado em 2022 para uma rotina específica. Não importar pressões por sequência perfeita, incentivos de assinatura ou previsões de aprendizado. A unidade usa conteúdo editorial como referência de pauta, sem mensuração social.', 'editorial_page', ['social'])

e('e28','Boas-vindas Freckle: contexto da conta e primeiro uso','direct','email|onboarding|boas-vindas|conta|próximo passo',
'Freckle','Exemplo de boas-vindas descrito no guia da Postmark',
'A Postmark descreve um e-mail da Freckle com dados da conta, plano, data de criação e caminhos de ajuda. O exemplo é documentado pela plataforma de e-mail, não recebido por nós na caixa de entrada.',
'O aspecto positivo é combinar acolhimento com informação de referência e uma ação inicial. Usar o nome da pessoa não basta para tornar uma mensagem útil. O conteúdo precisa corresponder ao evento que aconteceu e oferecer uma orientação compatível com a experiência.',
'Adaptação autoral: após um cadastro confirmado, um serviço pode explicar como acessar a área e qual primeiro dado completar. Informação da conta deve vir de um registro autorizado. O corpo separa próximo passo e ajuda, evitando apresentar todos os recursos de uma vez. Não enviar senhas ou dados sensíveis por e-mail como forma de parecer pessoal.',
'Verifique evento de disparo, destinatário, acesso e destino. A mensagem deve permanecer compreensível em texto e orientar uma ação real. Cadastro iniciado e cadastro concluído são estados distintos; não afirmar sucesso antes de ele ocorrer.',
'Não transcrevemos o corpo completo do e-mail nem testamos seu desempenho. A evidência é uma descrição secundária identificada e publicada pela Postmark. O recorte de boas-vindas continua sujeito ao contexto do serviço atual.', 'documented_email', ['direct'])

e('e29','Friend Streak: lembrete ligado a um compromisso aceito','direct','notificação|lembrete|consentimento|contexto|ação',
'Start a Friend Streak today!','Artigo oficial de lançamento e descrição dos lembretes',
'O artigo explica que a participação na sequência compartilhada depende da aceitação do convite. Descreve o acesso ao status e a possibilidade de enviar lembretes aos amigos.',
'O aspecto útil é a relação entre lembrete e compromisso conhecido. Uma mensagem direta tem mais contexto quando o destinatário reconhece o evento que a originou. O próximo passo se refere à mesma atividade, em vez de introduzir uma promoção sem relação com o que a pessoa combinou.',
'Adaptação autoral: um lembrete de preparação para atendimento pode retomar uma etapa acordada, como envio de medidas. A mensagem identifica o agendamento real e explica o dado pendente. Não dizer que o cliente prometeu algo se não existe registro. A intensidade deve ser adequada à marca, sem copiar pressão social ou culpa como mecanismo.',
'Conferir aceitação, estado e data antes de personalizar. Se a atividade já foi concluída, o lembrete está errado mesmo com texto elegante. O botão deve levar ao lugar pertinente e não exigir que a pessoa refaça uma etapa conhecida.',
'A fonte descreve uma funcionalidade e seu lançamento; não coletamos notificações privadas. Não importar números de adesão ou associação a conclusão de aula como efeito causal da copy. Repertório de comunicação contextual.', 'documented_notification', ['direct','social'])

e('e30','Verve Wine: suporte dentro de uma mensagem transacional','direct','email|transacional|suporte|acesso|clareza',
'Verve Wine','Exemplo de recuperação de senha no guia da Postmark',
'O guia descreve um e-mail da Verve Wine com opções de suporte no rodapé da recuperação de senha. Também discute mensagens quando a solicitação não foi feita pelo destinatário e a validade do link.',
'O aspecto útil é resolver a tarefa principal e prever uma dificuldade pertinente. Uma mensagem transacional pede clareza de ação e contexto; a personalidade da marca não deve esconder a orientação. Suporte acessível é informação funcional, diferente de um encerramento genérico de agradecimento.',
'Adaptação autoral: uma confirmação de orçamento pode informar como corrigir dados ou pedir esclarecimento, com canais reais. O próximo passo continua sendo a avaliação do orçamento. Não inserir um catálogo inteiro ou uma venda cruzada que rouba atenção da tarefa. Em mensagens de acesso, validade e procedimentos precisam vir da configuração real, nunca de uma invenção do redator.',
'Teste se a ação principal é identificável e se a ajuda resolve uma situação prevista. Verifique se o contato funciona e se a instrução de ignorar uma mensagem seria realmente adequada ao processo. A copy depende do fluxo técnico e do estado da conta.',
'Descrição secundária publicada pela Postmark, sem acesso à caixa de entrada ou teste de segurança. A unidade trata de orientação textual, sem prescrever uma implementação de recuperação de senha nem copiar seu corpo.', 'documented_email', ['direct'])
