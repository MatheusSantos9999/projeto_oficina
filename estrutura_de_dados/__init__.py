"""Estruturas de dados genéricas, sem nenhuma regra da oficina.

Classes:
    No: Elo de uma cadeia (dado + próximo).
    ListaEncadeada: Lista com referências para início e fim.
    Fila: FIFO, construída sobre ListaEncadeada.
    Pilha: LIFO, construída sobre ListaEncadeada.
    NoArvore: Nó de árvore n-ária, com filhos em ListaEncadeada.
"""
from estrutura_de_dados.no import No
from estrutura_de_dados.lista_encadeada import ListaEncadeada
from estrutura_de_dados.fila import Fila
from estrutura_de_dados.pilha import Pilha
from estrutura_de_dados.no_arvore import NoArvore

__all__ = ("No", "ListaEncadeada", "Fila", "Pilha", "NoArvore")
