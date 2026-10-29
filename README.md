# Oficina mecânica integrada

Sistema didático em memória que integra clientes, veículos, diagnóstico, atendimento, estoque, ordens de serviço e pagamentos simulados. Usa diretamente `ListaEncadeada`, `Fila`, `Pilha` e `NoArvore` implementados no próprio projeto.

## Executar

Use Python 3.10 ou superior. A entrega foi testada com Python 3.12.

Depois de extrair o ZIP, abra o terminal na pasta `oficina_mecanica`:

```bash
python main.py
```

O início permite escolher **operar a oficina**, **demonstração automática** ou **sair**. Também é possível iniciar diretamente um dos modos:

```bash
python main.py --menu
python main.py --demo
```

Não há pacotes externos. O `requirements.txt` foi incluído para registrar esse fato; não lista bibliotecas que já fazem parte do Python. Opcionalmente, o comando habitual continua válido:

```bash
python -m pip install -r requirements.txt
```

Todos os dados são mantidos somente durante a execução. Cada entrada em um modo cria uma nova oficina com dados fictícios. Sair de um modo e entrar novamente reinicia esses dados.

## Pagamentos

São aceitas as formas **PIX, Débito, Crédito e Bitcoin** para uma quitação integral simulada da ordem.

Não há cobrança, integração bancária, consulta de cotação, geração de endereço de carteira ou transferência de criptomoeda. Inclusive na opção Bitcoin, o programa registra o total da ordem **em reais**, identificado como simulação. Crédito não implica parcelamento nesta etapa.

A confirmação no menu marca a ordem como paga somente dentro do exercício. Uma ordem paga não aceita outro pagamento nem outra baixa de estoque.

## Arquivos e responsabilidades

Existe apenas um `main.py`, na raiz. Ele importa a aplicação e chama seu ponto de entrada. A navegação, os comandos e a demonstração estão no pacote `interface`.

| Arquivo ou grupo | Responsabilidade |
|---|---|
| `main.py` | Iniciar a aplicação; 4 linhas, sem classes de domínio ou menu |
| `interface/aplicacao.py` | Selecionar o modo inicial e tratar falhas de execução |
| `interface/menu.py` | Mostrar opções, despachar comandos e apresentar erros |
| `interface/entrada.py` e `encerramento.py` | Ler entradas e sinalizar saída |
| `interface/cadastros.py` | Ações de clientes e veículos no terminal |
| `interface/estoque.py` | Ações de produtos e lotes no terminal |
| `interface/atendimento.py` | Ações da fila e abertura de ordens |
| `interface/orcamento.py` | Entrada de avaliações e preparação do orçamento |
| `interface/execucao.py` | Ações de execução, remontagem e pagamento |
| `interface/relatorio_ordem.py` | Exibir os dados de uma ordem |
| `interface/demonstracao.py` | Executar o cenário automático completo |
| `oficina/oficina.py` | Montar e compartilhar os responsáveis; 43 linhas |
| `cliente/cadastro.py` | Cadastrar, buscar e listar clientes |
| `cliente/cliente.py` | Dados de um cliente e sua lista de veículos |
| `oficina/cadastro_veiculos.py` | Cadastrar veículos e manter o vínculo com o proprietário |
| `oficina/registro_diagnosticos.py` | Abrir, registrar e consultar visitas |
| `oficina/veiculo.py` | Identificação, proprietário e árvore de componentes |
| `oficina/componentes.py`, `avaliacao.py` e `diagnostico.py` | Componentes, resultados e histórico de inspeção |
| `oficina/validacao.py` | Validar os valores recebidos pelo domínio |
| `estoque/estoque.py` | Encaminhar as operações ao catálogo e à baixa; 78 linhas |
| `estoque/catalogo.py` | Cadastrar e localizar produtos |
| `estoque/produto.py` | Identificação e preço comercial |
| `estoque/lotes_produto.py` | Receber lotes e planejar seu consumo FIFO |
| `estoque/lote.py` | Dados e saldo de um lote |
| `estoque/pedido.py` e `consumo.py` | Quantidades solicitadas e registros das retiradas |
| `estoque/baixa.py` | Agrupar pedidos e confirmar a baixa completa |
| `servico/gestao_servicos.py` | Coordenar a abertura e as operações das ordens |
| `servico/atendimento.py` | Filas normal e prioritária |
| `servico/ordem_servico.py` | Proteger o ciclo de vida de uma ordem |
| `servico/item_servico.py` | Preservar quantidade e preço de cada item |
| `servico/pagamento.py` | Formas de pagamento e quitação simulada |
| `dados/veiculos.py` | Carga de dados fictícios |
| `estrutura_de_dados/` | Estruturas genéricas preservadas byte a byte |

