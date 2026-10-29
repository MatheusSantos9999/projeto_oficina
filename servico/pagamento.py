"""Pagamentos integrais simulados, sem conexão com bancos ou carteiras."""
from datetime import datetime, timezone
from enum import Enum
from oficina.validacao import Validacao


class FormaPagamento(Enum):
    """Formas aceitas para registrar uma quitação simulada."""

    PIX = "PIX"
    DEBITO = "Débito"
    CREDITO = "Crédito"
    BITCOIN = "Bitcoin"


class Pagamento:
    """Registra uma quitação simulada; todos os valores permanecem em reais."""

    def __init__(self, forma, valor):
        """Valida e registra a forma e o valor integral da ordem.

        Args:
            forma (FormaPagamento): Forma escolhida entre as quatro opções.
            valor (str | int | Decimal): Total em reais.

        Raises:
            TypeError: Se a forma ou o tipo monetário forem inválidos.
            ValueError: Se o valor não for positivo ou válido.

        Note:
            Bitcoin é somente uma opção de registro: não há cotação, conversão ou transferência.
        """
        Validacao.tipo(forma, FormaPagamento, "Forma de pagamento")
        self._valor = Validacao.dinheiro(valor)
        self._forma = forma
        self._instante = datetime.now(timezone.utc)

    @property
    def forma(self):
        """FormaPagamento: Forma escolhida para a simulação."""
        return self._forma

    @property
    def valor(self):
        """Decimal: Total quitado em reais."""
        return self._valor

    @property
    def instante(self):
        """datetime: Instante do registro em UTC."""
        return self._instante

    @property
    def simulado(self):
        """bool: Indica que não houve cobrança externa."""
        return True

