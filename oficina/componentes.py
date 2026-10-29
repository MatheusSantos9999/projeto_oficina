"""Identificação dos componentes e estados permitidos para a avaliação."""
from enum import Enum
from functools import partial

from estrutura_de_dados import NoArvore
from oficina.validacao import Validacao


class EstadoComponente(Enum):
    """Distingue ausência de avaliação dos resultados informados pelo avaliador.

    Attributes:
        NAO_AVALIADO: Componente ainda não examinado.
        SEM_DEFEITO_IDENTIFICADO: Avaliação sem defeito identificado.
        COM_DEFEITO: Avaliação que identificou um defeito.
    """

    NAO_AVALIADO = "Não avaliado"
    SEM_DEFEITO_IDENTIFICADO = "Sem defeito identificado"
    COM_DEFEITO = "Com defeito"


class Componente:
    """Descreve uma peça ou conjunto sem guardar resultados de atendimentos.

    Attributes:
        codigo (str): Identificador normalizado e somente leitura.
        nome (str): Descrição editável, validada antes da atribuição.
    """

    def __init__(self, codigo, nome):
        """Cria a identificação de uma peça ou conjunto.

        Args:
            codigo (str): Identificador único dentro da árvore.
            nome (str): Nome do componente.

        Raises:
            TypeError: Se os argumentos não forem textos.
            ValueError: Se algum argumento for inválido ou vazio.
        """
        self._codigo = Validacao.codigo(codigo)
        self.nome = nome

    @property
    def codigo(self):
        """str: Identificador estável, sem setter para preservar as referências."""
        return self._codigo

    @property
    def nome(self):
        """str: Descrição do componente."""
        return self._nome

    @nome.setter
    def nome(self, valor):
        """Valida a nova descrição antes de substituir a anterior.

        Args:
            valor (str): Descrição não vazia.

        Raises:
            TypeError: Se o valor não for texto.
            ValueError: Se a descrição estiver vazia.
        """
        self._nome = Validacao.texto(valor, "Nome do componente")

    def copiar(self):
        """Produz uma descrição independente da original.

        Returns:
            Componente: Cópia com o mesmo código e nome.
        """
        return Componente(self.codigo, self.nome)

    @staticmethod
    def buscar_no(raiz, codigo):
        """Localiza o componente usando o percurso da árvore já implementada.

        Args:
            raiz (NoArvore): Raiz da árvore de componentes do veículo.
            codigo (str): Identificador procurado.

        Returns:
            NoArvore: Nó existente que contém o componente procurado.

        Raises:
            TypeError: Se a raiz ou o código tiverem tipos incorretos.
            ValueError: Se o código for inválido ou não estiver na árvore.
        """
        Validacao.tipo(raiz, NoArvore, "Raiz")
        codigo = Validacao.codigo(codigo)
        candidatos = filter(partial(Componente._corresponde, codigo), raiz.pre_ordem())
        try:
            no, _ = next(candidatos)
        except StopIteration:
            raise ValueError(f"Componente não encontrado: {codigo}.") from None
        return no

    @staticmethod
    def _corresponde(codigo, par):
        """Compara o identificador com um componente visitado na árvore.

        Args:
            codigo (str): Identificador normalizado.
            par (tuple): Nó e profundidade fornecidos por NoArvore.pre_ordem.

        Returns:
            bool: Indica se o nó contém o componente procurado.
        """
        return par[0].dado.codigo == codigo
