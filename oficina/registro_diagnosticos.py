"""Abertura e consulta das visitas de diagnóstico."""
from functools import partial
from estrutura_de_dados import ListaEncadeada
from oficina.validacao import Validacao
from oficina.diagnostico import Diagnostico
from oficina.cadastro_veiculos import CadastroVeiculos


class RegistroDiagnosticos:
    """Preserva visitas independentes e seus identificadores únicos."""

    def __init__(self, veiculos):
        """Recebe o cadastro usado na abertura de visitas.

        Args:
            veiculos (CadastroVeiculos): Cadastro compartilhado dos veículos.

        Raises:
            TypeError: Se o cadastro tiver tipo incorreto.
        """
        Validacao.tipo(veiculos, CadastroVeiculos, "Cadastro de veículos")
        self._veiculos = veiculos
        self._diagnosticos = ListaEncadeada()

    @property
    def quantidade(self):
        """int: Quantidade de diagnósticos preservados pela oficina."""
        return len(self._diagnosticos)

    def abrir(self, identificador, placa):
        """Abre uma nova visita sem alterar diagnósticos anteriores.

        Args:
            identificador (str): Código único para este diagnóstico.
            placa (str): Identificação de um veículo já cadastrado.

        Returns:
            Diagnostico: Novo diagnóstico com componentes não avaliados.

        Raises:
            TypeError: Se os argumentos não forem textos.
            ValueError: Se o código estiver repetido ou o veículo não existir.
        """
        identificador = Validacao.codigo(identificador)
        self.validar_disponivel(identificador)
        veiculo = self._veiculos.buscar(placa)
        diagnostico = Diagnostico(identificador, veiculo)
        self._diagnosticos.adicionar_final(diagnostico)
        return diagnostico

    def validar_disponivel(self, identificador):
        """Impede a reutilização de um código de diagnóstico.

        Args:
            identificador (str): Código já normalizado.

        Raises:
            ValueError: Se o código já estiver registrado.
        """
        identificador = Validacao.codigo(identificador)
        try:
            self.buscar(identificador)
        except ValueError:
            return
        raise ValueError(f"Diagnóstico já cadastrado: {identificador}.")

    def buscar(self, identificador):
        """Encontra um diagnóstico aberto ou encerrado.

        Args:
            identificador (str): Código procurado.

        Returns:
            Diagnostico: Registro preservado pela oficina.

        Raises:
            TypeError: Se o identificador não for texto.
            ValueError: Se o código for inválido ou desconhecido.
        """
        identificador = Validacao.codigo(identificador)
        criterio = partial(self._mesmo_identificador, identificador)
        try:
            return self._diagnosticos.buscar(criterio)
        except ValueError:
            raise ValueError(f"Diagnóstico não encontrado: {identificador}.") from None

    @staticmethod
    def _mesmo_identificador(identificador, diagnostico):
        """Compara um identificador normalizado com um diagnóstico.

        Args:
            identificador (str): Código procurado.
            diagnostico (Diagnostico): Registro examinado pela lista.

        Returns:
            bool: Indica se o código corresponde ao registro.
        """
        return diagnostico.identificador == identificador

    def listar(self):
        """Disponibiliza todas as visitas, incluindo as encerradas.

        Returns:
            Iterator: Diagnósticos na ordem de abertura.
        """
        return iter(self._diagnosticos)

    def adicionar(self, diagnostico):
        """Preserva um diagnóstico preparado para a abertura de uma ordem.

        Args:
            diagnostico (Diagnostico): Visita a registrar.

        Raises:
            TypeError: Se o registro não for um diagnóstico.
            ValueError: Se o identificador já estiver em uso.
        """
        Validacao.tipo(diagnostico, Diagnostico, "Diagnóstico")
        self.validar_disponivel(diagnostico.identificador)
        self._diagnosticos.adicionar_final(diagnostico)
