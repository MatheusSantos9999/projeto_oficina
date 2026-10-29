"""Navegação e despacho dos comandos do terminal."""
from functools import partial
from itertools import count
from oficina.oficina import Oficina
from oficina.validacao import Validacao
from interface.entrada import Entrada
from interface.encerramento import EncerrarMenu
from interface.relatorio_ordem import RelatorioOrdem
from interface.cadastros import MenuCadastros
from interface.estoque import MenuEstoque
from interface.atendimento import MenuAtendimento
from interface.orcamento import MenuOrcamento
from interface.execucao import MenuExecucao


class Menu:
    """Seleciona ações e trata erros de interação, sem executar regras de negócio."""

    def __init__(self, oficina):
        """Monta os comandos ligados aos mesmos responsáveis da oficina.

        Args:
            oficina (Oficina): Instância compartilhada durante a sessão.

        Raises:
            TypeError: Se o argumento não for uma oficina.
        """
        Validacao.tipo(oficina, Oficina, "Oficina")
        self._opcoes = {}
        self._registrar(MenuCadastros(oficina.clientes, oficina.veiculos))
        self._registrar(MenuEstoque(oficina.estoque))
        self._registrar(MenuAtendimento(oficina.servicos))
        self._registrar(MenuOrcamento(oficina.servicos))
        self._registrar(MenuExecucao(oficina.servicos))
        consulta = partial(RelatorioOrdem.detalhar, oficina.servicos)
        self._opcoes["20"] = ("Detalhar ordem, diagnóstico e consumos", consulta)
        self._opcoes["0"] = ("Voltar ou encerrar o menu", self.sair)

    def _registrar(self, grupo):
        """Liga as opções declaradas pelo grupo às suas ações.

        Args:
            grupo (object): Grupo interno com OPCOES e métodos correspondentes.
        """
        for codigo, rotulo, nome in grupo.OPCOES:
            self._opcoes[codigo] = (rotulo, getattr(grupo, nome))

    def rodar(self):
        """Mantém o menu ativo até a saída ou o encerramento da entrada.
        """
        for _ in count():
            try:
                self._passo()
            except EncerrarMenu:
                return
            except (EOFError, KeyboardInterrupt):
                print("\nMenu encerrado.")
                return
            except (TypeError, ValueError, IndexError, RuntimeError) as erro:
                print(f"Não foi possível concluir: {erro}")

    def _passo(self):
        """Apresenta as opções e despacha a ação selecionada.

        Raises:
            EncerrarMenu: Se a saída for solicitada.
            ValueError: Se a opção ou os dados forem inválidos.
            EOFError: Se a entrada for encerrada.
        """
        for codigo in sorted(self._opcoes, key=self._ordem_opcao):
            print(f"{codigo} - {self._opcoes[codigo][0]}")
        _, acao = Entrada.escolher(self._opcoes, input("Opção: "))
        acao()
        print("Operação concluída.")

    @staticmethod
    def sair():
        """Solicita saída sem tratar a escolha como erro.

        Raises:
            EncerrarMenu: Sinaliza a saída solicitada.
        """
        raise EncerrarMenu()

    @staticmethod
    def _ordem_opcao(codigo):
        """Ordena os comandos numericamente e coloca a saída ao final.

        Args:
            codigo (str): Número da opção cadastrada.

        Returns:
            tuple: Indicador de saída e número da opção.
        """
        return codigo == "0", int(codigo)
