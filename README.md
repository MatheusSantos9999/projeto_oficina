# Oficina mecânica — estruturas de dados

Entrega inicial com implementação apenas das estruturas genéricas. As regras de cliente, veículo, estoque, atendimento, ordem de serviço e pagamento ficam reservadas para as próximas etapas.

A pasta solicitada como “estrutura de dados” foi nomeada `estrutura_de_dados`, sem espaços, para permitir sua importação como pacote Python.

## Conteúdo da entrega

| Caminho | Situação |
|---|---|
| `estrutura_de_dados/__init__.py` | Exporta as cinco classes públicas |
| `estrutura_de_dados/no.py` | Nó genérico com dado e próximo nó |
| `estrutura_de_dados/lista_encadeada.py` | Lista simplesmente encadeada própria |
| `estrutura_de_dados/fila.py` | Fila FIFO construída sobre a lista própria |
| `estrutura_de_dados/pilha.py` | Pilha LIFO construída sobre a lista própria |
| `estrutura_de_dados/no_arvore.py` | Árvore de zero a vários filhos e percurso em pré-ordem |
| `cliente/__init__.py`, `cliente/cliente.py` | Reservados, somente docstrings |
| `oficina/__init__.py`, `oficina/veiculo.py`, `oficina/componentes.py`, `oficina/estoque.py`, `oficina/oficina.py` | Reservados, somente docstrings |
| `servico/__init__.py`, `servico/atendimento.py`, `servico/ordem_servico.py`, `servico/pagamento.py` | Reservados, somente docstrings |
| `main.py` | Reservado, sem menu ou integração nesta etapa |

O pacote não usa listas prontas, `deque` ou árvores de bibliotecas como armazenamento principal. Os encadeamentos são feitos com nós próprios. Tuplas são usadas como pares de retorno, registros temporários do percurso e na validação de condições.

## Como experimentar

A implementação foi validada com Python 3.12 e não exige dependências externas. Abra o terminal na pasta que contém `main.py` e execute `python` para experimentar os exemplos abaixo.

### Lista encadeada

```python
from estrutura_de_dados import ListaEncadeada

lista = ListaEncadeada()
lista.adicionar_final("B")
lista.adicionar_inicio("A")
lista.adicionar_final("C")

print(tuple(lista))                         # ('A', 'B', 'C')
print(lista.buscar(lambda dado: dado == "B"))  # B
print(lista.remover(lambda dado: dado == "B")) # B
print(lista.remover_inicio())               # A
print(lista.primeiro, lista.ultimo)         # C C
print(lista.tamanho, lista.vazia)           # 1 False
```

`buscar()` e `remover()` recebem uma função de seleção. Assim, a lista não precisa conhecer CPF, placa, número de ordem de serviço ou outros campos da aplicação. A remoção afeta somente a primeira ocorrência correspondente.

### Fila

```python
from estrutura_de_dados import Fila

fila = Fila()
fila.enfileirar("Primeiro")
fila.enfileirar("Segundo")

print(fila.frente)          # Primeiro
print(fila.desenfileirar()) # Primeiro
print(fila.desenfileirar()) # Segundo
```

A fila segue FIFO: o primeiro dado a entrar é o primeiro a sair. O controle de prioridade de guinchos será implementado posteriormente em `servico/atendimento.py`, usando duas filas e a regra de seleção entre elas.

### Pilha

```python
from estrutura_de_dados import Pilha

pilha = Pilha()
pilha.empilhar("Primeiro")
pilha.empilhar("Segundo")

print(pilha.topo)          # Segundo
print(pilha.desempilhar()) # Segundo
print(pilha.desempilhar()) # Primeiro
```

A pilha segue LIFO: o último dado a entrar é o primeiro a sair. A integração com desmontagem e remontagem do veículo permanece fora desta etapa.

### Árvore com vários filhos

```python
from estrutura_de_dados import NoArvore

raiz = NoArvore("Raiz")
ramo_a = NoArvore("Ramo A")
ramo_b = NoArvore("Ramo B")
folha = NoArvore("Folha")

raiz.adicionar_filho(ramo_a)
raiz.adicionar_filho(ramo_b)
ramo_a.adicionar_filho(folha)

for no, nivel in raiz.pre_ordem():
    print("  " * nivel + str(no.dado))
```

