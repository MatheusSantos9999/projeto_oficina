"""Cadastro do veículo e de sua composição física."""
from itertools import count

from estrutura_de_dados import NoArvore, Pilha
from oficina.componentes import Componente
from oficina.validacao import Validacao


class Veiculo:
    """Mantém a identificação do veículo e sua árvore de componentes.

    Attributes:
        placa (str): Identificação normalizada e somente leitura.
        modelo (str): Descrição editável do modelo.
        cliente (str): Nome do cliente, sem implementar seu cadastro completo.
    """

    def __init__(self, placa, modelo, cliente=""):
        """Cria um veículo com uma árvore contendo somente a raiz.

        Args:
            placa (str): Identificação do veículo.
            modelo (str): Descrição não vazia do modelo.
            cliente (str): Nome opcional do cliente associado ao veículo.

        Raises:
            TypeError: Se os argumentos não forem textos.
            ValueError: Se a placa for inválida ou o modelo estiver vazio.
        """
        self._placa = Validacao.placa(placa)
        self.modelo = modelo
        self.cliente = cliente
        self._componentes = NoArvore(Componente("VEICULO", "Veículo"))

    @property
    def placa(self):
        """str: Identificação estável usada para localizar o cadastro."""
        return self._placa

    @property
    def modelo(self):
        """str: Descrição do modelo."""
        return self._modelo

    @modelo.setter
    def modelo(self, valor):
        """Atualiza o modelo após validar o novo texto.

        Args:
            valor (str): Nova descrição.

        Raises:
            TypeError: Se o valor não for texto.
            ValueError: Se a descrição estiver vazia.
        """
        self._modelo = Validacao.texto(valor, "Modelo")

    def adicionar_componente(self, codigo_pai, componente):
        """Acrescenta uma peça ou conjunto à composição deste veículo.

        Args:
            codigo_pai (str): Identificador do conjunto existente.
            componente (Componente): Descrição do novo componente.

        Raises:
            TypeError: Se os argumentos tiverem tipos incorretos.
            ValueError: Se o pai não existir ou o código estiver repetido.
        """
        Validacao.tipo(componente, Componente, "Componente")
        pai = Componente.buscar_no(self._componentes, codigo_pai)
        self._validar_codigo_livre(componente.codigo)
        pai.adicionar_filho(NoArvore(componente.copiar()))

    def _validar_codigo_livre(self, codigo):
        """Impede a inclusão de códigos repetidos na composição do veículo.

        Args:
            codigo (str): Identificador já validado pelo componente.

        Raises:
            ValueError: Se o código já estiver na árvore.
        """
        try:
            Componente.buscar_no(self._componentes, codigo)
        except ValueError:
            return
        raise ValueError(f"Componente já cadastrado: {codigo}.")

    def buscar_componente(self, codigo):
        """Consulta um componente pela identificação.

        Args:
            codigo (str): Código procurado.

        Returns:
            Componente: Cópia da descrição cadastrada.

        Raises:
            TypeError: Se o código não for texto.
            ValueError: Se o código for inválido ou desconhecido.
        """
        return Componente.buscar_no(self._componentes, codigo).dado.copiar()

    def percorrer_componentes(self):
        """Disponibiliza a composição do veículo em pré-ordem.

        Yields:
            tuple: Cópia do componente e profundidade na árvore.
        """
        for no, nivel in self._componentes.pre_ordem():
            yield no.dado.copiar(), nivel

    def copiar_componentes(self):
        """Obtém uma árvore independente para iniciar um diagnóstico.

        Returns:
            NoArvore: Raiz de uma cópia independente da composição atual.

        Note:
            Usa a Pilha própria para copiar sem recursão. A validação de pais
            em NoArvore.adicionar_filho pode levar o custo total a O(n²).
        """
        raiz = NoArvore(self._componentes.dado.copiar())
        pendentes = Pilha()
        pendentes.empilhar((self._componentes, raiz))
        for _ in count():
            try:
                original, copia = pendentes.desempilhar()
            except IndexError:
                return raiz
            self._copiar_filhos(original, copia, pendentes)

    @staticmethod
    def _copiar_filhos(original, copia, pendentes):
        """Copia os filhos diretos e agenda a cópia dos próximos níveis.

        Args:
            original (NoArvore): Nó cujos filhos serão lidos.
            copia (NoArvore): Nó que receberá os novos filhos.
            pendentes (Pilha): Pares de nós ainda aguardando cópia.
        """
        for filho in original.filhos:
            novo = NoArvore(filho.dado.copiar())
            copia.adicionar_filho(novo)
            pendentes.empilhar((filho, novo))

    @property
    def cliente(self):
        """str: Nome informado do cliente associado ao veículo."""
        return self._cliente

    @cliente.setter
    def cliente(self, valor):
        """Valida o nome do cliente antes de atualizá-lo.

        Args:
            valor (str): Nome ou texto vazio quando ainda não informado.

        Raises:
            TypeError: Se o valor não for texto.
        """
        self._cliente = Validacao.texto(valor, "Cliente", True)
