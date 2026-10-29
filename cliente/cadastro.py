"""Cadastro e pesquisa dos clientes."""
from functools import partial
from estrutura_de_dados import ListaEncadeada
from oficina.validacao import Validacao
from cliente.cliente import Cliente


class CadastroClientes:
    """Mantém códigos únicos e preserva a identidade dos clientes."""

    def __init__(self):
        """Inicia o cadastro de clientes vazio."""
        self._clientes = ListaEncadeada()

    @property
    def quantidade(self):
        """int: Quantidade de clientes cadastrados."""
        return len(self._clientes)

    def cadastrar(self, cliente):
        """Inclui um cliente sem repetir seu identificador.

        Args:
            cliente (Cliente): Cadastro a incluir.

        Raises:
            TypeError: Se o argumento não for cliente.
            ValueError: Se o código já estiver cadastrado.
        """
        Validacao.tipo(cliente, Cliente, "Cliente")
        self._validar_cliente_livre(cliente.codigo)
        self._clientes.adicionar_final(cliente)

    def _validar_cliente_livre(self, codigo):
        """Confere a disponibilidade do identificador do cliente.

        Args:
            codigo (str): Código normalizado.

        Raises:
            ValueError: Se o código já existir.
        """
        try:
            self.buscar(codigo)
        except ValueError:
            return
        raise ValueError("Cliente já cadastrado.")

    def buscar(self, codigo):
        """Encontra o cadastro de cliente pelo código.

        Args:
            codigo (str): Identificador procurado.

        Returns:
            Cliente: Cadastro mantido pela oficina.

        Raises:
            TypeError: Se o código não for texto.
            ValueError: Se o código for inválido ou desconhecido.
        """
        codigo = Validacao.codigo(codigo)
        try:
            return self._clientes.buscar(partial(self._mesmo_cliente, codigo))
        except ValueError:
            raise ValueError("Cliente não encontrado.") from None

    @staticmethod
    def _mesmo_cliente(codigo, cliente):
        """Compara o código de um cliente.

        Args:
            codigo (str): Identificador procurado.
            cliente (Cliente): Cadastro examinado.

        Returns:
            bool: Indica correspondência.
        """
        return cliente.codigo == codigo

    def listar(self):
        """Disponibiliza os clientes cadastrados.

        Returns:
            Iterator: Clientes na ordem de cadastro.
        """
        return iter(self._clientes)
