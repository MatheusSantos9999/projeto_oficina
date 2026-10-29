"""Preço e quantidade preservados em um item de serviço."""
from estoque.produto import Produto
from oficina.validacao import Validacao


class ItemServico:
    """Preserva o componente atendido e o preço de venda do produto solicitado."""

    def __init__(self, componente, produto, quantidade):
        """Cria um item sem alterar o estoque.

        Args:
            componente (str): Código da peça do veículo a atender.
            produto (Produto): Cadastro comercial escolhido.
            quantidade (int): Quantidade solicitada.

        Raises:
            TypeError: Se os tipos forem incorretos.
            ValueError: Se o componente ou quantidade forem inválidos.
        """
        Validacao.tipo(produto, Produto, "Produto")
        self._componente = Validacao.codigo(componente)
        self._produto = produto.codigo
        self._descricao = produto.nome
        self._quantidade = Validacao.quantidade(quantidade)
        self._valor_unitario = produto.preco

    @property
    def componente(self):
        """str: Componente do veículo associado ao item."""
        return self._componente

    @property
    def produto(self):
        """str: Código do produto no estoque."""
        return self._produto

    @property
    def descricao(self):
        """str: Descrição comercial preservada na inclusão."""
        return self._descricao

    @property
    def quantidade(self):
        """int: Quantidade solicitada."""
        return self._quantidade

    @property
    def valor_unitario(self):
        """Decimal: Preço preservado na inclusão."""
        return self._valor_unitario

    @property
    def total(self):
        """Decimal: Valor total deste item."""
        return self.quantidade * self.valor_unitario