A separação acompanha responsabilidades. `Menu` conhece os comandos, mas não cadastra clientes nem calcula consumo. Cada grupo recebe apenas os responsáveis de que precisa. A demonstração usa o domínio diretamente e compartilha a apresentação dos consumos com o relatório.

`Oficina` monta os objetos uma vez: o cadastro de veículos recebe o mesmo cadastro de clientes; o registro de diagnósticos recebe os mesmos veículos; a gestão de serviços recebe esses registros e o estoque compartilhado. Suas propriedades são somente leitura, evitando substituir acidentalmente uma dependência durante a sessão.

No estoque, o catálogo mantém os produtos, o controle de lotes prepara retiradas FIFO e `BaixaEstoque` confirma o conjunto depois das validações. A confirmação usa métodos internos do produto e do controle de lotes; não altera diretamente os atributos de outra entidade. O planejamento continua em cópias, preservando os saldos em caso de falha de validação.

`OrdemServico` continua protegendo suas próprias transições: aprovar, executar, concluir e pagar. Essas operações dependem do estado da mesma ordem. O item comercial foi extraído para seu módulo, enquanto as regras que impedem execução ou pagamento repetidos permanecem na ordem.

As dependências são passadas aos construtores e validadas. O domínio não importa a interface e não chama `input` ou `print`. As estruturas próprias continuam sendo usadas diretamente; não foi criada outra árvore.

### Acessos pelo código após a refatoração

O menu mantém as mesmas opções e entradas. Para chamar o projeto por outro código Python, os acessos passaram a indicar o responsável:

| Acesso anterior | Acesso atual |
|---|---|
| `oficina.cadastrar_cliente(cliente)` | `oficina.clientes.cadastrar(cliente)` |
| `oficina.buscar_cliente(codigo)` | `oficina.clientes.buscar(codigo)` |
| `oficina.listar_clientes()` | `oficina.clientes.listar()` |
| `oficina.quantidade_clientes` | `oficina.clientes.quantidade` |
| `oficina.cadastrar_veiculo(veiculo)` | `oficina.veiculos.cadastrar(veiculo)` |
| `oficina.buscar_veiculo(placa)` | `oficina.veiculos.buscar(placa)` |
| `oficina.listar_veiculos()` | `oficina.veiculos.listar()` |
| `oficina.quantidade_veiculos` | `oficina.veiculos.quantidade` |
| `oficina.iniciar_diagnostico(codigo, placa)` | `oficina.diagnosticos.abrir(codigo, placa)` |
| `oficina.buscar_diagnostico(codigo)` | `oficina.diagnosticos.buscar(codigo)` |
| `oficina.listar_diagnosticos()` | `oficina.diagnosticos.listar()` |
| `oficina.quantidade_diagnosticos` | `oficina.diagnosticos.quantidade` |
| `oficina.registrar_avaliacao(codigo, componente, estado)` | `oficina.diagnosticos.buscar(codigo).registrar(componente, estado)` |
| `oficina.encerrar_diagnostico(codigo)` | `oficina.diagnosticos.buscar(codigo).encerrar()` |
| `oficina.enfileirar(placa, prioritario)` | `oficina.servicos.enfileirar(placa, prioritario)` |
| `oficina.atender_proximo(codigo)` | `oficina.servicos.atender_proximo(codigo)` |
| `oficina.buscar_ordem(codigo)` | `oficina.servicos.buscar_ordem(codigo)` |
| `oficina.listar_ordens()` | `oficina.servicos.listar_ordens()` |
| `oficina.quantidade_ordens` | `oficina.servicos.quantidade_ordens` |
| `oficina.adicionar_item(...)` | `oficina.servicos.adicionar_item(...)` |
| `oficina.executar_ordem(codigo)` | `oficina.servicos.executar_ordem(codigo)` |
| `oficina.pagar_ordem(codigo, forma)` | `oficina.servicos.pagar_ordem(codigo, forma)` |
| `oficina.atendimento` | `oficina.servicos.atendimento` |

Importe cada entidade pelo módulo responsável: `from estoque.produto import Produto`, `from estoque.lote import Lote`, `from estoque.pedido import PedidoEstoque`, `from estoque.consumo import ConsumoLote` e `from servico.item_servico import ItemServico`. Para a demonstração, use `from interface.demonstracao import Demonstracao`. Esses caminhos substituem os imports concentrados em `main.py` e `estoque/estoque.py`.

## Dados de exemplo

A carga inicial contém:

- três clientes fictícios, identificados por código;
- quatro carros, com dois deles vinculados ao mesmo cliente;
- uma árvore independente com motor, freios e sistema elétrico para cada carro;
- quatro produtos, cada um com dois lotes: 3 unidades no `LOTE-A` e 9 no `LOTE-B`;
- preços e custos definidos exclusivamente para o exercício.

