"""Organização da espera por atendimento com prioridade absoluta."""
from itertools import chain
from estrutura_de_dados import Fila
from oficina.validacao import Validacao
from oficina.veiculo import Veiculo

class Atendimento:
    """Mantém duas filas FIFO e atende sempre a fila prioritária primeiro."""

    def __init__(self):
        """Cria as filas normal e prioritária.
        """
        self._normal = Fila()
        self._prioritaria = Fila()

    @property
    def quantidade_normal(self):
        """int: Veículos aguardando na fila normal."""
        return len(self._normal)

    @property
    def quantidade_prioritaria(self):
        """int: Veículos aguardando na fila prioritária."""
        return len(self._prioritaria)

    def adicionar(self, veiculo, prioritario=False):
        """Enfileira um veículo sem permitir duplicidade nas filas.

        Args:
            veiculo (Veiculo): Cadastro que aguardará atendimento.
            prioritario (bool): Indica entrada na fila prioritária.

        Raises:
            TypeError: Se os argumentos tiverem tipos incorretos.
            ValueError: Se a placa já estiver em uma fila.
        """
        Validacao.tipo(veiculo, Veiculo, "Veículo")
        Validacao.exigir(type(prioritario) is bool, "Prioridade deve ser booleana.", TypeError)
        Validacao.exigir(not self.contem(veiculo.placa), "Veículo já está aguardando atendimento.")
        fila = (self._normal, self._prioritaria)[prioritario]
        fila.enfileirar(veiculo)

    def contem(self, placa):
        """Verifica se o veículo já aguarda em alguma fila.

        Args:
            placa (str): Identificação procurada.

        Returns:
            bool: Indica se o veículo aguarda atendimento.

        Raises:
            TypeError: Se a placa não for texto.
            ValueError: Se a placa for inválida.
        """
        placa = Validacao.placa(placa)
        filas = (self._normal, self._prioritaria)
        return any(v.placa == placa for fila in filas for v in fila)

    def proximo(self):
        """Consulta o próximo veículo sem removê-lo.

        Returns:
            Veiculo: Primeiro prioritário ou primeiro normal.

        Raises:
            IndexError: Se as duas filas estiverem vazias.
        """
        try:
            return self._prioritaria.frente
        except IndexError:
            return self._normal.frente

    def retirar_proximo(self):
        """Retira o primeiro prioritário ou, na ausência dele, o primeiro normal.

        Returns:
            Veiculo: Cadastro retirado da fila.

        Raises:
            IndexError: Se as duas filas estiverem vazias.
        """
        try:
            return self._prioritaria.desenfileirar()
        except IndexError:
            return self._normal.desenfileirar()

    def listar(self):
        """Disponibiliza os veículos na ordem atual de atendimento.

        Returns:
            Iterator: Prioritários seguidos dos normais.
        """
        return chain(iter(self._prioritaria), iter(self._normal))

