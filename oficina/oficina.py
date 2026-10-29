"""Composição dos responsáveis por uma oficina em memória."""
from cliente.cadastro import CadastroClientes
from oficina.cadastro_veiculos import CadastroVeiculos
from oficina.registro_diagnosticos import RegistroDiagnosticos
from estoque.estoque import Estoque
from servico.gestao_servicos import GestaoServicos


class Oficina:
    """Reúne os serviços compartilhados, sem implementar cadastro, busca ou reparo."""

    def __init__(self):
        """Monta os responsáveis compartilhando as mesmas instâncias."""
        self._clientes = CadastroClientes()
        self._veiculos = CadastroVeiculos(self._clientes)
        self._diagnosticos = RegistroDiagnosticos(self._veiculos)
        self._estoque = Estoque()
        self._servicos = GestaoServicos(self._veiculos, self._diagnosticos, self._estoque)

    @property
    def clientes(self):
        """CadastroClientes: Cadastro compartilhado de clientes."""
        return self._clientes

    @property
    def veiculos(self):
        """CadastroVeiculos: Cadastro de veículos e vínculos."""
        return self._veiculos

    @property
    def diagnosticos(self):
        """RegistroDiagnosticos: Histórico das visitas."""
        return self._diagnosticos

    @property
    def estoque(self):
        """Estoque: Estoque usado pelas ordens."""
        return self._estoque

    @property
    def servicos(self):
        """GestaoServicos: Atendimento e coordenação das ordens."""
        return self._servicos
