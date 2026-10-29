"""Coordenação das ordens e do atendimento prioritário."""
from functools import partial
from estrutura_de_dados import ListaEncadeada
from estoque.estoque import Estoque
from oficina.validacao import Validacao
from oficina.cadastro_veiculos import CadastroVeiculos
from oficina.registro_diagnosticos import RegistroDiagnosticos
from oficina.diagnostico import Diagnostico
from servico.atendimento import Atendimento
from servico.ordem_servico import OrdemServico, SituacaoOrdem


class GestaoServicos:
    """Coordena a visita sem assumir as regras internas do estoque ou da ordem."""

    def __init__(self, veiculos, diagnosticos, estoque):
        """Liga o atendimento aos cadastros e ao estoque da mesma oficina.

        Args:
            veiculos (CadastroVeiculos): Cadastro de carros atendidos.
            diagnosticos (RegistroDiagnosticos): Histórico de visitas.
            estoque (Estoque): Estoque compartilhado para execução.

        Raises:
            TypeError: Se alguma dependência tiver tipo incorreto.
        """
        Validacao.tipo(veiculos, CadastroVeiculos, "Cadastro de veículos")
        Validacao.tipo(diagnosticos, RegistroDiagnosticos, "Registro de diagnósticos")
        Validacao.tipo(estoque, Estoque, "Estoque")
        self._veiculos = veiculos
        self._diagnosticos = diagnosticos
        self._estoque = estoque
        self._ordens = ListaEncadeada()
        self._atendimento = Atendimento()

    @property
    def atendimento(self):
        """Atendimento: Filas normal e prioritária desta oficina."""
        return self._atendimento

    @property
    def quantidade_ordens(self):
        """int: Ordens abertas ou históricas."""
        return len(self._ordens)

    def enfileirar(self, placa, prioritario=False):
        """Coloca um veículo livre na fila correspondente.

        Args:
            placa (str): Veículo já cadastrado.
            prioritario (bool): Indica atendimento prioritário.

        Raises:
            TypeError: Se os argumentos tiverem tipos incorretos.
            ValueError: Se o veículo não existir, já aguardar ou possuir serviço não quitado.
        """
        veiculo = self._veiculos.buscar(placa)
        self._validar_veiculo_livre(veiculo.placa)
        self.atendimento.adicionar(veiculo, prioritario)

    def _validar_veiculo_livre(self, placa):
        """Impede duas ordens ativas para o mesmo veículo.

        Args:
            placa (str): Identificação normalizada.

        Raises:
            ValueError: Se o veículo já tiver uma ordem não paga.
        """
        ativas = filter(partial(self._ordem_do_veiculo, placa), self._ordens)
        Validacao.exigir(not any(o.situacao is not SituacaoOrdem.PAGA for o in ativas), "Veículo possui uma ordem ainda não quitada.")

    @staticmethod
    def _ordem_do_veiculo(placa, ordem):
        """Seleciona ordens pelo veículo.

        Args:
            placa (str): Identificação procurada.
            ordem (OrdemServico): Registro examinado.

        Returns:
            bool: Indica correspondência.
        """
        return ordem.placa == placa

    def atender_proximo(self, codigo):
        """Abre diagnóstico e ordem antes de retirar o próximo veículo da fila.

        Args:
            codigo (str): Identificador único usado na ordem e no diagnóstico.

        Returns:
            OrdemServico: Nova ordem em situação aberta.

        Raises:
            TypeError: Se o código não for texto.
            ValueError: Se o identificador for inválido ou repetido.
            IndexError: Se não houver veículos aguardando.
        """
        codigo = Validacao.codigo(codigo)
        self._validar_ordem_livre(codigo)
        self._diagnosticos.validar_disponivel(codigo)
        veiculo = self.atendimento.proximo()
        diagnostico = Diagnostico(codigo, veiculo)
        ordem = OrdemServico(codigo, diagnostico)
        self._diagnosticos.adicionar(diagnostico)
        self._ordens.adicionar_final(ordem)
        self.atendimento.retirar_proximo()
        return ordem

    def _validar_ordem_livre(self, codigo):
        """Recusa códigos de ordens já utilizados.

        Args:
            codigo (str): Identificação normalizada.

        Raises:
            ValueError: Se a ordem já existir.
        """
        try:
            self.buscar_ordem(codigo)
        except ValueError:
            return
        raise ValueError("Ordem de serviço já cadastrada.")

    def buscar_ordem(self, codigo):
        """Encontra uma ordem aberta ou histórica.

        Args:
            codigo (str): Identificador procurado.

        Returns:
            OrdemServico: Registro mantido pela oficina.

        Raises:
            TypeError: Se o código não for texto.
            ValueError: Se o código for inválido ou desconhecido.
        """
        codigo = Validacao.codigo(codigo)
        try:
            return self._ordens.buscar(partial(self._mesma_ordem, codigo))
        except ValueError:
            raise ValueError("Ordem de serviço não encontrada.") from None

    @staticmethod
    def _mesma_ordem(codigo, ordem):
        """Compara o identificador de uma ordem.

        Args:
            codigo (str): Identificação procurada.
            ordem (OrdemServico): Registro examinado.

        Returns:
            bool: Indica correspondência.
        """
        return ordem.codigo == codigo

    def listar_ordens(self):
        """Disponibiliza todas as ordens, inclusive as quitadas.

        Returns:
            Iterator: Ordens na sequência de abertura.
        """
        return iter(self._ordens)

    def adicionar_item(self, ordem, componente, produto, quantidade):
        """Liga explicitamente um produto do estoque ao componente atendido.

        Args:
            ordem (str): Identificador da ordem.
            componente (str): Código do componente do veículo.
            produto (str): Código comercial no estoque.
            quantidade (int): Unidades solicitadas.

        Returns:
            ItemServico: Item com preço preservado.

        Raises:
            TypeError: Se os tipos forem inválidos.
            ValueError: Se os registros não existirem ou a quantidade for inválida.
            RuntimeError: Se a ordem não estiver aberta.
        """
        registro = self.buscar_ordem(ordem)
        mercadoria = self._estoque.buscar_produto(produto)
        return registro.adicionar_item(componente, mercadoria, quantidade)

    def executar_ordem(self, codigo):
        """Inicia o serviço usando o estoque compartilhado.

        Args:
            codigo (str): Identificador da ordem.

        Raises:
            TypeError: Se o código não for texto.
            ValueError: Se a ordem não existir ou faltar estoque.
            RuntimeError: Se a ordem não estiver aprovada.
        """
        self.buscar_ordem(codigo).iniciar_execucao(self._estoque)

    def pagar_ordem(self, codigo, forma):
        """Registra a quitação simulada de uma ordem concluída.

        Args:
            codigo (str): Identificação da ordem.
            forma (FormaPagamento): Forma de pagamento escolhida.

        Returns:
            Pagamento: Registro da quitação integral.

        Raises:
            TypeError: Se os tipos forem incorretos.
            ValueError: Se a ordem não existir ou seu valor for inválido.
            RuntimeError: Se a ordem não estiver concluída ou já estiver paga.
        """
        return self.buscar_ordem(codigo).pagar(forma)
