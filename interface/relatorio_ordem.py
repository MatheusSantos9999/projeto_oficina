"""Apresentação do diagnóstico, orçamento e lotes usados."""
from interface.entrada import Entrada


class RelatorioOrdem:
    """Apresenta uma ordem sem alterar seus dados."""

    @staticmethod
    def detalhar(servicos):
        """Mostra a inspeção, os itens, os lotes usados e o pagamento.

        Args:
            servicos (GestaoServicos): Registro consultado pelo terminal.

        Raises:
            ValueError: Se a ordem não existir.
            EOFError: Se a entrada for encerrada.
        """
        ordem = Entrada.ordem(servicos)
        print(f"{ordem.codigo} | {ordem.placa} | {ordem.situacao.value}")
        print(f"Cliente: {ordem.diagnostico.cliente} | total R$ {ordem.total:.2f}")
        RelatorioOrdem.diagnostico(ordem)
        RelatorioOrdem.itens(ordem)
        RelatorioOrdem.consumos(ordem)
        forma = getattr(getattr(ordem.pagamento, "forma", None), "value", "Pendente")
        print(f"Pagamento simulado: {forma} | peças desmontadas: {ordem.pecas_desmontadas}")

    @staticmethod
    def diagnostico(ordem):
        """Mostra os resultados no mesmo formato hierárquico da árvore.

        Args:
            ordem (OrdemServico): Ordem selecionada.
        """
        for avaliacao, nivel in ordem.diagnostico.relatorio():
            print(f"{'  ' * nivel}{avaliacao.codigo}: {avaliacao.estado.value}")

    @staticmethod
    def itens(ordem):
        """Mostra preços e quantidades preservados no orçamento.

        Args:
            ordem (OrdemServico): Ordem selecionada.
        """
        for item in ordem.listar_itens():
            print(f"Item {item.produto}: {item.quantidade} x R$ {item.valor_unitario:.2f} = R$ {item.total:.2f}")
        print(f"Mão de obra: R$ {ordem.mao_obra:.2f}")

    @staticmethod
    def consumos(ordem):
        """Mostra a origem das unidades usadas na execução.

        Args:
            ordem (OrdemServico): Ordem selecionada.
        """
        for consumo in ordem.listar_consumos():
            print(f"Consumo {consumo.produto} / {consumo.lote}: {consumo.quantidade} unidades")
