"""Pilha LIFO implementada sobre uma lista encadeada própria."""
from estrutura_de_dados.lista_encadeada import ListaEncadeada


class Pilha:
    """Pilha LIFO (last in, first out): o último a entrar é o primeiro a sair.

    Usa uma ListaEncadeada por composição: o topo da pilha é o início da
    lista, onde inserir e remover custa O(1).

    Complexidade de tempo (n = número de elementos):
        empilhar, desempilhar, topo, tamanho, vazia: O(1)

    Examples:
        >>> pilha = Pilha()
        >>> pilha.empilhar("A")
        >>> pilha.empilhar("B")
        >>> pilha.desempilhar()
        'B'
        >>> pilha.topo
        'A'
    """

    def __init__(self):
        """Cria uma pilha vazia."""
        self._dados = ListaEncadeada()

    def empilhar(self, dado):
        """Insere um dado no topo da pilha.

        Complexidade de tempo: O(1).

        Args:
            dado (object): Objeto a empilhar.
        """
        self._dados.adicionar_inicio(dado)

    def desempilhar(self):
        """Remove e devolve o dado do topo.

        Complexidade de tempo: O(1).

        Returns:
            object: O dado inserido mais recentemente.

        Raises:
            IndexError: Se a pilha está vazia.
        """
        try:
            return self._dados.remover_inicio()
        except IndexError:
            raise IndexError("A pilha está vazia.") from None

    @property
    def topo(self):
        """object: Dado do topo, sem removê-lo.

        Raises:
            IndexError: Se a pilha está vazia.
        """
        try:
            return self._dados.primeiro
        except IndexError:
            raise IndexError("A pilha está vazia.") from None

    @property
    def tamanho(self):
        """int: Quantidade de elementos na pilha."""
        return len(self._dados)

    @property
    def vazia(self):
        """bool: True se a pilha não tem elementos."""
        return self._dados.vazia

    def limpar(self):
        """Remove todos os elementos da pilha."""
        self._dados.limpar()

    def __iter__(self):
        """Itera do topo para a base, sem remover nada."""
        return iter(self._dados)

    def __len__(self):
        """Quantidade de elementos, para uso com `len()`."""
        return len(self._dados)

    def __bool__(self):
        """True se a pilha tem pelo menos um elemento."""
        return bool(self._dados)
