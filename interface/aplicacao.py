"""Seleção do modo de execução e tratamento de falhas do terminal."""
import argparse
import sys
from itertools import count
from dados import DadosExemplo
from interface.menu import Menu
from interface.demonstracao import Demonstracao
from interface.entrada import Entrada
from interface.encerramento import EncerrarMenu


class Aplicacao:
    """Seleciona o menu ou a demonstração a partir do único main do projeto."""

    @staticmethod
    def _argumentos():
        """Lê o modo solicitado na linha de comando.

        Returns:
            Namespace: Modo inicial, menu ou demonstração.

        Raises:
            SystemExit: Se os argumentos forem inválidos ou a ajuda for solicitada.
        """
        parser = argparse.ArgumentParser(description="Oficina mecânica: exercício em memória.")
        grupo = parser.add_mutually_exclusive_group()
        grupo.add_argument("--demo", dest="modo", action="store_const", const="demo")
        grupo.add_argument("--menu", dest="modo", action="store_const", const="menu")
        parser.set_defaults(modo="inicio")
        return parser.parse_args()

    @staticmethod
    def executar():
        """Inicia o modo solicitado pelo terminal.
        """
        acoes = {"inicio": Aplicacao._inicio, "menu": Aplicacao._menu, "demo": Demonstracao.executar}
        acoes[Aplicacao._argumentos().modo]()

    @staticmethod
    def _menu():
        """Abre o menu com uma nova oficina preenchida com dados fictícios.
        """
        print("Dados fictícios em memória; pagamentos são somente simulados.")
        Menu(DadosExemplo.criar_oficina()).rodar()

    @staticmethod
    def _inicio():
        """Permite escolher menu ou demonstração até solicitar saída.
        """
        for _ in count():
            try:
                Aplicacao._escolher_modo()
            except (EncerrarMenu, EOFError, KeyboardInterrupt):
                return
            except (TypeError, ValueError, IndexError, RuntimeError) as erro:
                print(f"Não foi possível concluir: {erro}")

    @staticmethod
    def _escolher_modo():
        """Apresenta os dois modos no início do programa.

        Raises:
            ValueError: Se a opção for inválida.
            EncerrarMenu: Se a saída for solicitada.
            EOFError: Se a entrada for encerrada.
        """
        print("\n1 Operar a oficina | 2 Demonstração automática | 0 Sair")
        acoes = {"1": Aplicacao._menu, "2": Demonstracao.executar, "0": Menu.sair}
        Entrada.escolher(acoes, input("Modo: "))()

    @staticmethod
    def iniciar(nome_modulo):
        """Executa o programa somente pela chamada do arquivo principal.

        Args:
            nome_modulo (str): Valor de __name__ do arquivo.

        Raises:
            SystemExit: Código 1 quando a execução não puder continuar.
        """
        try:
            ("__main__",).index(nome_modulo)
        except ValueError:
            return
        try:
            Aplicacao.executar()
        except (TypeError, ValueError, IndexError, RuntimeError) as erro:
            print(f"Falha na execução: {erro}", file=sys.stderr)
            raise SystemExit(1) from erro
