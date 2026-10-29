"""Cadastro e pesquisa de produtos."""
from functools import partial
from estrutura_de_dados import ListaEncadeada
from oficina.validacao import Validacao
from estoque.produto import Produto


class CatalogoProdutos:
    """Mantém produtos únicos na lista encadeada própria."""

    def __init__(self):
        """Cria um estoque sem produtos.
        """
        self._produtos = ListaEncadeada()

    def cadastrar_produto(self, produto):
        """Inclui um produto sem repetir seu código.

        Args:
            produto (Produto): Cadastro a incluir.

        Raises:
            TypeError: Se o argumento não for produto.
            ValueError: Se o código já existir.
        """
        Validacao.tipo(produto, Produto, "Produto")
        self._validar_codigo_livre(produto.codigo)
        self._produtos.adicionar_final(produto)

    def _validar_codigo_livre(self, codigo):
        """Confere a disponibilidade de um código de produto.

        Args:
            codigo (str): Identificador normalizado.

        Raises:
            ValueError: Se o produto já existir.
        """
        try:
            self.buscar_produto(codigo)
        except ValueError:
            return
        raise ValueError("Produto já cadastrado.")

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
        codigo = Validacao.codigo(codigo)
        try:
            return self._produtos.buscar(partial(self._mesmo_codigo, codigo))
        except ValueError:
            raise ValueError(f"Produto não encontrado: {codigo}.") from None

    @staticmethod
    def _mesmo_codigo(codigo, produto):
        """Compara o código de um produto.

        Args:
            codigo (str): Código procurado.
            produto (Produto): Cadastro examinado.

        Returns:
            bool: Indica correspondência.
        """
        return produto.codigo == codigo

    def listar_produtos(self):
        """Disponibiliza os produtos na ordem de cadastro.

        Returns:
            Iterator: Cadastros de produtos.
        """
        return iter(self._produtos)
