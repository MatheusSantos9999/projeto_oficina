"""Avaliações de um atendimento, isoladas de outros veículos e visitas."""
from functools import partial

from estrutura_de_dados import ListaEncadeada
from oficina.avaliacao import Avaliacao
from oficina.componentes import Componente, EstadoComponente
from oficina.validacao import Validacao
from oficina.veiculo import Veiculo


class Diagnostico:
    """Preserva a composição do veículo e o histórico de avaliações da visita.

    Attributes:
        identificador (str): Código único do diagnóstico na oficina.
        placa (str): Identificação do veículo no início da visita.
        modelo (str): Descrição do modelo no início da visita.
        cliente (str): Nome informado do cliente no início da visita.
        encerrado (bool): Impede novas avaliações quando verdadeiro.

    A árvore é copiada no início. Uma avaliação afeta somente o componente
    indicado; não modifica automaticamente os resultados dos pais ou filhos.
    Encerrar permite resultados não avaliados, que continuam explícitos.
    """

    def __init__(self, identificador, veiculo):
        """Abre um diagnóstico com uma cópia independente dos componentes.

        Args:
            identificador (str): Código da visita ou do diagnóstico.
            veiculo (Veiculo): Cadastro cuja composição será examinada.

        Raises:
            TypeError: Se os argumentos tiverem tipos incorretos.
            ValueError: Se o identificador for inválido.
        """
        Validacao.tipo(veiculo, Veiculo, "Veículo")
        self._identificador = Validacao.codigo(identificador)
        self._placa = veiculo.placa
        self._modelo = veiculo.modelo
        self._cliente = veiculo.cliente
        self._componentes = veiculo.copiar_componentes()
        self._avaliacoes = ListaEncadeada()
        self._encerrado = False

    @property
    def identificador(self):
        """str: Código estável do diagnóstico, somente leitura."""
        return self._identificador

    @property
    def placa(self):
        """str: Identificação preservada do veículo, somente leitura."""
        return self._placa

    @property
    def modelo(self):
        """str: Modelo preservado no início da visita, somente leitura."""
        return self._modelo

    @property
    def cliente(self):
        """str: Nome do cliente preservado no início da visita."""
        return self._cliente

    @property
    def encerrado(self):
        """bool: Indica que o registro de novas avaliações foi encerrado."""
        return self._encerrado

    def registrar(self, codigo, estado, observacao=""):
        """Acrescenta uma avaliação, mantendo as anteriores no histórico.

        Args:
            codigo (str): Identificação de um componente desta visita.
            estado (EstadoComponente): Resultado efetivo da inspeção.
            observacao (str): Descrição opcional do que foi observado.

        Returns:
            Avaliacao: Resultado registrado.

        Raises:
            TypeError: Se algum argumento tiver um tipo incorreto.
            ValueError: Se o componente não existir ou o estado for não avaliado.
            RuntimeError: Se o diagnóstico já estiver encerrado.
        """
        self._validar_aberto()
        Validacao.tipo(estado, EstadoComponente, "Estado")
        Validacao.exigir(estado is not EstadoComponente.NAO_AVALIADO, "Informe um resultado de avaliação.")
        componente = Componente.buscar_no(self._componentes, codigo).dado
        avaliacao = Avaliacao(componente, estado, observacao)
        # A primeira correspondência será sempre o resultado mais recente.
        self._avaliacoes.adicionar_inicio(avaliacao)
        return avaliacao

    def consultar(self, codigo):
        """Obtém a avaliação mais recente ou informa que a peça não foi avaliada.

        Args:
            codigo (str): Identificação do componente desta visita.

        Returns:
            Avaliacao: Último resultado ou um resultado com estado não avaliado.

        Raises:
            TypeError: Se o código não for texto.
            ValueError: Se o código for inválido ou não existir nesta árvore.
        """
        no = Componente.buscar_no(self._componentes, codigo)
        return self._consultar_componente(no.dado)

    def _consultar_componente(self, componente):
        """Obtém o resultado de um componente já localizado na árvore.

        Args:
            componente (Componente): Descrição pertencente a este diagnóstico.

        Returns:
            Avaliacao: Último resultado ou indicação de ausência de avaliação.
        """
        criterio = partial(self._mesmo_codigo, componente.codigo)
        try:
            return self._avaliacoes.buscar(criterio)
        except ValueError:
            return Avaliacao(componente, EstadoComponente.NAO_AVALIADO)

    @staticmethod
    def _mesmo_codigo(codigo, avaliacao):
        """Seleciona os registros do componente solicitado.

        Args:
            codigo (str): Identificação procurada.
            avaliacao (Avaliacao): Registro examinado pela lista.

        Returns:
            bool: Indica se o registro pertence ao componente.
        """
        return avaliacao.codigo == codigo

    def relatorio(self):
        """Percorre a hierarquia com o resultado atual de cada componente.

        Yields:
            tuple: Avaliação atual e profundidade do componente na árvore.

        Note:
            Não registre novas avaliações durante o consumo do iterador.
            Para n componentes e m registros, o custo é O(n * (m + 1)).
        """
        for no, nivel in self._componentes.pre_ordem():
            yield self._consultar_componente(no.dado), nivel

    def historico(self):
        """Disponibiliza as avaliações da mais recente para a mais antiga.

        Returns:
            Iterator: Registros preservados, inclusive avaliações substituídas.
        """
        return iter(self._avaliacoes)

    def _validar_aberto(self):
        """Impede alterações depois do encerramento.

        Raises:
            RuntimeError: Se o diagnóstico estiver encerrado.
        """
        Validacao.exigir(not self.encerrado, "O diagnóstico está encerrado.", RuntimeError)

    def encerrar(self):
        """Bloqueia novos registros sem excluir resultados ou histórico.

        Raises:
            RuntimeError: Se o diagnóstico já tiver sido encerrado.

        Note:
            O encerramento não atesta que o veículo esteja sem defeitos.
        """
        self._validar_aberto()
        self._encerrado = True