O cliente do veículo agora é um objeto `Cliente`, e não um nome solto. A lista do cliente e a lista da oficina apontam para o mesmo carro. O vínculo do proprietário é somente leitura; não foi implementada transferência de propriedade.

Cadastrar um veículo pelo menu usa a composição padrão descrita em `dados/veiculos.py`, sem presumir que ela corresponda à composição real de determinado modelo.

## Estruturas utilizadas

| Informação ou operação | Estrutura própria |
|---|---|
| Clientes, veículos, diagnósticos e ordens | `ListaEncadeada` |
| Veículos pertencentes a um cliente | `ListaEncadeada` |
| Produtos do estoque | `ListaEncadeada` |
| Lotes disponíveis de cada produto | `Fila` |
| Espera normal e prioritária | Duas `Fila` |
| Itens da ordem, avaliações e consumos | `ListaEncadeada` |
| Peças desmontadas em cada ordem | `Pilha` |
| Componentes e subcomponentes | `NoArvore` |

Tuplas nos dados de exemplo representam registros de entrada. Dicionários do terminal servem apenas para selecionar comandos; não substituem as coleções de domínio.

O estoque guarda códigos de lotes já recebidos em uma lista própria. Isso impede reutilizar o código de um lote esgotado para o mesmo produto.

## Regras do fluxo

1. Cadastre o cliente antes de cadastrar seu veículo.
2. Enfileire o carro como normal ou prioritário.
3. Inicie o próximo atendimento informando um código de ordem ainda não usado. A ordem e seu diagnóstico compartilham esse identificador.
4. Registre as avaliações dos componentes, escolha explicitamente os produtos necessários e informe a mão de obra.
5. Encerre o diagnóstico e aprove o orçamento.
6. Inicie a execução. O estoque verifica todas as peças e confirma a baixa completa.
7. Registre a desmontagem, quando aplicável, e remonte as peças na ordem inversa.
8. Conclua o serviço e registre o pagamento simulado.

### Prioridade

A fila prioritária é sempre consultada primeiro. Dentro de cada categoria, o atendimento respeita a ordem de entrada. Um novo prioritário passa à frente dos normais ainda aguardando; o serviço já iniciado não é interrompido.

A conclusão dos serviços não precisa seguir a ordem de chegada. Por isso, as ordens ficam em uma lista, e não na fila de espera. Um veículo não pode entrar duas vezes nas filas nem iniciar outra ordem antes de quitar a anterior.

### Diagnóstico e orçamento

Um componente começa como `NAO_AVALIADO`. As avaliações válidas são `COM_DEFEITO` e `SEM_DEFEITO_IDENTIFICADO`. Um defeito não seleciona automaticamente um produto do estoque: essa ligação é informada na ordem.

O diagnóstico preserva código e nome do cliente, placa, modelo e uma cópia da árvore da visita. Uma nova avaliação substitui o resultado atual, mas mantém o registro anterior no histórico.

Encerrar o diagnóstico não conclui o reparo nem declara o veículo sem defeitos. Avaliações parciais são permitidas, e componentes não examinados continuam identificados como não avaliados.

A aprovação bloqueia alterações dos itens e da mão de obra. Uma ordem precisa ter algum item ou mão de obra com valor positivo. Serviços somente de mão de obra são permitidos e não geram uma baixa fictícia no estoque.

### Estoque e preços

Os lotes são consumidos em FIFO. Um lote parcialmente utilizado continua na frente; só sai da fila quando seu saldo chega a zero.

As quantidades de itens repetidos do mesmo produto são somadas antes da verificação. As retiradas são preparadas em cópias dos lotes. Somente depois de todos os produtos serem validados as filas preparadas substituem as originais.

Falta de saldo, produto inexistente ou pedido inválido não reduz outros saldos. A ordem permanece aprovada, permitindo receber um novo lote e tentar a execução novamente. Não há reserva antecipada: entre ordens aprovadas, o estoque é confirmado na ordem de execução.

Cada ordem preserva o preço unitário de venda no momento da inclusão do item. Alterar o preço do produto depois não muda ordens anteriores. Os registros de consumo preservam separadamente os lotes, as quantidades e os custos de entrada.

Os valores usam `Decimal`, com duas casas decimais. `float`, valores não finitos, negativos e frações de centavo não são aceitos. No terminal, pode-se digitar ponto ou vírgula como separador decimal, sem separadores de milhares.

### Desmontagem e conclusão

A pilha pertence à ordem de serviço. Retirar um componente não o exclui da árvore do veículo. Remontar retira o topo da pilha e registra qual peça foi recolocada.

A mesma peça não pode ser empilhada duas vezes sem ser recolocada. A conclusão fica bloqueada enquanto houver peças desmontadas. As operações de retirada e recolocação permanecem no histórico da ordem.

