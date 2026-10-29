"""Identificação e preço comercial de um produto."""
from oficina.validacao import Validacao
from estoque.lotes_produto import LotesProduto


class Produto:
    """Mantém os dados comerciais e delega o controle dos lotes."""

    def __init__(self, codigo, nome, preco):
        """Cria um produto sem unidades disponíveis.

        Args:
            codigo (str): Identificador único no estoque.
            nome (str): Descrição do produto.
            preco (str | int | Decimal): Preço de venda unitário em reais.

        Raises:
            TypeError: Se os tipos forem incorretos.
            ValueError: Se os valores forem inválidos.
        """
        self._codigo = Validacao.codigo(codigo)
        self.nome = nome
        self.preco = preco
        self._saldo = LotesProduto(self.codigo)

    @property
    def codigo(self):
        """str: Identificador estável do produto."""
        return self._codigo

    @property
    def nome(self):
        """str: Descrição comercial do produto."""
        return self._nome

    @nome.setter
    def nome(self, valor):
        """Atualiza a descrição após validá-la.

        Args:
            valor (str): Nova descrição.

        Raises:
            TypeError: Se o valor não for texto.
            ValueError: Se o nome estiver vazio.
        """
        self._nome = Validacao.texto(valor, "Nome do produto")

    @property
    def preco(self):
        """Decimal: Preço de venda atual, sem alterar preços de ordens anteriores."""
        return self._preco

    @preco.setter
    def preco(self, valor):
        """Atualiza o preço para futuras inclusões em ordens.

        Args:
            valor (str | int | Decimal): Novo preço unitário.

        Raises:
            TypeError: Se o tipo não for aceito.
            ValueError: Se o preço for inválido.
        """
        self._preco = Validacao.dinheiro(valor)

    @property
    def saldo(self):
        """int: Unidades disponíveis nos lotes do produto."""
        return self._saldo.saldo

    def receber_lote(self, lote):
        """Acrescenta uma cópia do lote ao final da fila.

        Args:
            lote (Lote): Lote recebido com saldo positivo.

        Raises:
            TypeError: Se o argumento não for lote.
            ValueError: Se o código já foi usado ou não houver saldo.
        """
        self._saldo.receber_lote(lote)

    def listar_lotes(self):
        """Disponibiliza cópias dos lotes na ordem de consumo.

        Returns:
            Iterator: Cópias independentes dos lotes com saldo.
        """
        return self._saldo.listar_lotes()

    def planejar_consumo(self, quantidade):
        """Prepara a retirada em uma fila copiada, sem modificar o estoque.

        Args:
            quantidade (int): Total solicitado para este produto.

        Returns:
            tuple: Fila restante e lista de retiradas planejadas.

        Raises:
            TypeError: Se a quantidade não for inteira.
            ValueError: Se a quantidade for inválida ou faltar estoque.
        """
        return self._saldo.planejar_consumo(quantidade)

    def _confirmar_consumo(self, fila):
        """Confirma um planejamento interno depois da validação de todos os pedidos.

        Args:
            fila (Fila): Fila produzida pelo controle de lotes deste produto.
        """
        self._saldo._confirmar(fila)
