"""Cadastrar produtos, receber lotes e consultar saldos."""
from estoque.estoque import Estoque
from estoque.produto import Produto
from estoque.lote import Lote
from oficina.validacao import Validacao
from interface.entrada import Entrada


class MenuEstoque:
    """Cadastrar produtos, receber lotes e consultar saldos."""

    OPCOES = (
        ('4', 'Consultar estoque e lotes', 'listar_estoque'),
        ('5', 'Cadastrar produto', 'cadastrar_produto'),
        ('6', 'Receber lote no estoque', 'receber_lote'),
    )

    def __init__(self, estoque):
        """Recebe os responsáveis usados pelas ações do terminal.

        Args:
            estoque (Estoque): Dependência compartilhada desta operação.

        Raises:
            TypeError: Se alguma dependência tiver tipo incorreto.
        """
        Validacao.tipo(estoque, Estoque, "Estoque")
        self._estoque = estoque

    def listar_estoque(self):
        """Mostra saldos, preços e lotes na ordem FIFO.
        """
        for produto in self._estoque.listar_produtos():
            print(f"{produto.codigo} | {produto.nome} | saldo {produto.saldo} | R$ {produto.preco:.2f}")
            for lote in produto.listar_lotes():
                print(f"  {lote.codigo}: {lote.quantidade} unidades | custo R$ {lote.custo_unitario:.2f}")

    def cadastrar_produto(self):
        """Solicita um novo produto antes de receber seus lotes.

        Raises:
            ValueError: Se os dados forem inválidos ou duplicados.
            EOFError: Se a entrada for encerrada.
        """
        codigo = input("Código do produto: ")
        nome = input("Nome do produto: ")
        preco = Entrada.valor("Preço de venda em reais: ")
        self._estoque.cadastrar_produto(Produto(codigo, nome, preco))

    def receber_lote(self):
        """Recebe unidades no final da fila de lotes do produto.

        Raises:
            ValueError: Se os dados ou o código do produto forem inválidos.
            EOFError: Se a entrada for encerrada.
        """
        produto = input("Código do produto: ")
        codigo = input("Código do lote: ")
        quantidade = Entrada.quantidade()
        custo = Entrada.valor("Custo unitário em reais: ")
        self._estoque.receber_lote(produto, Lote(codigo, quantidade, custo))
