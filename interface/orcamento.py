"""Registrar a inspeção e preparar o orçamento da visita."""
from servico.gestao_servicos import GestaoServicos
from oficina.componentes import EstadoComponente
from oficina.validacao import Validacao
from interface.entrada import Entrada


class MenuOrcamento:
    """Registrar a inspeção e preparar o orçamento da visita."""

    OPCOES = (
        ('10', 'Registrar avaliação do diagnóstico', 'avaliar'),
        ('11', 'Adicionar item à ordem', 'adicionar_item'),
        ('12', 'Definir mão de obra', 'mao_obra'),
        ('13', 'Encerrar diagnóstico', 'encerrar_diagnostico'),
        ('14', 'Aprovar orçamento', 'aprovar'),
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

    def avaliar(self):
        """Registra o resultado informado para um componente da visita.

        Raises:
            ValueError: Se algum código ou opção for inválido.
            RuntimeError: Se o diagnóstico estiver encerrado.
            EOFError: Se a entrada for encerrada.
        """
        ordem = Entrada.ordem(self._servicos)
        componente = input("Código do componente: ")
        print("1 Com defeito | 2 Sem defeito identificado")
        opcoes = {"1": EstadoComponente.COM_DEFEITO, "2": EstadoComponente.SEM_DEFEITO_IDENTIFICADO}
        estado = Entrada.escolher(opcoes, input("Resultado: "))
        ordem.diagnostico.registrar(componente, estado, input("Observação: "))

    def adicionar_item(self):
        """Solicita o produto que será usado no componente escolhido.

        Raises:
            ValueError: Se os códigos ou a quantidade forem inválidos.
            RuntimeError: Se a ordem não estiver aberta.
            EOFError: Se a entrada for encerrada.
        """
        ordem = Entrada.ordem(self._servicos)
        componente = input("Código do componente: ")
        produto = input("Código do produto: ")
        self._servicos.adicionar_item(ordem.codigo, componente, produto, Entrada.quantidade())

    def mao_obra(self):
        """Define a mão de obra total da ordem.

        Raises:
            ValueError: Se o valor for inválido.
            RuntimeError: Se a ordem não estiver aberta.
            EOFError: Se a entrada for encerrada.
        """
        ordem = Entrada.ordem(self._servicos)
        ordem.definir_mao_obra(Entrada.valor("Mão de obra em reais: "))

    def encerrar_diagnostico(self):
        """Encerra a avaliação sem concluir o reparo.

        Raises:
            ValueError: Se a ordem não existir.
            RuntimeError: Se o diagnóstico já estiver encerrado.
            EOFError: Se a entrada for encerrada.
        """
        Entrada.ordem(self._servicos).diagnostico.encerrar()

    def aprovar(self):
        """Aprova o orçamento e bloqueia novas alterações nos itens.

        Raises:
            ValueError: Se não houver valor de serviço válido.
            RuntimeError: Se a ordem ou o diagnóstico estiverem em etapa incompatível.
            EOFError: Se a entrada for encerrada.
        """
        Entrada.ordem(self._servicos).aprovar()
