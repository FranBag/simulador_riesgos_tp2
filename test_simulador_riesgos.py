import pytest
from simulador_riesgos import Riesgo, MitigacionStrategy, GestorRiesgos, cargar_riesgos

def test_prioridad_calculo_correcto():
    riesgo = Riesgo("Test", probabilidad=4, impacto=5)
    assert riesgo.prioridad == 20

def test_nivel_prioridad_alta():
    riesgo = Riesgo("Test", 5, 5)  # Debería tener prioridad 25(Alta)
    assert riesgo.nivel_prioridad == "Alta"

def test_nivel_prioridad_media():
    riesgo = Riesgo("Test", 2, 4)  # Debería tener prioridad 8(Media)
    assert riesgo.nivel_prioridad == "Media"

def test_nivel_prioridad_baja():
    riesgo = Riesgo("Test", 1, 2)  # Debería tener prioridad 2(Baja)
    assert riesgo.nivel_prioridad == "Baja"

def test_generar_mitigacion_personalizada_y_urgente():
    riesgo = Riesgo("Falta de habilidades técnicas en el equipo", 5, 5)  # Prioridad alta
    resultado = MitigacionStrategy.generar_mitigacion(riesgo)
    assert resultado.startswith("ACCION INMEDIATA REQUERIDA:")

def test_generar_mitigacion_generica_para_riesgo_desconocido():
    riesgo = Riesgo("Otro riesgo", 5, 1)
    resultado = MitigacionStrategy.generar_mitigacion(riesgo)
    print(resultado)
    assert "Revisar procesos" in resultado

def test_simular_sprint_retorna_resultado_esperado():
    riesgos = cargar_riesgos()
    gestor = GestorRiesgos(riesgos)
    resultados = gestor.simular_sprint(1)
    assert len(resultados) == 1
    assert "riesgo" in resultados[0]
    assert "mitigacion" in resultados[0]

def test_obtener_riesgo_mas_prioritario_es_correcto():
    riesgos = [Riesgo("R1", 1, 1), Riesgo("R2", 5, 5), Riesgo("R3", 2, 2)] # R3 tiene la prioridad más alta
    gestor = GestorRiesgos(riesgos)
    max_riesgo = gestor.obtener_riesgo_mas_prioritario()
    assert max_riesgo.nombre == "R2"

def test_mitigacion_correcta_para_riesgo_especifico():
    riesgo = Riesgo("Deuda técnica acumulada", 3, 5)
    estrategia = MitigacionStrategy.generar_mitigacion(riesgo)
    assert "Asignar tiempo en cada sprint para reducir deuda técnica" in estrategia
    assert estrategia.startswith("ACCION INMEDIATA REQUERIDA:")

def test_simular_varios_sprints_devuelve_lista_de_resultados():
    riesgos = cargar_riesgos()
    gestor = GestorRiesgos(riesgos)
    resultados = gestor.simular_sprint(5) # Esta función debe devolver 5 riesgos con sus respectivas mitigaciones
    assert len(resultados) == 5
    for r in resultados:
        assert "riesgo" in r and "mitigacion" in r

def test_seleccion_riesgo_aleatoria_por_probabilidad():
    riesgos = [
        Riesgo("R1", 1, 1),
        Riesgo("R2", 10, 1), # R2 tiene mayor probabilidad de aparición que R1.
    ]
    gestor = GestorRiesgos(riesgos)
    seleccionados = [gestor.seleccionar_riesgo_aleatorio().nombre for _ in range(100)]
    porcentaje_r2 = seleccionados.count("R2") / 100
    assert porcentaje_r2 > 0.8 # R2 debería de aparecer mayor cantidad de veces


def test_obtener_riesgos_por_nivel_devuelve_correctos():
    riesgos = [
        Riesgo("R1", 1, 1),  # Baja
        Riesgo("R2", 2, 4),  # Media
        Riesgo("R3", 5, 5),  # Alta
    ]
    gestor = GestorRiesgos(riesgos)
    riesgos_media = gestor.obtener_riesgos_por_nivel("Media") # Debería de devolver 1 riesgo
    assert len(riesgos_media) == 1
    assert riesgos_media[0].nombre == "R2"
