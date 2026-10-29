"""Clientes, veículos e estoque fictícios para demonstração local."""
from cliente.cliente import Cliente
from estoque.produto import Produto
from estoque.lote import Lote
from oficina.componentes import Componente
from oficina.oficina import Oficina
from oficina.veiculo import Veiculo

CLIENTES = (
    ("CLI001", "Cliente fictício 01"),
    ("CLI002", "Cliente fictício 02"),
    ("CLI003", "Cliente fictício 03"),
)

# O primeiro campo liga o carro ao cliente cadastrado.
VEICULOS = (
    ("CLI001", "TST1A01", "Hatch de exemplo"),
    ("CLI002", "TST1A02", "Sedã de exemplo"),
    ("CLI003", "TST1A03", "Utilitário de exemplo"),
    ("CLI001", "TST1A04", "Segundo carro de exemplo"),
)

COMPONENTES = (
    ("VEICULO", "MOTOR", "Motor"),
    ("MOTOR", "VELA_1", "Vela 1"),
    ("VEICULO", "FREIOS", "Sistema de freios"),
    ("FREIOS", "PASTILHA_DE", "Pastilha dianteira esquerda"),
    ("FREIOS", "DISCO_DE", "Disco dianteiro esquerdo"),
    ("VEICULO", "ELETRICA", "Sistema elétrico"),
    ("ELETRICA", "BATERIA", "Bateria"),
)

# Valores de venda e custo em reais, definidos somente para o exercício.
PRODUTOS = (
    ("PASTILHA", "Pastilha de exemplo", "120.00", "65.00"),
    ("DISCO", "Disco de exemplo", "200.00", "110.00"),
    ("VELA", "Vela de exemplo", "70.00", "35.00"),
    ("BATERIA", "Bateria de exemplo", "350.00", "240.00"),
)


class DadosExemplo:
    """Cria objetos independentes a partir de registros integralmente fictícios."""

    @staticmethod
    def criar_oficina():
        """Monta clientes, carros e estoque na mesma oficina.

        Returns:
            Oficina: Instância integrada pronta para experimentar.

        Raises:
            TypeError: Se algum dado editado tiver tipo incorreto.
            ValueError: Se houver dados inválidos ou duplicados.
        """
        oficina = Oficina()
        DadosExemplo._clientes(oficina)
        DadosExemplo._veiculos(oficina)
        DadosExemplo._estoque(oficina)
        return oficina

    @staticmethod
    def _clientes(oficina):
        """Cadastra os clientes fictícios.

        Args:
            oficina (Oficina): Instância que recebe os dados.
        """
        for codigo, nome in CLIENTES:
            oficina.clientes.cadastrar(Cliente(codigo, nome))

    @staticmethod
    def _veiculos(oficina):
        """Vincula cada carro ao mesmo objeto de cliente cadastrado.

        Args:
            oficina (Oficina): Instância que recebe os carros.
        """
        for codigo, placa, modelo in VEICULOS:
            cliente = oficina.clientes.buscar(codigo)
            oficina.veiculos.cadastrar(DadosExemplo.criar_veiculo(cliente, placa, modelo))

    @staticmethod
    def criar_veiculo(cliente, placa, modelo):
        """Monta o carro e sua árvore própria de componentes.

        Args:
            cliente (Cliente): Cadastro real da instância da oficina, com dados fictícios.
            placa (str): Identificação do exemplo.
            modelo (str): Modelo informado.

        Returns:
            Veiculo: Carro com árvore independente.

        Raises:
            TypeError: Se algum tipo for incorreto.
            ValueError: Se os dados forem inválidos.
        """
        veiculo = Veiculo(placa, modelo, cliente)
        for pai, codigo, nome in COMPONENTES:
            veiculo.adicionar_componente(pai, Componente(codigo, nome))
        return veiculo

    @staticmethod
    def _estoque(oficina):
        """Cria dois lotes FIFO por produto de exemplo.

        Args:
            oficina (Oficina): Instância com o estoque compartilhado.
        """
        for codigo, nome, venda, custo in PRODUTOS:
            produto = Produto(codigo, nome, venda)
            produto.receber_lote(Lote("LOTE-A", 3, custo))
            produto.receber_lote(Lote("LOTE-B", 9, custo))
            oficina.estoque.cadastrar_produto(produto)
