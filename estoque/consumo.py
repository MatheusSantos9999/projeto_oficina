"""Dados de ConsumoLote usados nas operações de estoque."""
from estoque.lote import Lote
from oficina.validacao import Validacao


class ConsumoLote:
    """Preserva o produto, o lote e o custo de uma retirada confirmada."""

    def __init__(self, produto, lote, quantidade):
        """Guarda um registro independente da retirada.

        Args:
            produto (str): Código do produto consumido.
            lote (Lote): Lote que forneceu as unidades.
            quantidade (int): Quantidade retirada deste lote.

        Raises:
            TypeError: Se algum argumento tiver tipo incorreto.
            ValueError: Se os dados da retirada forem inválidos.
        """
        Validacao.tipo(lote, Lote, "Lote")
        self._produto = Validacao.codigo(produto)
        self._lote = lote.codigo
        self._quantidade = Validacao.quantidade(quantidade)
        self._custo_unitario = lote.custo_unitario

    @property
    def produto(self):
        """str: Produto consumido."""
        return self._produto

    @property
    def lote(self):
        """str: Código do lote usado."""
        return self._lote

    @property
    def quantidade(self):
        """int: Quantidade retirada."""
        return self._quantidade

    @property
    def custo_unitario(self):
        """Decimal: Custo por unidade preservado no registro."""
        return self._custo_unitario
