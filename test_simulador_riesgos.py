import pytest
from simulador_riegos import Riesgo


def test_impacto_Riesgo():
    riesgo = Riesgo("test", 2, 3)
    assert riesgo.nivel_prioridad == "Baja"