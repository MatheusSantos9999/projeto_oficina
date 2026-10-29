<<<<<<< HEAD
# Oficina mecânica

Projeto de uma oficina mecânica em Python, desenvolvido para aplicar estruturas de dados ao acompanhamento de um serviço: cadastro do cliente, entrada do veículo, diagnóstico, orçamento, uso de peças, execução e pagamento.

## Problema e objetivo

Uma oficina precisa relacionar cada veículo ao seu proprietário, organizar a espera e acompanhar o que acontece durante o reparo. A ordem de atendimento deve respeitar as prioridades, enquanto o consumo de peças precisa considerar o saldo disponível e os lotes recebidos. O diagnóstico, o orçamento e o pagamento pertencem à mesma visita e precisam permanecer associados.

O sistema organiza esse fluxo por meio de ordens de serviço. Cada ordem identifica o veículo atendido, preserva o diagnóstico e os preços do orçamento, registra os lotes consumidos e controla as etapas até a quitação. As regras impedem situações como executar o mesmo serviço duas vezes, consumir apenas parte de um pedido que não pode ser atendido ou concluir um reparo com peças aguardando remontagem.

O objetivo da atividade é implementar essas relações usando listas encadeadas, filas, pilhas e árvores próprias. Os dados são fictícios e ficam em memória durante a execução.

## Organização do projeto

O código está dividido por responsabilidade. A interface recebe os comandos do usuário; os cadastros mantêm os registros; as classes de serviço e estoque aplicam as regras de cada operação.

| Arquivo ou pasta | Responsabilidade |
|---|---|
| `main.py` | Ponto de entrada único; chama a aplicação |
| `interface/` | Menu, leitura de entradas, apresentação dos dados e demonstração automática |
| `cliente/` | Dados dos clientes e operações de cadastro e consulta |
| `oficina/` | Veículos, componentes, avaliações, diagnósticos e composição dos responsáveis |
| `servico/` | Atendimento, ordens de serviço, itens e pagamentos |
| `estoque/` | Produtos, lotes, pedidos e registros de consumo |
| `estrutura_de_dados/` | Implementações genéricas de lista encadeada, fila, pilha e nó de árvore |
| `dados/` | Clientes, veículos, componentes e produtos fictícios para iniciar o programa |
| `requirements.txt` | Registro das dependências do projeto |

### Interface e composição

`Aplicacao`, em `interface/aplicacao.py`, seleciona o modo de execução. `Menu` apresenta as opções e encaminha cada comando para um grupo de operações: cadastros, estoque, atendimento, orçamento ou execução. `Entrada` concentra a leitura e a conversão dos valores do terminal. `RelatorioOrdem` apresenta os dados de uma ordem.

`Oficina`, em `oficina/oficina.py`, monta os responsáveis e compartilha suas instâncias. `CadastroVeiculos` recebe o cadastro de clientes; `RegistroDiagnosticos` recebe o cadastro de veículos; `GestaoServicos` recebe os veículos, os diagnósticos e o estoque. Assim, as operações da sessão usam os mesmos registros.

O domínio funciona sem depender do terminal. As chamadas a `input` e `print` ficam na interface, que também apresenta as mensagens de erro ao usuário.

### Cadastros, serviços e estoque

`CadastroClientes` mantém os clientes por código. `CadastroVeiculos` mantém os veículos por placa e confere se o proprietário pertence ao cadastro da oficina. O veículo consultado pelo cliente é o mesmo objeto mantido no cadastro de veículos.

`RegistroDiagnosticos` preserva as visitas. Cada `Diagnostico` guarda os dados do veículo e do cliente, uma cópia da árvore de componentes e o histórico das avaliações.

`GestaoServicos` coordena a fila e a abertura das ordens. `OrdemServico` controla o estado de uma visita e as operações permitidas em cada etapa. `ItemServico` preserva o produto, a quantidade e o preço unitário registrado no orçamento.

No estoque, `CatalogoProdutos` cadastra e localiza produtos. `Produto` mantém os dados comerciais e utiliza `LotesProduto` para controlar seu saldo. `BaixaEstoque` reúne os pedidos, prepara as retiradas e confirma os saldos depois de validar todos os produtos envolvidos.

## Estruturas de dados utilizadas

