"""Cadastrar e consultar clientes e veículos."""
from cliente.cadastro import CadastroClientes
from oficina.cadastro_veiculos import CadastroVeiculos
from cliente.cliente import Cliente
from dados import DadosExemplo
from oficina.validacao import Validacao
from interface.entrada import Entrada


class MenuCadastros:
    """Cadastrar e consultar clientes e veículos."""

    OPCOES = (
        ('1', 'Listar clientes e veículos', 'listar_clientes'),
        ('2', 'Cadastrar cliente', 'cadastrar_cliente'),
        ('3', 'Cadastrar veículo', 'cadastrar_veiculo'),
    )

    def __init__(self, clientes, veiculos):
        """Recebe os responsáveis usados pelas ações do terminal.

        Args:
            clientes (CadastroClientes): Dependência compartilhada desta operação.
            veiculos (CadastroVeiculos): Dependência compartilhada desta operação.

        Raises:
            TypeError: Se alguma dependência tiver tipo incorreto.
        """
        Validacao.tipo(clientes, CadastroClientes, "CadastroClientes")
        self._clientes = clientes
        Validacao.tipo(veiculos, CadastroVeiculos, "CadastroVeiculos")
        self._veiculos = veiculos

    def listar_clientes(self):
        """Mostra os clientes e os veículos vinculados aos mesmos objetos.
        """
        for cliente in self._clientes.listar():
            print(f"{cliente.codigo}: {cliente.nome}")
            for veiculo in cliente.listar_veiculos():
                self._exibir_veiculo(veiculo)

    @staticmethod
    def _exibir_veiculo(veiculo):
        """Mostra a placa, o modelo e os códigos dos componentes.

        Args:
            veiculo (Veiculo): Cadastro a apresentar.
        """
        print(f"  {veiculo.placa} | {veiculo.modelo}")
        for componente, nivel in veiculo.percorrer_componentes():
            print(f"  {'  ' * nivel}{componente.codigo}: {componente.nome}")

    def cadastrar_cliente(self):
        """Solicita e cadastra um novo cliente.

        Raises:
            ValueError: Se os dados forem inválidos ou o código já existir.
            EOFError: Se a entrada for encerrada.
        """
        codigo = input("Código do cliente: ")
        nome = input("Nome do cliente: ")
        self._clientes.cadastrar(Cliente(codigo, nome))

    def cadastrar_veiculo(self):
        """Cadastra um carro com a composição padrão do exercício.

        Raises:
            ValueError: Se o cliente não existir ou os dados forem inválidos.
            EOFError: Se a entrada for encerrada.
        """
        cliente = self._clientes.buscar(input("Código do cliente: "))
        placa = input("Placa: ")
        modelo = input("Modelo: ")
        veiculo = DadosExemplo.criar_veiculo(cliente, placa, modelo)
        self._veiculos.cadastrar(veiculo)
