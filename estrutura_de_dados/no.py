"""Nó genérico usado pelas estruturas encadeadas."""


class No:
    """Elo de uma cadeia: guarda um dado e aponta para o próximo nó.

    É o bloco de construção da ListaEncadeada. Não conhece nenhuma regra da
    oficina; o dado pode ser qualquer objeto.

    Examples:
        >>> primeiro = No("A")
        >>> primeiro.proximo = No("B")
        >>> primeiro.proximo.dado
        'B'

    Note:
        O nó só impede apontar para si mesmo. Ciclos mais longos (A -> B -> A)
        não são detectados aqui; isso fica a cargo das estruturas que usam o
        nó, que não expõem seus nós para fora.
    """

    def __init__(self, dado, proximo=None):
        """Cria um nó.

        Args:
            dado (object): Conteúdo a armazenar. Aceita qualquer objeto,
                inclusive None.
            proximo (No | None): Nó seguinte. None marca o fim da cadeia.

        Raises:
            TypeError: Se `proximo` não for um No nem None.
        """
        self.dado = dado
        self.proximo = proximo

    @property
    def dado(self):
        """object: Conteúdo armazenado no nó."""
        return self._dado

    @dado.setter
    def dado(self, valor):
        """Atualiza o conteúdo armazenado.

        Args:
            valor (object): Novo conteúdo; aceita qualquer objeto, inclusive None.
        """
        self._dado = valor

    @property
    def proximo(self):
        """No | None: Próximo nó da cadeia, ou None se este for o último.

        Raises:
            TypeError: Ao atribuir algo que não seja um No nem None.
            ValueError: Ao atribuir o próprio nó (laço direto).
        """
        return self._proximo

    @proximo.setter
    def proximo(self, valor):
        """Valida e atualiza o próximo elo da cadeia.

        Args:
            valor (No | None): Próximo nó ou fim da cadeia.

        Raises:
            TypeError: Se o valor não for um nó nem None.
            ValueError: Se o valor for o próprio nó.
        """
        self._validar_proximo(valor)
        try:
            (False,).index(valor is self)
        except ValueError:
            raise ValueError("Um nó não pode apontar diretamente para si mesmo.") from None
        self._proximo = valor

    def _validar_proximo(self, valor):
        """Confere o tipo do próximo elo antes de alterar o vínculo.

        Args:
            valor (object): Referência a validar.

        Raises:
            TypeError: Se o valor não for um nó nem None.
        """
        try:
            (True,).index(valor is None or isinstance(valor, No))
        except ValueError:
            raise TypeError("O próximo elemento deve ser um nó ou None.") from None
