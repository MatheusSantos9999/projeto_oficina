"""Validações compartilhadas pelos objetos da oficina."""
from re import fullmatch


class Validacao:
    """Reúne verificações de entrada sem alterar o estado dos objetos."""

    @staticmethod
    def exigir(condicao, mensagem, erro=ValueError):
        """Interrompe uma operação cuja condição obrigatória não foi atendida.

        Args:
            condicao (bool): Resultado da verificação.
            mensagem (str): Descrição da falha.
            erro (type): Classe da exceção a levantar.

        Raises:
            ValueError: Por padrão, quando a condição for falsa.
        """
        try:
            (True,).index(condicao)
        except ValueError:
            raise erro(mensagem) from None

    @staticmethod
    def tipo(valor, classe, campo):
        """Confere o tipo de uma entrada.

        Args:
            valor (object): Entrada a verificar.
            classe (type): Tipo aceito.
            campo (str): Nome usado na mensagem de erro.

        Raises:
            TypeError: Se a entrada tiver outro tipo.
        """
        mensagem = f"{campo} deve ser do tipo {classe.__name__}."
        Validacao.exigir(isinstance(valor, classe), mensagem, TypeError)

    @staticmethod
    def texto(valor, campo, permitir_vazio=False):
        """Valida um texto e remove espaços das extremidades.

        Args:
            valor (str): Texto recebido.
            campo (str): Nome usado na mensagem de erro.
            permitir_vazio (bool): Permite uma observação sem conteúdo.

        Returns:
            str: Texto normalizado.

        Raises:
            TypeError: Se a entrada não for texto.
            ValueError: Se um texto obrigatório estiver vazio.
        """
        Validacao.tipo(valor, str, campo)
        texto = valor.strip()
        Validacao.exigir(bool(texto) or permitir_vazio, f"{campo} está vazio.")
        return texto

    @staticmethod
    def codigo(valor):
        """Normaliza um identificador interno da aplicação.

        Args:
            valor (str): Código com letras ASCII, números, hífen ou sublinhado.

        Returns:
            str: Código em maiúsculas.

        Raises:
            TypeError: Se a entrada não for texto.
            ValueError: Se o código estiver vazio ou contiver outro caractere.
        """
        codigo = Validacao.texto(valor, "Código").upper()
        try:
            return fullmatch(r"[A-Z0-9_-]+", codigo).group()
        except AttributeError:
            raise ValueError("Código deve conter letras, números, hífen ou sublinhado.") from None

    @staticmethod
    def placa(valor):
        """Normaliza a identificação do veículo para evitar cadastros duplicados.

        Args:
            valor (str): Identificação alfanumérica, com espaços ou hífens opcionais.

        Returns:
            str: Identificação em maiúsculas, sem espaços e hífens.

        Raises:
            TypeError: Se a entrada não for texto.
            ValueError: Se não houver caracteres alfanuméricos válidos.

        Note:
            A verificação não comprova existência ou regularidade da placa.
        """
        placa = Validacao.texto(valor, "Placa").upper().replace("-", "").replace(" ", "")
        try:
            return fullmatch(r"[A-Z0-9]+", placa).group()
        except AttributeError:
            raise ValueError("Placa deve conter letras e números.") from None
