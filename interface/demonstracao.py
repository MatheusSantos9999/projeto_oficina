"""Demonstração automática com dados fictícios."""
from dados import DadosExemplo
from oficina.componentes import EstadoComponente
from servico.pagamento import FormaPagamento
from interface.relatorio_ordem import RelatorioOrdem


class Demonstracao:
    """Executa quatro serviços completos em uma oficina de dados fictícios."""

    @staticmethod
    def executar():
        """Mostra prioridade, consumo FIFO, remontagem e as quatro formas de pagamento.

        Returns:
            Oficina: Instância com quatro ordens pagas e histórico preservado.

        Raises:
            ValueError: Se dados editados impedirem o fluxo.
            RuntimeError: Se alguma etapa estiver inconsistente.
        """
        oficina = DadosExemplo.criar_oficina()
        Demonstracao._filas(oficina)
        for numero, forma in enumerate(FormaPagamento, 1):
            ordem = oficina.servicos.atender_proximo(f"OS{numero:03d}")
            Demonstracao._preparar(oficina, ordem)
            Demonstracao._executar(oficina, ordem, forma)
            Demonstracao._resumir(ordem)
        print(f"Saldo final de PASTILHA: {oficina.estoque.buscar_produto('PASTILHA').saldo}")
        return oficina

    @staticmethod
    def _filas(oficina):
        """Enfileira normais antes de prioritários para evidenciar a regra.

        Args:
            oficina (Oficina): Instância da demonstração.
        """
        print("DEMONSTRAÇÃO FICTÍCIA: todos os pagamentos são simulados.")
        for placa, prioridade in (("TST1A01", False), ("TST1A02", True), ("TST1A03", False), ("TST1A04", True)):
            oficina.servicos.enfileirar(placa, prioridade)
        print("Ordem de atendimento: " + ", ".join(v.placa for v in oficina.servicos.atendimento.listar()))

    @staticmethod
    def _preparar(oficina, ordem):
        """Registra inspeção e orçamento antes de aprovar.

        Args:
            oficina (Oficina): Instância da demonstração.
            ordem (OrdemServico): Ordem recém-aberta.
        """
        ordem.diagnostico.registrar("PASTILHA_DE", EstadoComponente.COM_DEFEITO, "Inspeção fictícia.")
        oficina.servicos.adicionar_item(ordem.codigo, "PASTILHA_DE", "PASTILHA", 2)
        ordem.definir_mao_obra("80.00")
        ordem.diagnostico.encerrar()
        ordem.aprovar()

    @staticmethod
    def _executar(oficina, ordem, forma):
        """Executa, remonta em ordem inversa e registra o pagamento.

        Args:
            oficina (Oficina): Instância da demonstração.
            ordem (OrdemServico): Serviço aprovado.
            forma (FormaPagamento): Forma simulada desta execução.
        """
        oficina.servicos.executar_ordem(ordem.codigo)
        ordem.desmontar("PASTILHA_DE")
        ordem.desmontar("DISCO_DE")
        for _ in range(2):
            print(f"{ordem.codigo}: remontagem de {ordem.remontar()}")
        ordem.concluir()
        oficina.servicos.pagar_ordem(ordem.codigo, forma)

    @staticmethod
    def _resumir(ordem):
        """Apresenta a quitação e os lotes usados no serviço.

        Args:
            ordem (OrdemServico): Ordem já quitada na simulação.
        """
        print(f"{ordem.codigo} | {ordem.placa} | {ordem.situacao.value} | {ordem.pagamento.forma.value} | R$ {ordem.total:.2f}")
        RelatorioOrdem.consumos(ordem)
