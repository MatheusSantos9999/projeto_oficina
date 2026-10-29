"""Planejamento e confirmação de uma baixa completa."""
from functools import partial
from estrutura_de_dados import ListaEncadeada
from oficina.validacao import Validacao
from estoque.catalogo import CatalogoProdutos
from estoque.pedido import PedidoEstoque


class BaixaEstoque:
    """Agrupa pedidos e confirma os saldos apenas após validar todos os produtos."""

    def __init__(self, catalogo):
        """Recebe o catálogo usado para localizar os produtos da baixa.

        Args:
            catalogo (CatalogoProdutos): Cadastro compartilhado com o estoque.

        Raises:
            TypeError: Se o catálogo tiver tipo incorreto.
        """
        Validacao.tipo(catalogo, CatalogoProdutos, "Catálogo")
        self._catalogo = catalogo

    def consumir(self, pedidos):
        """Confirma uma baixa completa após preparar todos os produtos.

        Args:
            pedidos (ListaEncadeada): Registros PedidoEstoque, inclusive códigos repetidos.

        Returns:
            ListaEncadeada: Registros de consumo por lote.

        Raises:
            TypeError: Se a coleção ou seus registros tiverem tipo incorreto.
            ValueError: Se faltar estoque ou algum produto não existir.

        Note:
            Erros de validação não alteram saldos. A operação em memória não é concorrente.
        """
        self._validar_pedidos(pedidos)
        planos = ListaEncadeada()
        for pedido in pedidos:
            self._preparar_produto(pedido.produto, pedidos, planos)
        return self._confirmar(planos)

    @staticmethod
    def _validar_pedidos(pedidos):
        """Confere todos os registros antes de planejar a baixa.

        Args:
            pedidos (ListaEncadeada): Coleção recebida.

        Raises:
            TypeError: Se a coleção ou algum registro tiver tipo incorreto.
            ValueError: Se a coleção estiver vazia.
        """
        Validacao.tipo(pedidos, ListaEncadeada, "Pedidos")
        Validacao.exigir(bool(pedidos), "Informe ao menos um produto.")
        for pedido in pedidos:
            Validacao.tipo(pedido, PedidoEstoque, "Pedido")

    def _preparar_produto(self, codigo, pedidos, planos):
        """Soma as ocorrências de um produto antes de verificar seu saldo.

        Args:
            codigo (str): Produto solicitado.
            pedidos (ListaEncadeada): Todos os pedidos da ordem.
            planos (ListaEncadeada): Recebe somente um plano por produto.

        Raises:
            ValueError: Se o produto não existir ou faltar saldo.
        """
        produto = self._catalogo.buscar_produto(codigo)
        try:
            planos.buscar(partial(self._produto_planejado, produto))
        except ValueError:
            quantidade = sum(p.quantidade for p in filter(partial(self._pedido_codigo, codigo), pedidos))
            fila, movimentos = produto.planejar_consumo(quantidade)
            planos.adicionar_final((produto, fila, movimentos))

    @staticmethod
    def _produto_planejado(produto, plano):
        """Verifica se já há um plano para o mesmo produto.

        Args:
            produto (Produto): Cadastro procurado.
            plano (tuple): Produto, fila copiada e movimentos.

        Returns:
            bool: Indica se o produto já foi planejado.
        """
        return plano[0] is produto

    @staticmethod
    def _pedido_codigo(codigo, pedido):
        """Seleciona todas as ocorrências de um produto no pedido.

        Args:
            codigo (str): Produto procurado.
            pedido (PedidoEstoque): Registro examinado.

        Returns:
            bool: Indica correspondência.
        """
        return pedido.produto == codigo

    @staticmethod
    def _confirmar(planos):
        """Publica as filas preparadas depois de reunir os registros.

        Args:
            planos (ListaEncadeada): Planos já validados, sem produtos repetidos.

        Returns:
            ListaEncadeada: Retiradas confirmadas.
        """
        registros = ListaEncadeada()
        for _, _, movimentos in planos:
            for movimento in movimentos:
                registros.adicionar_final(movimento)
        for produto, fila, _ in planos:
            produto._confirmar_consumo(fila)
        return registros