| Estrutura | Onde é usada | Motivo |
|---|---|---|
| Lista encadeada | Clientes, veículos, diagnósticos, ordens, produtos, itens e históricos | Os registros precisam ser incluídos e percorridos, com consultas por identificador. A consulta de uma ordem não depende de ela ser a primeira a entrar. |
| Duas filas | Espera normal e prioritária | Os prioritários são atendidos primeiro. Dentro de cada categoria, o primeiro veículo a entrar é o primeiro a ser atendido. |
| Fila | Lotes de cada produto | O lote recebido primeiro fornece as primeiras unidades consumidas: FIFO. |
| Pilha | Componentes desmontados durante uma ordem | A última peça retirada é a primeira a ser remontada: LIFO. |
| Árvore n-ária | Componentes e subcomponentes do veículo | Um componente pode conter vários outros, formando uma hierarquia. |

As estruturas genéricas estão em `estrutura_de_dados/` e não conhecem regras da oficina. O nó de árvore `NoArvore`, por exemplo, armazena os componentes do veículo sem precisar saber o que é um motor ou uma pastilha.

### Atendimento por prioridade

A classe `Atendimento` possui uma fila normal e uma prioritária. Ao solicitar o próximo atendimento, consulta primeiro a prioritária e recorre à normal quando aquela está vazia.

Se um carro normal chegar antes de um prioritário, mas ambos ainda estiverem aguardando, o prioritário será atendido primeiro. Um serviço já iniciado continua sua execução. A prioridade é informada ao enfileirar o veículo.

Depois da abertura do serviço, a ordem fica em uma lista encadeada. Isso permite que serviços sejam consultados e concluídos em uma sequência diferente da chegada dos carros.

### Lotes e remontagem

No estoque, um lote parcialmente consumido permanece na frente da fila. Ele só é removido quando seu saldo chega a zero. Os códigos de lotes recebidos também são mantidos em uma lista para impedir sua reutilização no mesmo produto.

Na execução, cada desmontagem coloca o código do componente no topo da pilha da ordem. A remontagem retira esse topo. Essa sequência representa o exercício de desmontar e remontar em ordem inversa; não é um procedimento técnico de reparo de um veículo real.

### Componentes do veículo

A árvore representa relações de composição. Por exemplo, o veículo contém o sistema de freios, que contém uma pastilha e um disco. Cada nó pode ter vários filhos, por isso a estrutura é n-ária.

O diagnóstico percorre essa árvore para apresentar os componentes e suas avaliações. Uma nova visita recebe uma cópia independente, preservando o registro das visitas anteriores.

## Fluxo do código

1. **Inicialização:** `main.py` chama `Aplicacao.iniciar`. A aplicação lê os argumentos e abre a seleção inicial, o menu ou a demonstração.
2. **Carga dos dados:** `DadosExemplo.criar_oficina` cria a oficina, cadastra os clientes, vincula os veículos e recebe os lotes dos produtos fictícios.
3. **Entrada na fila:** `GestaoServicos.enfileirar` localiza o veículo, verifica se há uma ordem ainda não quitada e o encaminha para `Atendimento`.
4. **Abertura da visita:** `GestaoServicos.atender_proximo` valida o identificador, consulta o próximo veículo e registra o diagnóstico e a ordem antes de retirar o carro da fila.
5. **Diagnóstico e orçamento:** o operador avalia os componentes, informa os produtos necessários e define a mão de obra. O diagnóstico é encerrado e o orçamento é aprovado.
6. **Início da execução:** a ordem solicita a baixa ao estoque. Os pedidos do mesmo produto são somados, os saldos são conferidos e o consumo FIFO é preparado em cópias dos lotes.
7. **Confirmação do consumo:** depois da validação de todos os produtos, as filas preparadas substituem os saldos anteriores e os registros de consumo ficam associados à ordem.
8. **Reparo e conclusão:** as desmontagens e remontagens são registradas. A ordem pode ser concluída quando estiver em execução e não houver peças na pilha.
9. **Pagamento:** uma ordem concluída aceita uma quitação integral simulada. Depois de paga, permanece disponível para consulta e o veículo pode iniciar outra visita.

### Estados da ordem

| Estado | Operações principais |
|---|---|
| Aberta | Registrar avaliações, adicionar itens, definir mão de obra e aprovar o orçamento após encerrar o diagnóstico |
| Aprovada | Iniciar a execução e confirmar o consumo das peças |
| Em execução | Registrar desmontagem e remontagem; concluir quando não houver peças desmontadas |
| Concluída | Registrar o pagamento |
| Paga | Consultar o histórico |

A aprovação bloqueia alterações nos itens e na mão de obra. Executar ou pagar novamente uma ordem já processada gera erro. Também é possível aprovar um serviço apenas de mão de obra, sem consumo de produtos.

## Regras de diagnóstico e estoque

Um componente começa como `NAO_AVALIADO`. A inspeção pode registrá-lo como `COM_DEFEITO` ou `SEM_DEFEITO_IDENTIFICADO`. Reavaliar um componente atualiza seu resultado e preserva a avaliação anterior no histórico. Encerrar o diagnóstico mantém os componentes não examinados como não avaliados.