| Situação | Próxima operação principal |
|---|---|
| Aberta | Encerrar diagnóstico e aprovar orçamento |
| Aprovada | Iniciar execução e confirmar estoque |
| Em execução | Executar e remontar as peças retiradas |
| Concluída | Registrar pagamento simulado |
| Paga | Consultar histórico; permitir nova visita do veículo |

Não foram implementados cancelamentos, devoluções, estornos ou parcelamentos.

## Percurso manual no menu

Um exemplo usando os dados iniciais:

| Opção | Entrada principal |
|---|---|
| 7 — Enfileirar | `TST1A01`, categoria normal |
| 7 — Enfileirar | `TST1A02`, categoria prioritária |
| 8 — Atender | Código `OS001`; o carro atendido será `TST1A02` |
| 10 — Avaliar | `OS001`, `PASTILHA_DE`, com defeito, observação livre |
| 11 — Adicionar item | `OS001`, `PASTILHA_DE`, produto `PASTILHA`, quantidade 2 |
| 12 — Mão de obra | `OS001`, valor 80 |
| 13 — Encerrar diagnóstico | `OS001` |
| 14 — Aprovar | `OS001` |
| 15 — Executar | `OS001` |
| 16 — Desmontar | `OS001`, componente `PASTILHA_DE` |
| 17 — Remontar | `OS001` |
| 18 — Concluir | `OS001` |
| 19 — Pagar | `OS001`, forma escolhida |
| 20 — Detalhar | `OS001` |

As demais opções permitem cadastrar clientes, veículos e produtos, receber lotes, consultar filas e listar os registros. Entradas inválidas apresentam uma mensagem e devolvem o controle ao menu.

## Demonstração automática

O modo `--demo` cria uma oficina nova e enfileira os carros nas categorias normal, prioritária, normal e prioritária.

A ordem de atendimento resultante é `TST1A02`, `TST1A04`, `TST1A01`, `TST1A03`. São concluídas quatro ordens de R$ 320,00: duas pastilhas de R$ 120,00 mais R$ 80,00 de mão de obra. Cada ordem usa uma das quatro formas de pagamento.

A segunda ordem demonstra consumo entre lotes: utiliza a unidade restante do `LOTE-A` e uma unidade do `LOTE-B`. Depois das quatro ordens, o saldo de `PASTILHA` é 4 unidades. O modo também mostra a remontagem em ordem inversa e preserva os históricos até terminar o processo.

## Código e verificações

As classes e os métodos possuem docstrings em português no estilo Google. Todos os métodos do projeto têm até dez linhas não vazias de lógica, desconsiderando assinatura, docstrings e comentários. Os blocos `try` têm até duas linhas de corpo. Foram preservadas as restrições de não usar `if`, `else` ou `while`.

As exceções são específicas e tratadas em blocos pequenos. A adaptação de condições booleanas com `tuple.index` atende à restrição solicitada; não representa uma recomendação geral para escrever Python.

Foram aprovados **65 testes externos**, incluindo:

- vínculos entre clientes e veículos, identificadores e duplicidades;
- prioridade absoluta e FIFO dentro de cada fila;
- preservação da fila quando a abertura de uma ordem falha;
- consumo parcial de lotes, soma de pedidos repetidos e falta de saldo sem baixa parcial;
- preservação de preços, orçamento e histórico de avaliações;
- transições da ordem, pilha de remontagem e bloqueio de operações repetidas;
- as quatro formas de pagamento e a liberação do veículo para uma nova visita;
- demonstração automática e operação completa pelo menu em subprocessos;
- importação de `main.py` sem execução, EOF e opções inválidas;
- 1.000 operações aleatórias na lista e retiradas comparadas a um modelo de referência;
- docstrings, limite dos métodos e preservação byte a byte das estruturas próprias;
- ponto de entrada mínimo e domínio independente do terminal;
- dependências compartilhadas, propriedades somente leitura e rejeição de argumentos inválidos;
- importação isolada de todos os módulos, verificando dependências circulares.

Os testes de desenvolvimento foram executados fora do ZIP. Os exemplos das docstrings podem ser verificados na pasta do projeto com:

```bash
python -m doctest estrutura_de_dados/no.py estrutura_de_dados/lista_encadeada.py estrutura_de_dados/fila.py estrutura_de_dados/pilha.py estrutura_de_dados/no_arvore.py oficina/oficina.py
```

O projeto é um exercício local em memória: não possui persistência, autenticação, acesso concorrente ou integração de pagamentos. Não altere os atributos internos iniciados por `_`. As buscas nas estruturas são lineares, e a cópia da árvore pode custar O(n²) devido à validação de ancestrais.
