"""Resultados individuais registrados durante um diagnóstico."""
from oficina.componentes import Componente, EstadoComponente
from oficina.validacao import Validacao


class Avaliacao:
    """Guarda um resultado que não pode ser editado pela interface pública.

    Attributes:
        codigo (str): Identificação do componente examinado.
        nome (str): Nome do componente no momento do registro.
        estado (EstadoComponente): Situação informada pelo avaliador.
        observacao (str): Descrição complementar, possivelmente vazia.

    Para corrigir um resultado, registra-se outra avaliação no diagnóstico.
    Assim, os registros anteriores permanecem disponíveis no histórico.
    """

    def __init__(self, componente, estado, observacao=""):
        """Valida os dados e guarda os valores do resultado.

        Args:
            componente (Componente): Peça ou conjunto examinado.
            estado (EstadoComponente): Resultado da avaliação.
            observacao (str): Descrição opcional.

        Raises:
            TypeError: Se algum argumento tiver um tipo incorreto.
        """
        Validacao.tipo(componente, Componente, "Componente")
        Validacao.tipo(estado, EstadoComponente, "Estado")
        self._observacao = Validacao.texto(observacao, "Observação", True)
        self._codigo = componente.codigo
        self._nome = componente.nome
        self._estado = estado

    @property
    def codigo(self):
        """str: Código do componente examinado, somente leitura."""
        return self._codigo

    @property
    def nome(self):
        """str: Nome preservado no resultado, somente leitura."""
        return self._nome

    @property
    def estado(self):
        """EstadoComponente: Resultado registrado, somente leitura."""
        return self._estado

    @property
    def observacao(self):
        """str: Observação preservada no resultado, somente leitura."""
        return self._observacao
