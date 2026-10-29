"""Cadastro de veículos, composição de componentes e diagnósticos por visita."""
from oficina.avaliacao import Avaliacao
from oficina.componentes import Componente, EstadoComponente
from oficina.diagnostico import Diagnostico
from oficina.oficina import Oficina
from oficina.veiculo import Veiculo

__all__ = (
    "Avaliacao", "Componente", "EstadoComponente",
    "Diagnostico", "Oficina", "Veiculo",
)
