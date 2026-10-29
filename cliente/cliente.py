"""Cliente identificado por código e seus veículos cadastrados."""
from functools import partial
from estrutura_de_dados import ListaEncadeada
from oficina.validacao import Validacao

class Cliente:
    """Mantém a identificação do cliente e referências aos seus veículos."""

    def __init__(self, codigo, nome):
        """Cria um cliente sem veículos vinculados.

        Args:
            codigo (str): Identificador único do cliente.
            nome (str): Nome informado no cadastro.

        Raises:
            TypeError: Se os argumentos não forem textos.
            ValueError: Se os dados estiverem vazios ou inválidos.
        """
        self._codigo = Validacao.codigo(codigo)
        self.nome = nome
        self._veiculos = ListaEncadeada()

    @property
    def codigo(self):
        """str: Identificador estável do cliente."""
        return self._codigo

    @property
    def nome(self):
        """str: Nome atual do cadastro."""
        return self._nome

    @nome.setter
    def nome(self, valor):
        """Valida o nome antes de substituir o anterior.

        Args:
            valor (str): Novo nome.

        Raises:
            TypeError: Se o nome não for texto.
            ValueError: Se o nome estiver vazio.
        """
        self._nome = Validacao.texto(valor, "Nome do cliente")

    def buscar_veiculo(self, placa):
        """Encontra um veículo entre os cadastros deste cliente.

        Args:
            placa (str): Identificação procurada.

        Returns:
            Veiculo: Mesmo objeto mantido pela oficina.

        Raises:
            TypeError: Se a placa não for texto.
            ValueError: Se a placa for inválida ou não existir.
        """
        placa = Validacao.placa(placa)
        try:
            return self._veiculos.buscar(partial(self._mesma_placa, placa))
        except ValueError:
            raise ValueError("Veículo não vinculado a este cliente.") from None

    @staticmethod
    def _mesma_placa(placa, veiculo):
        """Compara a placa com o cadastro examinado.

        Args:
            placa (str): Identificação normalizada.
            veiculo (Veiculo): Cadastro examinado.

        Returns:
            bool: Indica correspondência.
        """
        return veiculo.placa == placa

    def adicionar_veiculo(self, veiculo):
        """Vincula o veículo sem copiar seu cadastro.

        Args:
            veiculo (Veiculo): Cadastro cujo proprietário é este cliente.

        Raises:
            TypeError: Se o argumento não for veículo.
            ValueError: Se o proprietário não corresponder ou a placa se repetir.
        """
        from oficina.veiculo import Veiculo
        Validacao.tipo(veiculo, Veiculo, "Veículo")
        Validacao.exigir(veiculo.cliente is self, "O veículo pertence a outro cliente.")
        self._validar_placa_livre(veiculo.placa)
        self._veiculos.adicionar_final(veiculo)

    def _validar_placa_livre(self, placa):
        """Recusa um vínculo repetido.

        Args:
            placa (str): Placa normalizada.

        Raises:
            ValueError: Se a placa já estiver vinculada.
        """
        try:
            self.buscar_veiculo(placa)
        except ValueError:
            return
        raise ValueError("Veículo já vinculado ao cliente.")

    def listar_veiculos(self):
        """Disponibiliza os veículos do cliente sem expor a lista interna.

        Returns:
            Iterator: Veículos na ordem de cadastro.
        """
        return iter(self._veiculos)

