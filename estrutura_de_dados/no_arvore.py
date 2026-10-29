"""Nó de árvore genérica com quantidade variável de filhos."""
from functools import partial
from itertools import count
from operator import is_
from estrutura_de_dados.lista_encadeada import ListaEncadeada
from estrutura_de_dados.pilha import Pilha


class NoArvore:
    """Nó de uma árvore n-ária: pode ter zero ou mais filhos.

    Os filhos ficam em uma ListaEncadeada interna, na ordem em que foram
    adicionados. O percurso em pré-ordem é iterativo e usa uma Pilha em vez de
    recursão. Não é árvore binária nem de busca: não há ordenação entre nós, e
    o nó não conhece nenhuma regra da oficina.

    Complexidade de tempo (n = nós da árvore, f = filhos do nó, h = altura):
        adicionar_filho: O(h), pois sobe até a raiz para evitar ciclos
        remover_filho: O(f)
        pre_ordem: O(n) no percurso completo
        quantidade_filhos, pai: O(1)

    Examples:
        >>> raiz = NoArvore("Raiz")
        >>> filho = NoArvore("Filho")
        >>> raiz.adicionar_filho(filho)
        >>> tuple((no.dado, nivel) for no, nivel in raiz.pre_ordem())
        (('Raiz', 0), ('Filho', 1))

    Note:
        Cada nó tem no máximo um pai. Alterar a árvore durante um percurso
        em pré-ordem gera resultado imprevisível.
    """

    def __init__(self, dado):
        """Cria um nó sem pai e sem filhos.

        Args:
            dado (object): Conteúdo representado por este nó.
        """
        self.dado = dado
        self._filhos = ListaEncadeada()
        self._pai = None

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
    def pai(self):
        """Nó acima deste na hierarquia, ou None se este for a raiz.

        Somente leitura: o vínculo só muda por adicionar_filho e remover_filho.
        """
        return self._pai

    @property
    def filhos(self):
        """Iterator: Filhos diretos, na ordem de inclusão."""
        return iter(self._filhos)

    @property
    def quantidade_filhos(self):
        """int: Número de filhos diretos."""
        return len(self._filhos)

    def adicionar_filho(self, filho):
        """Liga um nó sem pai como último filho deste nó.

        Complexidade de tempo: O(h), custo da checagem de ciclo; a inserção
        em si é O(1).

        Args:
            filho (NoArvore): Nó a ser ligado. Não pode ter pai.

        Raises:
            TypeError: Se `filho` não for um NoArvore.
            ValueError: Se `filho` já tiver pai ou se a inclusão formar um
                ciclo (adicionar o nó a si mesmo ou a um de seus ancestrais).
        """
        self._validar_filho(filho)
        self._validar_ancestrais(filho)
        self._filhos.adicionar_final(filho)
        filho._pai = self

    def _validar_filho(self, filho):
        """Confere o tipo e se o candidato ainda não tem pai.

        Raises:
            TypeError: Se `filho` não for um NoArvore.
            ValueError: Se `filho` já tiver pai.
        """
        self._validar_no(filho)
        try:
            (True,).index(filho.pai is None)
        except ValueError:
            raise ValueError("Remova o nó do pai atual antes de adicioná-lo.") from None

    def _validar_ancestrais(self, filho):
        """Impede ligar um nó a si mesmo ou a um de seus ancestrais.

        Sobe de pai em pai até a raiz procurando `filho`.

        Raises:
            ValueError: Se a inclusão formaria um ciclo.
        """
        atual = self
        for _ in count():
            try:
                (False,).index(atual is filho)
            except ValueError:
                raise ValueError("A inclusão formaria um ciclo na árvore.") from None
            try:
                atual = atual.pai
            except AttributeError:
                return

    def pre_ordem(self):
        """Percorre este nó e seus descendentes em pré-ordem.

        Visita o nó e depois cada filho, da esquerda para a direita (ordem de
        inclusão). A pilha guarda os nós ainda não visitados.

        Complexidade de tempo: O(n). Cada nó entra e sai da pilha uma vez.

        Yields:
            tuple: Par (nó, profundidade), com profundidade 0 neste nó. Serve
            para indentar a exibição.
        """
        pendentes = Pilha()
        pendentes.empilhar((self, 0))
        for _ in count():
            try:
                atual, nivel = pendentes.desempilhar()
            except IndexError:
                return
            yield atual, nivel
            atual._empilhar_filhos(pendentes, nivel + 1)

    def _empilhar_filhos(self, pendentes, nivel):
        """Empilha os filhos de modo que o primeiro filho seja o próximo.

        A pilha inverte a ordem de saída, então os filhos passam antes por uma
        pilha auxiliar para serem empilhados do último para o primeiro.

        Args:
            pendentes (Pilha): Pilha de nós que ainda serão visitados.
            nivel (int): Profundidade dos filhos neste percurso.
        """
        inversa = Pilha()
        # A última inserção na pilha será a próxima visita.
        for filho in self._filhos:
            inversa.empilhar(filho)
        for _ in range(len(inversa)):
            pendentes.empilhar((inversa.desempilhar(), nivel))

    def _validar_no(self, filho):
        """Confere o tipo antes de acessar vínculos da árvore.

        Raises:
            TypeError: Se `filho` não for um NoArvore.
        """
        try:
            (True,).index(isinstance(filho, NoArvore))
        except ValueError:
            raise TypeError("O filho deve ser um nó de árvore.") from None

    def remover_filho(self, filho):
        """Desliga um filho direto, mantendo os descendentes dele.

        Complexidade de tempo: O(f), pois procura o filho na lista.

        Args:
            filho (NoArvore): O próprio objeto a retirar. A busca compara a
                identidade (`is`), não o conteúdo.

        Returns:
            NoArvore: O nó removido, agora sem pai.

        Raises:
            TypeError: Se `filho` não for um NoArvore.
            ValueError: Se `filho` não for filho direto deste nó.
        """
        self._validar_no(filho)
        # A remoção considera a identidade do nó, não o conteúdo.
        removido = self._filhos.remover(partial(is_, filho))
        removido._pai = None
        return removido
