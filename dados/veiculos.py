"""Veículos e clientes fictícios, sem relação com cadastros reais."""
from oficina.componentes import Componente
from oficina.oficina import Oficina
from oficina.veiculo import Veiculo

# Cada registro contém cliente, placa fictícia e modelo de exemplo.
VEICULOS = (
    ("Cliente fictício 01", "TST1A01", "Hatch de exemplo"),
    ("Cliente fictício 02", "TST1A02", "Sedã de exemplo"),
    ("Cliente fictício 03", "TST1A03", "Utilitário de exemplo"),
)

# O pai aparece antes dos filhos para permitir a montagem da hierarquia.
COMPONENTES = (
    ("VEICULO", "MOTOR", "Motor"),
    ("MOTOR", "VELA_1", "Vela 1"),
    ("VEICULO", "FREIOS", "Sistema de freios"),
    ("FREIOS", "PASTILHA_DE", "Pastilha dianteira esquerda"),
    ("FREIOS", "DISCO_DE", "Disco dianteiro esquerdo"),
    ("VEICULO", "ELETRICA", "Sistema elétrico"),
    ("ELETRICA", "BATERIA", "Bateria"),
)


class DadosExemplo:
    """Monta cadastros novos a partir dos dados fictícios deste módulo.

    Cada chamada produz objetos independentes. As tuplas acima são somente
    dados de entrada; os cadastros usam a ListaEncadeada e a árvore próprias.
    """

    @staticmethod
    def criar_oficina():
        """Cria uma oficina com os três veículos de exemplo.

        Returns:
            Oficina: Nova oficina preenchida com os cadastros fictícios.

        Raises:
            TypeError: Se os dados de entrada tiverem tipos incorretos.
            ValueError: Se os dados editados contiverem valores inválidos.
        """
        oficina = Oficina()
        for cliente, placa, modelo in VEICULOS:
            veiculo = DadosExemplo.criar_veiculo(cliente, placa, modelo)
            oficina.cadastrar_veiculo(veiculo)
        return oficina

    @staticmethod
    def criar_veiculo(cliente, placa, modelo):
        """Monta um veículo com sua própria árvore de componentes.

        Args:
            cliente (str): Nome fictício do cliente.
            placa (str): Identificação fictícia do veículo.
            modelo (str): Modelo de exemplo.

        Returns:
            Veiculo: Cadastro com componentes independentes dos demais carros.

        Raises:
            TypeError: Se algum argumento tiver tipo incorreto.
            ValueError: Se um identificador ou texto obrigatório for inválido.
        """
        veiculo = Veiculo(placa, modelo, cliente)
        for codigo_pai, codigo, nome in COMPONENTES:
            veiculo.adicionar_componente(codigo_pai, Componente(codigo, nome))
        return veiculo
