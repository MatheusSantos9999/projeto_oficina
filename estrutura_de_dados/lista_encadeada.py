"""Lista simplesmente encadeada com referências para início e fim."""
from estrutura_de_dados.no import No


class ListaEncadeada:
    """Lista simplesmente encadeada genérica.

    Cada elemento fica em um No que aponta para o próximo. Como a lista guarda
    referências para o primeiro e para o último nó, inserir nas duas pontas e
    remover do início não exigem percorrer a lista.

    A busca recebe um critério (função que recebe o dado e devolve True ou
    False), então a lista não precisa conhecer o tipo do que guarda.

    Complexidade de tempo (n = número de elementos):
        adicionar_inicio, adicionar_final, remover_inicio: O(1)
        buscar, remover: O(n)
        tamanho, vazia, primeiro, ultimo: O(1)

    Examples:
        >>> lista = ListaEncadeada()
        >>> lista.adicionar_final("A")
        >>> lista.adicionar_inicio("B")
        >>> tuple(lista)
        ('B', 'A')
        >>> lista.remover_inicio()
        'B'

    Note:
        A cada inserção ou remoção o contador interno `_versao` aumenta.
        Iteradores e buscas comparam a versão ao longo do percurso e levantam
        RuntimeError se ela mudar. É a mesma ideia do erro "dictionary changed
        size during iteration" do Python. A lista não é thread-safe.
    """

    def __init__(self):
        """Cria uma lista vazia."""
        self._inicio = None
        self._fim = None
        self._tamanho = 0
        self._versao = 0

    @property
    def tamanho(self):
        """int: Quantidade de elementos."""
        return self._tamanho

    @property
    def vazia(self):
        """bool: True se a lista não tem elementos."""
        return self._tamanho == 0

    @property
    def primeiro(self):
        """object: Primeiro dado da lista, sem removê-lo.

        Raises:
            IndexError: Se a lista está vazia.
        """
        try:
            return self._inicio.dado
        except AttributeError:
            raise IndexError("A lista está vazia.") from None

    @property
    def ultimo(self):
        """object: Último dado da lista, sem removê-lo.

        Raises:
            IndexError: Se a lista está vazia.
        """
        try:
            return self._fim.dado
        except AttributeError:
            raise IndexError("A lista está vazia.") from None

    def adicionar_inicio(self, dado):
        """Insere um dado antes de todos os outros.

        Complexidade de tempo: O(1).

        Args:
            dado (object): Objeto a armazenar. Aceita None.
        """
        novo = No(dado, self._inicio)
        self._inicio = novo
        try:
            self._fim.dado
        except AttributeError:
            self._fim = novo
        self._tamanho += 1
        self._versao += 1

    def adicionar_final(self, dado):
        """Insere um dado depois de todos os outros.

        Complexidade de tempo: O(1), graças à referência para o último nó.

        Args:
            dado (object): Objeto a armazenar. Aceita None.
        """
        novo = No(dado)
        # A primeira inserção também define o início da lista.
        try:
            self._fim.proximo = novo
        except AttributeError:
            self._inicio = novo
        self._fim = novo
        self._tamanho += 1
        self._versao += 1

    def remover_inicio(self):
        """Remove e devolve o primeiro dado.

        Complexidade de tempo: O(1).

        Returns:
            object: O dado removido (pode ser None).

        Raises:
            IndexError: Se a lista está vazia.
        """
        try:
            self._inicio.dado
        except AttributeError:
            raise IndexError("A lista está vazia.") from None
        return self._desvincular(None, self._inicio)

    def buscar(self, criterio):
        """Devolve o primeiro dado que satisfaz o critério, sem removê-lo.

        Complexidade de tempo: O(n).

        Args:
            criterio (callable): Função que recebe um dado e devolve True ou
                False.

        Returns:
            object: Primeiro dado para o qual `criterio` é verdadeiro.

        Raises:
            TypeError: Se `criterio` não for chamável.
            ValueError: Se nenhum dado satisfizer o critério.
            RuntimeError: Se o critério alterar a lista durante a busca.

        Examples:
            >>> lista = ListaEncadeada()
            >>> lista.adicionar_final(10)
            >>> lista.adicionar_final(20)
            >>> lista.buscar(lambda numero: numero > 15)
            20
        """
        _, atual = self._localizar(criterio)
        return atual.dado

    def remover(self, criterio):
        """Remove e devolve o primeiro dado que satisfaz o critério.

        Complexidade de tempo: O(n) para localizar + O(1) para religar os nós.

        Args:
            criterio (callable): Função que recebe um dado e devolve True ou
                False.

        Returns:
            object: O dado removido.

        Raises:
            TypeError: Se `criterio` não for chamável.
            ValueError: Se nenhum dado satisfizer o critério.
            RuntimeError: Se o critério alterar a lista durante a busca.

        Examples:
            >>> lista = ListaEncadeada()
            >>> for letra in "ABC":
            ...     lista.adicionar_final(letra)
            >>> lista.remover(lambda letra: letra == "B")
            'B'
            >>> tuple(lista)
            ('A', 'C')
        """
        anterior, atual = self._localizar(criterio)
        return self._desvincular(anterior, atual)

    def _localizar(self, criterio):
        """Percorre a lista até achar o primeiro nó que satisfaz o critério.

        Guarda o nó anterior durante o percurso, necessário para religar a
        cadeia em uma remoção.

        Args:
            criterio (callable): Função de seleção.

        Returns:
            tuple: Par (nó anterior, nó encontrado). O anterior é None quando
            o nó encontrado é o primeiro.

        Raises:
            ValueError: Se nenhum nó satisfizer o critério.
        """
        self._validar_criterio(criterio)
        versao = self._versao
        for anterior, atual in self._pares(versao):
            encontrado = self._avaliar_criterio(criterio, atual, versao)
            try:
                (True,).index(encontrado)
            except ValueError:
                continue
            return anterior, atual
        raise ValueError("Nenhum elemento corresponde ao critério.")

    def _validar_criterio(self, criterio):
        """Recusa critérios inválidos, mesmo com a lista vazia.

        Raises:
            TypeError: Se `criterio` não for chamável.
        """
        try:
            (True,).index(callable(criterio))
        except ValueError:
            raise TypeError("O critério deve ser uma função ou objeto chamável.") from None

    def _desvincular(self, anterior, atual):
        """Retira um nó da cadeia e mantém início, fim e contador coerentes.

        Args:
            anterior (No | None): Nó anterior, ou None se `atual` é o início.
            atual (No): Nó da lista que será retirado.

        Returns:
            object: Dado do nó retirado.
        """
        self._religar(anterior, atual.proximo)
        self._atualizar_fim(anterior, atual)
        atual.proximo = None
        self._tamanho -= 1
        self._versao += 1
        return atual.dado

    def limpar(self):
        """Remove todos os elementos.

        Complexidade de tempo: O(1). Os nós descartados são liberados pelo
        coletor de lixo do Python. Iteradores em andamento são invalidados.
        """
        self._inicio = None
        self._fim = None
        self._tamanho = 0
        self._versao += 1

    def _validar_versao(self, versao):
        """Confere se a lista não mudou desde que a operação começou.

        Args:
            versao (int): Versão capturada no início da operação.

        Raises:
            RuntimeError: Se houve inserção, remoção ou limpeza no meio.
        """
        try:
            (True,).index(versao == self._versao)
        except ValueError:
            raise RuntimeError("A lista foi modificada durante a operação.") from None

    def _percorrer(self, versao):
        """Gera os dados do início ao fim, conferindo a versão a cada passo.

        Args:
            versao (int): Versão esperada durante todo o percurso.

        Yields:
            object: Cada dado, na ordem atual da lista.

        Raises:
            RuntimeError: Se a lista for alterada durante o percurso.
        """
        for atual in self._percorrer_nos(versao):
            yield atual.dado

    def __iter__(self):
        """Itera do início ao fim, sem remover nada."""
        return self._percorrer(self._versao)

    def __len__(self):
        """Quantidade de elementos, para uso com `len()`."""
        return self._tamanho

    def __bool__(self):
        """True se a lista tem pelo menos um elemento."""
        return self._tamanho != 0

    def _percorrer_nos(self, versao):
        """Percorre os nós sem expor vínculos pela interface pública.

        Args:
            versao (int): Versão esperada da lista.

        Yields:
            No: Próximo nó encadeado.

        Raises:
            RuntimeError: Se a lista mudar durante o percurso.
        """
        atual = self._inicio
        for _ in range(self._tamanho):
            self._validar_versao(versao)
            yield atual
            self._validar_versao(versao)
            atual = atual.proximo
        self._validar_versao(versao)

    def _pares(self, versao):
        """Associa cada nó ao seu antecessor durante uma busca.

        Args:
            versao (int): Versão esperada da lista.

        Yields:
            tuple: Par com o nó anterior e o atual.
        """
        anterior = None
        for atual in self._percorrer_nos(versao):
            yield anterior, atual
            anterior = atual

    def _avaliar_criterio(self, criterio, atual, versao):
        """Executa a seleção e verifica alterações estruturais.

        Args:
            criterio (callable): Função de seleção fornecida pelo chamador.
            atual (No): Nó cujo dado será avaliado.
            versao (int): Versão esperada da lista.

        Returns:
            bool: Resultado da seleção.

        Raises:
            RuntimeError: Se o critério modificar a lista.

        Note:
            Exceções do critério são propagadas sem conversão.
        """
        encontrado = bool(criterio(atual.dado))
        self._validar_versao(versao)
        return encontrado

    def _religar(self, anterior, proximo):
        """Religa a cadeia após a retirada de um nó.

        Args:
            anterior (No | None): Antecessor ou ausência no início da lista.
            proximo (No | None): Sucessor do nó retirado.
        """
        try:
            anterior.proximo = proximo
        except AttributeError:
            self._inicio = proximo

    def _atualizar_fim(self, anterior, atual):
        """Atualiza a última referência quando o nó retirado era o último.

        Args:
            anterior (No | None): Novo último nó caso haja atualização.
            atual (No): Nó retirado da cadeia.
        """
        try:
            (True,).index(atual is self._fim)
        except ValueError:
            return
        self._fim = anterior