O produto utilizado no reparo é escolhido pelo operador. A árvore descreve os componentes do veículo, enquanto o estoque contém os produtos disponíveis para uso; a ligação entre eles é registrada no item da ordem.

A baixa considera o pedido inteiro. Se faltar um produto, houver saldo insuficiente ou algum pedido for inválido, os demais saldos permanecem intactos. A ordem continua aprovada, permitindo receber peças e tentar a execução novamente. Não há reserva de estoque durante a elaboração do orçamento.

Os valores monetários usam `Decimal`. O preço de venda é preservado no item da ordem, e o custo de entrada é preservado no registro de consumo do lote. Alterações posteriores no preço do produto não modificam o orçamento já registrado. Quantidades precisam ser inteiras positivas; os valores monetários não aceitam frações de centavo.

## Pagamentos

As formas disponíveis são PIX, Débito, Crédito e Bitcoin. Todas registram uma quitação simulada dentro do programa, com o total em reais.

O sistema não realiza cobranças, transferências, conversão de criptomoedas ou parcelamentos. A opção Bitcoin identifica a forma escolhida na simulação, sem calcular uma quantidade em BTC.

## Execução

**Versão adotada no projeto: Python 3.15.** O programa utiliza somente a biblioteca padrão. O `requirements.txt` não possui pacotes externos para instalar.

Na pasta `oficina_mecanica`, execute:

```bash
python main.py
```

O menu inicial permite escolher a operação manual ou a demonstração automática. Para entrar diretamente em um modo:

```bash
python main.py --menu
python main.py --demo
```

### Operação manual

O menu permite cadastrar clientes e veículos, cadastrar produtos, receber lotes, organizar a fila e acompanhar cada etapa de uma ordem. As consultas mostram os códigos disponíveis para as próximas operações.

Com os dados iniciais, um fluxo de exemplo é:

| Opção | Dados informados |
|---|---|
| 7 — Enfileirar | `TST1A01`, normal; depois `TST1A02`, prioritário |
| 8 — Atender | Código da ordem `OS001`; o veículo atendido será `TST1A02` |
| 10 — Avaliar | `OS001`, componente `PASTILHA_DE`, resultado e observação |
| 11 — Adicionar item | `OS001`, componente `PASTILHA_DE`, produto `PASTILHA`, quantidade 2 |
| 12 — Mão de obra | `OS001`, valor 80 |
| 13 — Encerrar diagnóstico | `OS001` |
| 14 — Aprovar | `OS001` |
| 15 — Executar | `OS001` |
| 16 — Desmontar | `OS001`, componente `PASTILHA_DE` |
| 17 — Remontar | `OS001` |
| 18 — Concluir | `OS001` |
| 19 — Pagar | `OS001`, forma de pagamento |
| 20 — Detalhar | `OS001` |

### Demonstração automática

A demonstração cria quatro atendimentos completos. Os carros entram alternando entre normal e prioritário, resultando na sequência `TST1A02`, `TST1A04`, `TST1A01` e `TST1A03`.

Cada ordem registra a avaliação, inclui duas pastilhas, define a mão de obra, aprova o orçamento, consome o estoque, desmonta e remonta componentes e registra uma das quatro formas de pagamento. A saída mostra a prioridade, o consumo entre lotes e a ordem inversa de remontagem.

## Convenções do código

As classes e os métodos usam nomes em português e docstrings no estilo Google. Os métodos têm até dez linhas de lógica, sem contar assinatura, docstrings e comentários.

As entradas são validadas antes de alterar os registros. Exceções específicas são tratadas em blocos curtos de `try/except`; na interface, a falha é apresentada e o controle retorna ao menu. As propriedades que permitem alteração validam o novo valor no setter, enquanto identificadores e vínculos estáveis são somente leitura.

A atividade adota a restrição de não utilizar `if`, `else` ou `while`. O código utiliza iterações com `for`, mapeamento de comandos e validações com exceções para seguir essa convenção.

## Escopo

A carga inicial contém três clientes, quatro veículos e quatro produtos fictícios. Os veículos usam uma composição de componentes definida para a atividade, sem representar um modelo real específico.

Os dados existem apenas em memória. Cada entrada no menu ou na demonstração cria uma nova oficina com a carga inicial. O projeto não inclui banco de dados, execução concorrente, cancelamento de ordens, devolução de peças ou estorno de pagamentos.
=======

>>>>>>> 45b192f7c98ac0a4b30412a4cf72a8f6db033eda
