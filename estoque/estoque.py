"""Ponto de acesso às operações do estoque."""
from estoque.catalogo import CatalogoProdutos
from estoque.baixa import BaixaEstoque


class Estoque:
    """Encaminha cadastros e baixas aos responsáveis que compartilham os produtos."""

    def __init__(self):
        """Compartilha um catálogo entre consultas, entradas e baixas."""
        self._catalogo = CatalogoProdutos()
        self._baixa = BaixaEstoque(self._catalogo)

    def cadastrar_produto(self, produto):
        """Inclui um produto sem repetir seu código.

        Args:
            produto (Produto): Cadastro a incluir.

        Raises:
            TypeError: Se o argumento não for produto.
            ValueError: Se o código já existir.
        """
        self._catalogo.cadastrar_produto(produto)

    def buscar_produto(self, codigo):
        """Localiza um produto pelo identificador.

        Args:
            codigo (str): Identificador procurado.

        Returns:
            Produto: Cadastro encontrado.

        Raises:
            TypeError: Se o código não for texto.
            ValueError: Se o código for inválido ou desconhecido.
        """
        return self._catalogo.buscar_produto(codigo)

    def listar_produtos(self):
        """Disponibiliza os produtos na ordem de cadastro.

        Returns:
            Iterator: Cadastros de produtos.
        """
        return self._catalogo.listar_produtos()

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
        return self._baixa.consumir(pedidos)

    def receber_lote(self, codigo, lote):
        """Registra a entrada no produto indicado.

        Args:
            codigo (str): Produto que recebe o lote.
            lote (Lote): Dados da entrada.

        Raises:
            TypeError: Se os tipos forem inválidos.
            ValueError: Se o produto não existir ou o lote for inválido.
        """
        self.buscar_produto(codigo).receber_lote(lote)
