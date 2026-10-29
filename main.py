"""Ponto de entrada principal para apresentar os veículos fictícios da oficina."""
import sys

from dados import DadosExemplo


class Aplicacao:
    """Carrega os dados de exemplo e apresenta os cadastros no terminal."""

    @staticmethod
    def executar():
        """Apresenta os clientes, veículos e componentes dos dados fictícios.

        Raises:
            TypeError: Se um dado de exemplo tiver tipo incorreto.
            ValueError: Se houver dados inválidos ou identificadores duplicados.
        """
        oficina = DadosExemplo.criar_oficina()
        print(f"Oficina: {oficina.quantidade_veiculos} veículos fictícios cadastrados.")
        for veiculo in oficina.listar_veiculos():
            Aplicacao._exibir_veiculo(veiculo)

    @staticmethod
    def _exibir_veiculo(veiculo):
        """Mostra o cadastro e sua hierarquia de componentes.

        Args:
            veiculo (Veiculo): Cadastro fictício a apresentar.
        """
        print(f"\n{veiculo.cliente} | {veiculo.placa} | {veiculo.modelo}")
        for componente, nivel in veiculo.percorrer_componentes():
            print(f"{'  ' * nivel}{componente.codigo}: {componente.nome}")

    @staticmethod
    def iniciar(nome_modulo):
        """Executa somente quando este arquivo é chamado como programa.

        Args:
            nome_modulo (str): Nome recebido da variável __name__ do módulo.

        Raises:
            SystemExit: Com código 1 quando os dados impedirem a execução.
        """
        try:
            ("__main__",).index(nome_modulo)
        except ValueError:
            return
        try:
            Aplicacao.executar()
        except (TypeError, ValueError, RuntimeError) as erro:
            print(f"Não foi possível carregar a oficina: {erro}", file=sys.stderr)
            raise SystemExit(1) from erro


Aplicacao.iniciar(__name__)