O percurso visita raiz, ramo A, folha e ramo B, nessa ordem. O nível começa em zero para o nó em que `pre_ordem()` é chamado. A impressão e a formatação pertencem ao chamador; o método devolve pares de nó e nível.

Cada nó pode ter qualquer quantidade de filhos, limitada pelos recursos da máquina. Não existe regra de árvore binária ou ordenação de busca. O conteúdo é genérico: nome, código e estado de um componente serão responsabilidade de `oficina/componentes.py`.

O vínculo com o pai é controlado pela árvore. Um filho não pode pertencer a dois pais nem formar um ciclo. Para transferir um ramo:

```python
ramo = raiz.remover_filho(ramo_a)
outra_raiz = NoArvore("Outra raiz")
outra_raiz.adicionar_filho(ramo)
```

Os descendentes do ramo são preservados. O método `remover_filho()` exige a referência exata a um filho direto; dados iguais não tornam dois nós o mesmo objeto. A edição é uma capacidade genérica para montagem e manutenção, embora o enunciado permita manter a árvore de componentes pré-definida.

## Encapsulamento e exceções

Os nós usam propriedades para acessar e atualizar `dado`. Como o conteúdo é genérico, qualquer objeto é aceito, inclusive `None`; validações de cliente, veículo ou componente não cabem às estruturas.

`No.proximo` valida a referência recebida e recusa apontar diretamente para o próprio nó. O nó linear isolado não procura ciclos indiretos: as listas criam e controlam seus próprios nós, sem expor o encadeamento pela API pública. Não altere atributos internos iniciados por `_`.

Contadores, início lógico da fila, topo da pilha, pai e coleção de filhos são consultados por propriedades sem setters públicos. Isso evita atribuições que deixariam tamanho ou vínculos inconsistentes. Para mudar o conteúdo, use os métodos públicos.

| Situação | Exceção |
|---|---|
| Consultar ou retirar de uma estrutura vazia | `IndexError` |
| Buscar ou remover sem encontrar correspondência | `ValueError` |
| Informar critério não chamável ou vínculo com tipo inválido | `TypeError` |
| Tentar criar ciclo ou atribuir segundo pai na árvore | `ValueError` |
| Modificar a lista durante iteração ou durante o critério de busca | `RuntimeError` |

Uma estrutura pode armazenar `None`; por isso, esse valor não é utilizado como sinal de falha de remoção. Erros próprios da função de seleção são propagados para o chamador, sem serem escondidos.

Os blocos `try/except` são curtos e capturam falhas específicas. Não há `if`, `else`, expressões condicionais ou `while` no código. Os percursos usam `for`, com `range` ou `itertools.count`. Para atender à restrição nas validações booleanas, `tuple.index` procura o resultado esperado e sua falha é convertida na exceção prevista. Exceções dos critérios fornecidos pelo chamador são avaliadas fora desses blocos, preservando o erro original.

As classes e métodos possuem docstrings no padrão Google, em português. Todos os 63 métodos têm até dez linhas não vazias de lógica, desconsiderando assinatura, docstrings e comentários. Os comentários são curtos e explicam trechos pontuais.

## Combinações já implementadas

| Classes e métodos envolvidos | Motivo da combinação |
|---|---|
| `Fila.enfileirar()` e `Fila.desenfileirar()` usam `ListaEncadeada.adicionar_final()` e `remover_inicio()` | Reaproveitar o encadeamento e manter a interface pública FIFO |
| `Pilha.empilhar()` e `Pilha.desempilhar()` usam `ListaEncadeada.adicionar_inicio()` e `remover_inicio()` | Reaproveitar o mesmo encadeamento com uma interface pública LIFO |
| `NoArvore.adicionar_filho()` usa uma `ListaEncadeada` de nós filhos | Representar zero a N filhos sem um vetor de capacidade fixa |
| `NoArvore.pre_ordem()` e `_empilhar_filhos()` usam `Pilha` | Percorrer sem recursão, preservando a ordem de inclusão dos filhos |

