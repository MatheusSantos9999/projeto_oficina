"""Cadastro de veículos e coordenação dos diagnósticos da oficina."""
from functools import partial

from estrutura_de_dados import ListaEncadeada
from oficina.diagnostico import Diagnostico
from oficina.validacao import Validacao
from oficina.veiculo import Veiculo


class Oficina:
    """Coordena os cadastros e diagnósticos com listas encadeadas próprias.

    Veículos são encontrados pela placa; diagnósticos, pelo identificador.
    A ordem de cadastro não limita qual registro pode ser consultado.
    Os dados permanecem somente em memória durante a execução.

    Attributes:
        quantidade_veiculos (int): Quantidade de veículos cadastrados.
        quantidade_diagnosticos (int): Total de diagnósticos, inclusive encerrados.

    Examples:
        >>> from oficina.componentes import Componente, EstadoComponente
        >>> oficina = Oficina()
        >>> carro = Veiculo("abc-1234", "Modelo de exemplo")
        >>> carro.adicionar_componente("VEICULO", Componente("MOTOR", "Motor"))
        >>> oficina.cadastrar_veiculo(carro)
        >>> visita = oficina.iniciar_diagnostico("VISITA-1", "ABC1234")
        >>> visita.consultar("MOTOR").estado is EstadoComponente.NAO_AVALIADO
        True
        >>> resultado = visita.registrar("MOTOR", EstadoComponente.COM_DEFEITO)
        >>> resultado.codigo
        'MOTOR'
        >>> oficina.encerrar_diagnostico("VISITA-1")
        >>> oficina.buscar_diagnostico("VISITA-1").encerrado
        True
    """

    def __init__(self):
        """Cria uma oficina sem veículos ou diagnósticos."""
        self._veiculos = ListaEncadeada()
        self._diagnosticos = ListaEncadeada()

    @property
    def quantidade_veiculos(self):
        """int: Quantidade atual de cadastros de veículos."""
        return len(self._veiculos)

    @property
    def quantidade_diagnosticos(self):
        """int: Quantidade de diagnósticos preservados pela oficina."""
        return len(self._diagnosticos)

    def cadastrar_veiculo(self, veiculo):
        """Inclui um cadastro sem permitir placas repetidas.

        Args:
            veiculo (Veiculo): Objeto a cadastrar.

        Raises:
            TypeError: Se o argumento não for um veículo.
            ValueError: Se a placa já estiver cadastrada.
        """
        Validacao.tipo(veiculo, Veiculo, "Veículo")
        self._validar_placa_livre(veiculo.placa)
        self._veiculos.adicionar_final(veiculo)

    def _validar_placa_livre(self, placa):
        """Verifica a disponibilidade de uma placa já normalizada.

        Args:
            placa (str): Identificação do novo cadastro.

        Raises:
            ValueError: Se a placa já estiver cadastrada.
        """
        try:
            self.buscar_veiculo(placa)
        except ValueError:
            return
        raise ValueError(f"Veículo já cadastrado: {placa}.")

    def buscar_veiculo(self, placa):
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

    def iniciar_diagnostico(self, identificador, placa):
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
        self._validar_identificador_livre(identificador)
        veiculo = self.buscar_veiculo(placa)
        diagnostico = Diagnostico(identificador, veiculo)
        self._diagnosticos.adicionar_final(diagnostico)
        return diagnostico

    def _validar_identificador_livre(self, identificador):
        """Impede a reutilização de um código de diagnóstico.

        Args:
            identificador (str): Código já normalizado.

        Raises:
            ValueError: Se o código já estiver registrado.
        """
        try:
            self.buscar_diagnostico(identificador)
        except ValueError:
            return
        raise ValueError(f"Diagnóstico já cadastrado: {identificador}.")

    def buscar_diagnostico(self, identificador):
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

    def registrar_avaliacao(self, identificador, codigo, estado, observacao=""):
        """Encaminha uma avaliação para o diagnóstico escolhido.

        Args:
            identificador (str): Código do diagnóstico.
            codigo (str): Código do componente.
            estado (EstadoComponente): Resultado da inspeção.
            observacao (str): Descrição opcional.

        Returns:
            Avaliacao: Resultado incluído no histórico.

        Raises:
            TypeError: Se algum argumento tiver um tipo incorreto.
            ValueError: Se um identificador ou estado for inválido.
            RuntimeError: Se o diagnóstico estiver encerrado.
        """
        diagnostico = self.buscar_diagnostico(identificador)
        return diagnostico.registrar(codigo, estado, observacao)

    def encerrar_diagnostico(self, identificador):
        """Encerra uma visita, mantendo o registro consultável.

        Args:
            identificador (str): Código do diagnóstico.

        Raises:
            TypeError: Se o identificador não for texto.
            ValueError: Se o código for inválido ou desconhecido.
            RuntimeError: Se a visita já estiver encerrada.
        """
        self.buscar_diagnostico(identificador).encerrar()

    def listar_veiculos(self):
        """Disponibiliza os cadastros na ordem em que foram incluídos.

        Returns:
            Iterator: Veículos mantidos pela oficina.
        """
        return iter(self._veiculos)

    def listar_diagnosticos(self):
        """Disponibiliza todas as visitas, incluindo as encerradas.

        Returns:
            Iterator: Diagnósticos na ordem de abertura.
        """
        return iter(self._diagnosticos)
