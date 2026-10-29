"""Conduzir execução, remontagem e quitação da ordem."""
from servico.gestao_servicos import GestaoServicos

from oficina.validacao import Validacao
from interface.entrada import Entrada


class MenuExecucao:
    """Conduzir execução, remontagem e quitação da ordem."""

    OPCOES = (
        ('15', 'Iniciar execução e baixar peças', 'executar_ordem'),
        ('16', 'Registrar desmontagem', 'desmontar'),
        ('17', 'Remontar última peça retirada', 'remontar'),
        ('18', 'Concluir serviço', 'concluir'),
        ('19', 'Registrar pagamento simulado', 'pagar'),
    )

    def __init__(self, servicos):
        """Recebe os responsáveis usados pelas ações do terminal.

        Args:
            servicos (GestaoServicos): Dependência compartilhada desta operação.

        Raises:
            TypeError: Se alguma dependência tiver tipo incorreto.
        """
        Validacao.tipo(servicos, GestaoServicos, "GestaoServicos")
        self._servicos = servicos

    def executar_ordem(self):
        """Inicia o reparo e confirma a baixa de todas as peças.

        Raises:
            ValueError: Se faltar estoque ou houver código inválido.
            RuntimeError: Se a ordem não estiver aprovada.
            EOFError: Se a entrada for encerrada.
        """
        ordem = Entrada.ordem(self._servicos)
        self._servicos.executar_ordem(ordem.codigo)

    def desmontar(self):
        """Empilha a peça retirada nesta ordem.

        Raises:
            ValueError: Se o componente não existir ou já estiver desmontado.
            RuntimeError: Se a ordem não estiver em execução.
            EOFError: Se a entrada for encerrada.
        """
        ordem = Entrada.ordem(self._servicos)
        ordem.desmontar(input("Código do componente retirado: "))

    def remontar(self):
        """Recoloca e apresenta a última peça retirada.

        Raises:
            IndexError: Se não houver peças desmontadas.
            RuntimeError: Se a ordem não estiver em execução.
            EOFError: Se a entrada for encerrada.
        """
        codigo = Entrada.ordem(self._servicos).remontar()
        print(f"Peça recolocada: {codigo}")

    def concluir(self):
        """Conclui o reparo sem efetuar pagamento.

        Raises:
            RuntimeError: Se a execução não começou ou houver peças desmontadas.
            ValueError: Se a ordem não existir.
            EOFError: Se a entrada for encerrada.
        """
        Entrada.ordem(self._servicos).concluir()

    def pagar(self):
        """Registra uma quitação integral simulada.

        Raises:
            ValueError: Se a escolha ou a ordem forem inválidas.
            RuntimeError: Se a ordem não estiver concluída ou já estiver paga.
            EOFError: Se a entrada for encerrada.
        """
        ordem = Entrada.ordem(self._servicos)
        pagamento = self._servicos.pagar_ordem(ordem.codigo, Entrada.forma_pagamento())
        print(f"SIMULAÇÃO: {pagamento.forma.value} | R$ {pagamento.valor:.2f} | sem cobrança externa")
