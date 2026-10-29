"""Cadastro de veículos e vínculo com seus proprietários."""
from functools import partial
from estrutura_de_dados import ListaEncadeada
from cliente.cadastro import CadastroClientes
from oficina.validacao import Validacao
from oficina.veiculo import Veiculo


class CadastroVeiculos:
    """Mantém placas únicas e compartilha os veículos com seus clientes."""

    def __init__(self, clientes):
        """Vincula veículos aos clientes já cadastrados.

        Args:
            clientes (CadastroClientes): Cadastro dos proprietários.

        Raises:
            TypeError: Se o cadastro tiver tipo incorreto.
        """
        Validacao.tipo(clientes, CadastroClientes, "Cadastro de clientes")
        self._clientes = clientes
        self._veiculos = ListaEncadeada()

    @property
    def quantidade(self):
        """int: Quantidade atual de cadastros de veículos."""
        return len(self._veiculos)

    def cadastrar(self, veiculo):
        """Inclui um cadastro sem permitir placas repetidas.

        Args:
            veiculo (Veiculo): Objeto a cadastrar.

        Raises:
            TypeError: Se o argumento não for um veículo.
            ValueError: Se a placa já estiver cadastrada.
        """
        Validacao.tipo(veiculo, Veiculo, "Veículo")
        cliente = self._clientes.buscar(veiculo.cliente.codigo)
        Validacao.exigir(cliente is veiculo.cliente, "Use o cadastro de cliente desta oficina.")
        self._validar_placa_livre(veiculo.placa)
        cliente.adicionar_veiculo(veiculo)
        self._veiculos.adicionar_final(veiculo)

    def _validar_placa_livre(self, placa):
        """Verifica a disponibilidade de uma placa já normalizada.

        Args:
            placa (str): Identificação do novo cadastro.

        Raises:
            ValueError: Se a placa já estiver cadastrada.
        """
        try:
            self.buscar(placa)
        except ValueError:
            return
        raise ValueError(f"Veículo já cadastrado: {placa}.")

    def buscar(self, placa):
        """Encontra um veículo sem depender da ordem de cadastro.

        Args:
            placa (str): Identificação procurada.

        Returns:
            Veiculo: Cadastro mantido pela oficina.

        Raises:
            TypeError: Se a placa não for texto.
            ValueError: Se a identificação for inválida ou desconhecida.
        """
        placa = Validacao.placa(placa)
        try:
            return self._veiculos.buscar(partial(self._mesma_placa, placa))
        except ValueError:
            raise ValueError(f"Veículo não cadastrado: {placa}.") from None

    @staticmethod
    def _mesma_placa(placa, veiculo):
        """Compara uma placa normalizada com um cadastro.

        Args:
            placa (str): Identificação procurada.
            veiculo (Veiculo): Cadastro examinado pela lista.

        Returns:
            bool: Indica se a identificação corresponde ao cadastro.
        """
        return veiculo.placa == placa

    def listar(self):
        """Disponibiliza os cadastros na ordem em que foram incluídos.

        Returns:
            Iterator: Veículos mantidos pela oficina.
        """
        return iter(self._veiculos)
