"""Saldo e consumo FIFO dos lotes de um único produto."""
from functools import partial
from operator import eq
from estrutura_de_dados import ListaEncadeada, Fila
from oficina.validacao import Validacao
from estoque.lote import Lote
from estoque.consumo import ConsumoLote


class LotesProduto:
    """Mantém lotes e prepara retiradas sem alterar o saldo original."""

    def __init__(self, codigo):
        """Inicializa o saldo de um produto.

        Args:
            codigo (str): Identificação do produto dono dos lotes.

        Raises:
            TypeError: Se o código não for texto.
            ValueError: Se o código for inválido.
        """
        self._codigo = Validacao.codigo(codigo)
        self._lotes = Fila()
        self._codigos_lotes = ListaEncadeada()

    @property
    def saldo(self):
        """int: Soma dos saldos da fila de lotes."""
        return sum(lote.quantidade for lote in self._lotes)

    def receber_lote(self, lote):
        """Acrescenta uma cópia do lote ao final da fila.

        Args:
            lote (Lote): Lote recebido com saldo positivo.

        Raises:
            TypeError: Se o argumento não for lote.
            ValueError: Se o código já foi usado ou não houver saldo.
        """
        Validacao.tipo(lote, Lote, "Lote")
        self._validar_lote_livre(lote.codigo)
        copia = lote.copiar()
        self._lotes.enfileirar(copia)
        self._codigos_lotes.adicionar_final(lote.codigo)

    def _validar_lote_livre(self, codigo):
        """Recusa códigos de lotes já recebidos, inclusive esgotados.

        Args:
            codigo (str): Identificador normalizado.

        Raises:
            ValueError: Se o código já tiver sido utilizado.
        """
        try:
            self._codigos_lotes.buscar(partial(eq, codigo))
        except ValueError:
            return
        raise ValueError("Código de lote já recebido para este produto.")

    def listar_lotes(self):
        """Disponibiliza cópias dos lotes na ordem de consumo.

        Returns:
            Iterator: Cópias independentes dos lotes com saldo.
        """
        return (lote.copiar() for lote in self._lotes)

    def planejar_consumo(self, quantidade):
        """Prepara a retirada em uma fila copiada, sem modificar o estoque.

        Args:
            quantidade (int): Total solicitado para este produto.

        Returns:
            tuple: Fila restante e lista de retiradas planejadas.

        Raises:
            TypeError: Se a quantidade não for inteira.
            ValueError: Se a quantidade for inválida ou faltar estoque.
        """
        quantidade = Validacao.quantidade(quantidade)
        Validacao.exigir(quantidade <= self.saldo, f"Estoque insuficiente: {self._codigo}.")
        copia = self._copiar_lotes()
        movimentos = ListaEncadeada()
        self._consumir_copia(copia, quantidade, movimentos)
        return copia, movimentos

    def _copiar_lotes(self):
        """Copia a fila usando a estrutura própria.

        Returns:
            Fila: Nova fila com saldos independentes.
        """
        copia = Fila()
        for lote in self._lotes:
            copia.enfileirar(lote.copiar())
        return copia

    def _consumir_copia(self, fila, quantidade, movimentos):
        """Retira dos lotes copiados até completar o pedido.

        Args:
            fila (Fila): Fila copiada com saldo suficiente.
            quantidade (int): Unidades restantes.
            movimentos (ListaEncadeada): Recebe os registros planejados.
        """
        for _ in range(len(fila)):
            try:
                (True,).index(quantidade > 0)
            except ValueError:
                return
            retirada = self._retirar_lote(fila, quantidade)
            quantidade -= retirada.quantidade
            movimentos.adicionar_final(retirada)

    def _retirar_lote(self, fila, quantidade):
        """Consome a frente da fila, mantendo lotes parcialmente usados.

        Args:
            fila (Fila): Fila copiada com pelo menos um lote.
            quantidade (int): Unidades ainda solicitadas.

        Returns:
            ConsumoLote: Retirada efetuada somente na cópia.
        """
        lote = fila.frente
        retirada = ConsumoLote(self._codigo, lote, min(quantidade, lote.quantidade))
        lote.retirar(retirada.quantidade)
        try:
            (False,).index(lote.quantidade == 0)
        except ValueError:
            fila.desenfileirar()
        return retirada

    def _confirmar(self, fila):
        """Publica a fila preparada internamente pela baixa de estoque.

        Args:
            fila (Fila): Cópia já validada durante o planejamento completo.
        """
        self._lotes = fila
