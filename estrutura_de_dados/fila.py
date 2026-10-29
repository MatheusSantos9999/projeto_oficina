"""Fila FIFO implementada sobre uma lista encadeada própria."""
from estrutura_de_dados.lista_encadeada import ListaEncadeada


class Fila:
    """Fila FIFO (first in, first out): o primeiro a entrar é o primeiro a sair.

    Usa uma ListaEncadeada por composição: insere no fim e remove do início.
    Como as duas pontas são acessadas diretamente, nenhuma operação percorre a
    fila. Em um array, retirar o primeiro elemento (`pop(0)`) custaria O(n),
    pois todos os outros precisariam andar uma posição.

    Complexidade de tempo (n = número de elementos):
        enfileirar, desenfileirar, frente, tamanho, vazia: O(1)

    Examples:
        >>> fila = Fila()
        >>> fila.enfileirar("A")
        >>> fila.enfileirar("B")
        >>> fila.desenfileirar()
        'A'
        >>> fila.frente
        'B'
    """

    def __init__(self):
        """Cria uma fila vazia."""
        self._dados = ListaEncadeada()

    def enfileirar(self, dado):
        """Insere um dado no fim da fila.

        Complexidade de tempo: O(1).

        Args:
            dado (object): Objeto que aguardará sua vez.
        """
        self._dados.adicionar_final(dado)

    def desenfileirar(self):
        """Remove e devolve o dado mais antigo da fila.

        Complexidade de tempo: O(1).

        Returns:
            object: O dado que estava na frente.

        Raises:
            IndexError: Se a fila está vazia.
        """
        try:
            return self._dados.remover_inicio()
        except IndexError:
            raise IndexError("A fila está vazia.") from None

    @property
    def frente(self):
        """object: Próximo dado a sair, sem removê-lo.

        Raises:
            IndexError: Se a fila está vazia.
        """
        try:
            return self._dados.primeiro
        except IndexError:
            raise IndexError("A fila está vazia.") from None

    @property
    def tamanho(self):
        """int: Quantidade de elementos na fila."""
        return len(self._dados)

    @property
    def vazia(self):
        """bool: True se a fila não tem elementos."""
        return self._dados.vazia

    def limpar(self):
        """Remove todos os elementos da fila."""
        self._dados.limpar()

    def __iter__(self):
        """Itera da frente para o fim, sem remover nada."""
        return iter(self._dados)

    def __len__(self):
        """Quantidade de elementos, para uso com `len()`."""
        return len(self._dados)

    def __bool__(self):
        """True se a fila tem pelo menos um elemento."""
        return bool(self._dados)
