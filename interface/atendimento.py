"""Gerenciar a espera e abrir ordens por prioridade."""
from servico.gestao_servicos import GestaoServicos

from oficina.validacao import Validacao
from interface.entrada import Entrada


class MenuAtendimento:
    """Gerenciar a espera e abrir ordens por prioridade."""

    OPCOES = (
        ('7', 'Enfileirar veículo', 'enfileirar'),
        ('8', 'Atender próximo veículo', 'atender'),
        ('9', 'Consultar filas e ordens', 'listar_ordens'),
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

    def enfileirar(self):
        """Solicita a categoria de atendimento do veículo.

        Raises:
            ValueError: Se a opção, o veículo ou sua disponibilidade forem inválidos.
            EOFError: Se a entrada for encerrada.
        """
        placa = input("Placa do veículo: ")
        print("1 Normal | 2 Prioritário")
        prioritario = Entrada.escolher({"1": False, "2": True}, input("Categoria: "))
        self._servicos.enfileirar(placa, prioritario)

    def atender(self):
        """Abre uma ordem para o próximo veículo, respeitando a prioridade.

        Raises:
            ValueError: Se o código estiver inválido ou repetido.
            IndexError: Se não houver veículos aguardando.
            EOFError: Se a entrada for encerrada.
        """
        ordem = self._servicos.atender_proximo(input("Código da nova ordem: "))
        print(f"Atendimento iniciado: {ordem.codigo} | {ordem.placa}")

    def listar_ordens(self):
        """Mostra a ordem de espera e o estado dos serviços.
        """
        print("Fila: " + ", ".join(v.placa for v in self._servicos.atendimento.listar()))
        for ordem in self._servicos.listar_ordens():
            print(f"{ordem.codigo} | {ordem.placa} | {ordem.situacao.value} | R$ {ordem.total:.2f}")
