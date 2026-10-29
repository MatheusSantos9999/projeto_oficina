"""Leitura e conversão das entradas de terminal."""
from oficina.validacao import Validacao
from servico.pagamento import FormaPagamento


class Entrada:
    """Converte entradas de terminal sem alterar os objetos da oficina."""

    @staticmethod
    def escolher(opcoes, escolha):
        """Resolve uma opção entre os valores previamente apresentados.

        Args:
            opcoes (dict): Mapeamento de opções conhecidas.
            escolha (str): Texto digitado pelo usuário.

        Returns:
            object: Valor associado à opção.

        Raises:
            ValueError: Se a opção não estiver no menu.
        """
        try:
            return opcoes[escolha.strip()]
        except KeyError:
            raise ValueError("Opção inválida. Escolha um dos números apresentados.") from None

    @staticmethod
    def quantidade():
        """Lê uma quantidade inteira positiva.

        Returns:
            int: Quantidade validada.

        Raises:
            ValueError: Se a entrada não for inteira positiva.
            EOFError: Se a entrada do terminal for encerrada.
        """
        try:
            valor = int(input("Quantidade: "))
        except ValueError:
            raise ValueError("Digite uma quantidade inteira.") from None
        return Validacao.quantidade(valor)

    @staticmethod
    def valor(mensagem):
        """Lê um valor decimal aceitando ponto ou vírgula.

        Args:
            mensagem (str): Solicitação apresentada ao usuário.

        Returns:
            str: Texto para validação monetária no domínio.

        Raises:
            EOFError: Se a entrada do terminal for encerrada.
        """
        return input(mensagem).strip().replace(",", ".")

    @staticmethod
    def forma_pagamento():
        """Apresenta as quatro formas de pagamento simulado.

        Returns:
            FormaPagamento: Forma escolhida.

        Raises:
            ValueError: Se a escolha for inválida.
            EOFError: Se a entrada for encerrada.
        """
        print("1 PIX | 2 Débito | 3 Crédito | 4 Bitcoin (simulado, total em reais)")
        opcoes = {str(i): forma for i, forma in enumerate(FormaPagamento, 1)}
        return Entrada.escolher(opcoes, input("Forma: "))

    @staticmethod
    def ordem(servicos):
        """Lê o identificador de uma ordem existente.

        Args:
            servicos (GestaoServicos): Responsável pela consulta das ordens.

        Returns:
            OrdemServico: Ordem localizada.

        Raises:
            ValueError: Se o código não existir.
            EOFError: Se a entrada for encerrada.
        """
        return servicos.buscar_ordem(input("Código da ordem: "))
