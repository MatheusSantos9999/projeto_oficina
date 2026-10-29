"""Ciclo de vida e regras de uma ordem de serviço."""
from decimal import Decimal
from enum import Enum
from estrutura_de_dados import ListaEncadeada, Pilha
from estoque.estoque import Estoque
from estoque.pedido import PedidoEstoque
from oficina.diagnostico import Diagnostico
from oficina.validacao import Validacao
from servico.item_servico import ItemServico
from servico.pagamento import Pagamento


class SituacaoOrdem(Enum):
    """Etapas permitidas da abertura até a quitação simulada."""

    ABERTA = "Aberta"
    APROVADA = "Aprovada"
    EM_EXECUCAO = "Em execução"
    CONCLUIDA = "Concluída"
    PAGA = "Paga"


class OrdemServico:
    """Controla o serviço de uma visita e impede execução ou pagamento repetidos."""

    def __init__(self, codigo, diagnostico):
        """Abre uma ordem associada a um diagnóstico.

        Args:
            codigo (str): Identificador único da ordem.
            diagnostico (Diagnostico): Avaliação inicial da visita.

        Raises:
            TypeError: Se os tipos forem incorretos.
            ValueError: Se o código for inválido.
        """
        Validacao.tipo(diagnostico, Diagnostico, "Diagnóstico")
        self._codigo = Validacao.codigo(codigo)
        self._diagnostico = diagnostico
        self._itens = ListaEncadeada()
        self._mao_obra = Decimal("0.00")
        self._situacao = SituacaoOrdem.ABERTA
        self._iniciar_controles()

    def _iniciar_controles(self):
        """Inicializa consumo, desmontagem e pagamento da visita.
        """
        self._consumos = ListaEncadeada()
        self._desmontagem = Pilha()
        self._operacoes = ListaEncadeada()
        self._pagamento = None

    @property
    def codigo(self):
        """str: Identificador estável da ordem."""
        return self._codigo

    @property
    def diagnostico(self):
        """Diagnostico: Registro de inspeção associado à visita."""
        return self._diagnostico

    @property
    def placa(self):
        """str: Placa preservada pelo diagnóstico."""
        return self.diagnostico.placa

    @property
    def situacao(self):
        """SituacaoOrdem: Etapa atual do serviço."""
        return self._situacao

    @property
    def mao_obra(self):
        """Decimal: Valor total de mão de obra."""
        return self._mao_obra

    @property
    def total(self):
        """Decimal: Soma dos itens e da mão de obra."""
        return sum((item.total for item in self._itens), self.mao_obra)

    @property
    def pagamento(self):
        """Pagamento | None: Quitação simulada, quando registrada."""
        return self._pagamento

    @property
    def pecas_desmontadas(self):
        """int: Quantidade de peças ainda fora do veículo."""
        return len(self._desmontagem)

    def _exigir_situacao(self, esperada):
        """Recusa operações incompatíveis com a etapa atual.

        Args:
            esperada (SituacaoOrdem): Etapa necessária para a operação.

        Raises:
            RuntimeError: Se a ordem estiver em outra etapa.
        """
        Validacao.exigir(self.situacao is esperada, f"Operação exige ordem {esperada.value.lower()}.", RuntimeError)

    def adicionar_item(self, componente, produto, quantidade):
        """Inclui um produto para um componente existente no diagnóstico.

        Args:
            componente (str): Componente que receberá o produto.
            produto (Produto): Produto escolhido explicitamente.
            quantidade (int): Unidades necessárias.

        Returns:
            ItemServico: Registro incluído na ordem.

        Raises:
            TypeError: Se algum tipo for inválido.
            ValueError: Se o componente ou a quantidade forem inválidos.
            RuntimeError: Se a ordem não estiver aberta.
        """
        self._exigir_situacao(SituacaoOrdem.ABERTA)
        avaliacao = self.diagnostico.consultar(componente)
        item = ItemServico(avaliacao.codigo, produto, quantidade)
        self._itens.adicionar_final(item)
        return item

    def definir_mao_obra(self, valor):
        """Define a cobrança de mão de obra antes da aprovação.

        Args:
            valor (str | int | Decimal): Total da mão de obra em reais.

        Raises:
            TypeError: Se o tipo monetário não for aceito.
            ValueError: Se o valor for inválido.
            RuntimeError: Se a ordem não estiver aberta.
        """
        self._exigir_situacao(SituacaoOrdem.ABERTA)
        self._mao_obra = Validacao.dinheiro(valor, permitir_zero=True)

    def aprovar(self):
        """Confirma o orçamento após o encerramento do diagnóstico.

        Raises:
            RuntimeError: Se o diagnóstico estiver aberto ou a ordem em outra etapa.
            ValueError: Se não houver valor de serviço válido.
        """
        self._exigir_situacao(SituacaoOrdem.ABERTA)
        Validacao.exigir(self.diagnostico.encerrado, "Encerre o diagnóstico antes de aprovar.", RuntimeError)
        Validacao.exigir(bool(self._itens) or self.mao_obra > 0, "Inclua itens ou mão de obra antes de aprovar.")
        Validacao.dinheiro(self.total)
        self._situacao = SituacaoOrdem.APROVADA

    def iniciar_execucao(self, estoque):
        """Baixa as peças uma única vez e inicia o serviço.

        Args:
            estoque (Estoque): Mesmo estoque compartilhado pela oficina.

        Raises:
            TypeError: Se o argumento não for estoque.
            ValueError: Se algum produto não existir ou faltar saldo.
            RuntimeError: Se a ordem não estiver aprovada.

        Note:
            Uma falha de validação mantém a ordem aprovada e preserva os saldos.
        """
        self._exigir_situacao(SituacaoOrdem.APROVADA)
        Validacao.tipo(estoque, Estoque, "Estoque")
        pedidos = self._pedidos()
        self._consumos = self._consumir_pedidos(estoque, pedidos)
        self._situacao = SituacaoOrdem.EM_EXECUCAO

    def _pedidos(self):
        """Transforma os itens em solicitações para o estoque.

        Returns:
            ListaEncadeada: Solicitações que podem repetir um mesmo produto.
        """
        pedidos = ListaEncadeada()
        for item in self._itens:
            pedidos.adicionar_final(PedidoEstoque(item.produto, item.quantidade))
        return pedidos

    @staticmethod
    def _consumir_pedidos(estoque, pedidos):
        """Permite serviços somente de mão de obra sem inventar uma baixa.

        Args:
            estoque (Estoque): Estoque compartilhado.
            pedidos (ListaEncadeada): Produtos solicitados.

        Returns:
            ListaEncadeada: Consumos confirmados ou coleção vazia.

        Raises:
            ValueError: Se houver produto inexistente ou saldo insuficiente.
        """
        try:
            (True,).index(bool(pedidos))
        except ValueError:
            return ListaEncadeada()
        return estoque.consumir(pedidos)

    def desmontar(self, componente):
        """Registra uma retirada na pilha desta ordem, sem apagar a árvore.

        Args:
            componente (str): Código da peça retirada.

        Raises:
            TypeError: Se o código não for texto.
            ValueError: Se a peça não existir ou já estiver desmontada.
            RuntimeError: Se o serviço não estiver em execução.
        """
        self._exigir_situacao(SituacaoOrdem.EM_EXECUCAO)
        codigo = self.diagnostico.consultar(componente).codigo
        Validacao.exigir(codigo not in self._desmontagem, "Componente já está desmontado.")
        self._desmontagem.empilhar(codigo)
        self._operacoes.adicionar_final(("Retirada", codigo))

    def remontar(self):
        """Recoloca a última peça retirada, seguindo a pilha.

        Returns:
            str: Código da peça recolocada.

        Raises:
            IndexError: Se não houver peça desmontada.
            RuntimeError: Se o serviço não estiver em execução.
        """
        self._exigir_situacao(SituacaoOrdem.EM_EXECUCAO)
        codigo = self._desmontagem.desempilhar()
        self._operacoes.adicionar_final(("Recolocada", codigo))
        return codigo

    def concluir(self):
        """Conclui o serviço depois de remontar todas as peças retiradas.

        Raises:
            RuntimeError: Se a execução não começou ou houver peças desmontadas.
        """
        self._exigir_situacao(SituacaoOrdem.EM_EXECUCAO)
        Validacao.exigir(self._desmontagem.vazia, "Há peças aguardando remontagem.", RuntimeError)
        self._situacao = SituacaoOrdem.CONCLUIDA

    def pagar(self, forma):
        """Registra uma única quitação integral simulada.

        Args:
            forma (FormaPagamento): PIX, débito, crédito ou Bitcoin.

        Returns:
            Pagamento: Registro da quitação simulada.

        Raises:
            TypeError: Se a forma de pagamento for inválida.
            ValueError: Se o total não for válido.
            RuntimeError: Se o serviço não estiver concluído ou já estiver pago.
        """
        self._exigir_situacao(SituacaoOrdem.CONCLUIDA)
        pagamento = Pagamento(forma, self.total)
        self._pagamento = pagamento
        self._situacao = SituacaoOrdem.PAGA
        return pagamento

    def listar_itens(self):
        """Disponibiliza os itens na ordem de inclusão.

        Returns:
            Iterator: Itens com preços preservados.
        """
        return iter(self._itens)

    def listar_consumos(self):
        """Disponibiliza as retiradas confirmadas do estoque.

        Returns:
            Iterator: Produtos, lotes, quantidades e custos consumidos.
        """
        return iter(self._consumos)

    def listar_operacoes(self):
        """Disponibiliza o histórico de desmontagem e remontagem.

        Returns:
            Iterator: Pares de operação e código do componente.
        """
        return iter(self._operacoes)