Concentrar todos esses comportamentos em uma única estrutura exporia operações incompatíveis com cada finalidade e misturaria as responsabilidades. Uma fila, por exemplo, não deve oferecer inserção pública no início, embora a lista interna tenha essa capacidade.

As combinações de domínio exigidas no enunciado — duas filas para prioridade, lista de produtos com filas de lotes e lista de clientes com listas de veículos — ainda precisam ser integradas às regras da oficina. Esta entrega prepara as estruturas necessárias, mas não implementa o sistema completo.

## Complexidades

Considere `n` elementos da lista ou nós percorridos, `h` a altura até o nó e `k` a quantidade de filhos diretos. Nas buscas, considere também o custo do critério fornecido pelo chamador.

| Operação | Tempo |
|---|---|
| Inserir no início ou fim da lista | O(1) |
| Consultar início, fim ou tamanho | O(1) |
| Remover o início da lista | O(1) |
| Buscar ou remover por critério | O(n), com critério de custo constante |
| Enfileirar, desenfileirar ou consultar frente | O(1) |
| Empilhar, desempilhar ou consultar topo | O(1) |
| Adicionar filho à árvore | O(h), pela verificação de ancestrais |
| Remover um filho direto | O(k) |
| Percorrer a árvore em pré-ordem | O(n) |

Lista, fila e pilha ocupam O(n) de memória. O percurso da árvore usa até O(n) de memória auxiliar no pior caso, incluindo as pilhas temporárias de filhos. `limpar()` descarta as referências iniciais; a liberação dos nós pode exigir O(n), conforme o gerenciamento de memória do Python.

Os iteradores de lista, fila e pilha detectam alterações estruturais, mas não oferecem segurança entre threads. A árvore não deve ser modificada durante seu percurso. O conteúdo dos objetos é armazenado por referência; modificar um objeto armazenado não cria uma cópia nem altera automaticamente a versão da lista.

## Validação executada

Nesta revisão, foram aprovados 11 testes externos de regressão, com múltiplos cenários por teste, além da conferência automática de docstrings e tamanho dos métodos. A bateria completa de teste não foi incluída no ZIP para manter somente os arquivos de estrutura solicitados.

Os testes cobriram ordem FIFO/LIFO, dados `None`, elementos duplicados, remoções, reutilização após limpeza, propagação de falhas dos critérios, invalidação de iteradores, vínculos inválidos, ciclos, múltiplos pais e transferência de ramos. Também foram verificadas 6.000 operações aleatórias de lista, uma árvore com 1.501 níveis e uma raiz com mil filhos.

Os exemplos das docstrings foram executados e podem ser conferidos novamente a partir da raiz do projeto:

```bash
python -m doctest estrutura_de_dados/no.py estrutura_de_dados/lista_encadeada.py estrutura_de_dados/fila.py estrutura_de_dados/pilha.py estrutura_de_dados/no_arvore.py
```

A ausência de mensagens indica que os exemplos passaram. Acrescente `-v` depois de `doctest` para ver os detalhes.

## Verificação do PDF recebido

O arquivo `Projeto_2.pdf` tem quatro páginas. Foram examinados texto extraído, páginas renderizadas, metadados comuns e XMP, anotações, anexos, objetos de ação, propriedades de conteúdo opcional e características de renderização do texto.

Não foram encontrados sinais de prompts ocultos nas verificações realizadas. Não apareceram anexos, JavaScript, ações automáticas, anotações ou trechos de texto invisível, branco, de opacidade quase nula, fora da página ou de tamanho inferior a três pontos.

A observação sobre uso indevido de LLMs e a exigência de domínio do código estão visíveis na avaliação da página 4. Elas não são instruções ocultas. O prazo antigo de 22/10/2026 está visivelmente riscado e substituído por 29/10/2026.

A inspeção foi estática e não representa garantia absoluta contra qualquer técnica de ocultação. Para a apresentação, estude as decisões, operações e complexidades e observe as regras da disciplina.
