"""Dados de Lote usados nas operações de estoque."""
from oficina.validacao import Validacao


class Lote:
    """Representa um lote de entrada e seu saldo disponível."""

    def __init__(self, codigo, quantidade, custo_unitario):
        """Valida um lote antes de colocá-lo no estoque.

        Args:
            codigo (str): Identificador do lote dentro do produto.
            quantidade (int): Unidades recebidas.
            custo_unitario (str | int | Decimal): Custo por unidade em reais.

        Raises:
            TypeError: Se algum argumento tiver tipo inválido.
            ValueError: Se o código, quantidade ou custo forem inválidos.
        """
        self._codigo = Validacao.codigo(codigo)
        self._quantidade = Validacao.quantidade(quantidade)
        self._custo_unitario = Validacao.dinheiro(custo_unitario)

    @property
    def codigo(self):
        """str: Identificador estável do lote."""
        return self._codigo

    @property
    def quantidade(self):
        """int: Saldo de unidades ainda disponíveis."""
        return self._quantidade

    @property
    def custo_unitario(self):
        """Decimal: Custo registrado na entrada."""
        return self._custo_unitario

    def retirar(self, quantidade):
        """Diminui o saldo após conferir a quantidade solicitada.

        Args:
            quantidade (int): Unidades a retirar.

        Raises:
            TypeError: Se a quantidade não for inteira.
            ValueError: Se a retirada for inválida ou exceder o saldo.
        """
        quantidade = Validacao.quantidade(quantidade)
        Validacao.exigir(quantidade <= self.quantidade, "Saldo insuficiente no lote.")
        self._quantidade -= quantidade

    def copiar(self):
        """Cria um lote independente com os mesmos dados.

        Returns:
            Lote: Cópia de um lote com saldo positivo.

        Raises:
            ValueError: Se o lote já estiver esgotado.
        """
        return Lote(self.codigo, self.quantidade, self.custo_unitario)
