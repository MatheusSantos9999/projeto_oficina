"""Dados de PedidoEstoque usados nas operações de estoque."""
from oficina.validacao import Validacao


class PedidoEstoque:
    """Representa uma quantidade de um produto solicitada por uma ordem."""

    def __init__(self, produto, quantidade):
        """Valida a identificação e a quantidade solicitadas.

        Args:
            produto (str): Código do produto.
            quantidade (int): Quantidade positiva solicitada.

        Raises:
            TypeError: Se os tipos não corresponderem ao contrato.
            ValueError: Se os valores forem inválidos.
        """
        self._produto = Validacao.codigo(produto)
        self._quantidade = Validacao.quantidade(quantidade)

    @property
    def produto(self):
        """str: Código do produto solicitado."""
        return self._produto

    @property
    def quantidade(self):
        """int: Quantidade solicitada."""
        return self._quantidade
