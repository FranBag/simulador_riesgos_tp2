import random
import os
from dataclasses import dataclass
from typing import List, Dict, Tuple

def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

@dataclass
class Riesgo:
    """Clase que representa un riesgo en un proyecto Scrum.
    Contiene el nombre, probabilidad de ocurrencia e impacto del riesgo.
    """
    nombre: str
    probabilidad: int  # Valor entre 1-5 (1=muy baja, 5=muy alta)
    impacto: int       # Valor entre 1-5 (1=muy bajo, 5=muy alto)
    
    @property
    def prioridad(self) -> int:
        """Calcula la prioridad del riesgo como producto de probabilidad e impacto.
        Retorna un valor entre 1-25.
        """
        return self.probabilidad * self.impacto
    
    @property
    def nivel_prioridad(self) -> str:
        """Clasifica el riesgo en niveles de prioridad según su valor calculado:
        - Baja (1-6)
        - Media (7-14)
        - Alta (15-25)
        """
        if 1 <= self.prioridad <= 6:
            return "Baja"
        elif 7 <= self.prioridad <= 14:
            return "Media"
        elif 15 <= self.prioridad <= 25:
            return "Alta"
        else:
            return "Desconocida"

class MitigacionStrategy:
    """Clase que implementa el patrón Strategy para generar estrategias de mitigación
    personalizadas según el tipo de riesgo y su nivel de prioridad.
    """
    
    @staticmethod
    def generar_mitigacion(riesgo: Riesgo) -> str:
        """Genera una estrategia de mitigación basada en el tipo de riesgo y prioridad
        """
        # Diccionario con estrategias base para cada tipo de riesgo
        estrategias = {
            "Estimaciones de tiempo poco realistas": 
                "Utilizar técnicas de estimación como Planning Poker e implementar revisiones periódicas de estimaciones.",
            "Falta de habilidades técnicas en el equipo": 
                "Implementar un programa de mentorías y capacitaciones técnicas. Considerar contratación de especialistas.",
            "Deuda técnica acumulada": 
                "Asignar tiempo en cada sprint para reducir deuda técnica. Priorizar refactorización de código crítico.",
            "Mala implementación del backlog": 
                "Realizar sesiones de refinamiento del backlog con todo el equipo. Definir criterios de aceptación claros.",
            "La documentación no refleja el codigo o no existe": 
                "Establecer un estándar de documentación. Implementar revisiones periódicas y documentación automatizada.",
            "Falta de implementación de pruebas o testing": 
                "Implementar pruebas automatizadas. Establecer requisitos mínimos de cobertura para merges.",
            "Dificultad en la integración con otros sistemas": 
                "Planificar integraciones desde el inicio. Usar APIs bien documentadas y pruebas de integración continuas.",
            "Reuniones de Scrum ineficientes": 
                "Definir agendas claras y límites de tiempo. Usar herramientas visuales para seguimiento.",
            "Reducción de productividad por Micromanagement": 
                "Fomentar autonomía del equipo. Establecer objetivos claros en lugar de supervisión constante.",
            "El cliente no se compromete con la creación de Historias de Usuario": 
                "Involucrar al cliente en reuniones clave. Realizar workshops para co-creación de historias."
        }
        
        # Obtiene estrategia base o una por defecto si no existe
        estrategia_base = estrategias.get(riesgo.nombre, "Revisar procesos y realizar un análisis de causa raíz.")
        
        # Ajusta estrategia según el nivel de prioridad
        if riesgo.nivel_prioridad == "Alta":
            return f"ACCION INMEDIATA REQUERIDA: {estrategia_base} Asignar recursos adicionales y monitorear diariamente."
        elif riesgo.nivel_prioridad == "Media":
            return f"Acciones planificadas: {estrategia_base} Revisar progreso semanalmente."
        else:
            return f"Acciones preventivas: {estrategia_base} Monitorear periódicamente."

class GestorRiesgos:
    """Clase principal que gestiona la simulación de riesgos y sus operaciones."""
        
    def __init__(self, riesgos: List[Riesgo]):
        """Inicializa el gestor con una lista de riesgos posibles."""
        self.riesgos = riesgos
        self.mitigacion_strategy = MitigacionStrategy()
    
    def seleccionar_riesgo_aleatorio(self) -> Riesgo:
        """Selecciona un riesgo aleatorio usando su probabilidad."""
        pesos = [riesgo.probabilidad for riesgo in self.riesgos]
        return random.choices(self.riesgos, weights=pesos, k=1)[0]
    
    def simular_sprint(self, num_sprints: int = 1) -> List[Dict]:
        """Simula uno o múltiples sprints y genera los riesgos asociados."""
        resultados = []
        for _ in range(num_sprints):
            riesgo = self.seleccionar_riesgo_aleatorio()
            mitigacion = self.mitigacion_strategy.generar_mitigacion(riesgo)
            resultados.append({
                "riesgo": riesgo.nombre,
                "probabilidad": riesgo.probabilidad,
                "impacto": riesgo.impacto,
                "prioridad": riesgo.prioridad,
                "nivel_prioridad": riesgo.nivel_prioridad,
                "mitigacion": mitigacion
            })
        return resultados
    
    def obtener_riesgo_mas_prioritario(self) -> Riesgo:
        """Obtiene el riesgo con mayor prioridad de la lista."""
        return max(self.riesgos, key=lambda r: r.prioridad)
    
    def obtener_todos_riesgos_ordenados(self) -> List[Riesgo]:
        """Devuelve todos los riesgos ordenados por prioridad."""
        return sorted(self.riesgos, key=lambda r: r.prioridad, reverse=True)
    
    def obtener_riesgos_por_nivel(self, nivel: str) -> List[Riesgo]:
        """Muestra riesgos por nivel de prioridad."""
        return [r for r in self.riesgos if r.nivel_prioridad == nivel]

class ReporteRiesgos:
    """Clase que genera reportes de riesgos."""
    
    @staticmethod
    def generar_reporte(resultados: List[Dict]) -> str:
        """Genera un reporte de los resultados de la simulación."""
        reporte = "=== Reporte de Riesgos en Sprint ===\n\n"
        for i, resultado in enumerate(resultados, 1):
            reporte += (
                f"Riesgo {i}:\n"
                f"  - Nombre: {resultado['riesgo']}\n"
                f"  - Probabilidad: {resultado['probabilidad']}/5\n"
                f"  - Impacto: {resultado['impacto']}/5\n"
                f"  - Prioridad: {resultado['prioridad']} ({resultado['nivel_prioridad']})\n"
                f"  - Mitigación sugerida: {resultado['mitigacion']}\n\n"
            )
        return reporte
    
    @staticmethod
    def generar_reporte_prioritario(riesgo: Riesgo, mitigacion: str) -> str:
        """Genera un reporte para el riesgo con mayor prioridad."""
        return (
            "=== Riesgo más prioritario ===\n"
            f"Nombre: {riesgo.nombre}\n"
            f"Prioridad: {riesgo.prioridad} ({riesgo.nivel_prioridad}) "
            f"(Probabilidad: {riesgo.probabilidad}, Impacto: {riesgo.impacto})\n"
            f"Mitigación sugerida: {mitigacion}\n"
        )
    
    @staticmethod
    def generar_reporte_por_nivel(riesgos: List[Tuple[Riesgo, str]], nivel: str) -> str:
        """Filtra y genera un reporte de riesgos por nivel de prioridad"""
        reporte = f"=== Riesgos con Prioridad {nivel} ===\n\n"
        for i, (riesgo, mitigacion) in enumerate(riesgos, 1):
            reporte += (
                f"{i}. {riesgo.nombre}\n"
                f"   - Prioridad: {riesgo.prioridad}\n"
                f"   - Probabilidad: {riesgo.probabilidad}/5\n"
                f"   - Impacto: {riesgo.impacto}/5\n"
                f"   - Mitigación: {mitigacion}\n\n"
            )
        return reporte

def cargar_riesgos() -> List[Riesgo]:
    """Carga la lista de riesgos predefinida."""
    return [
        Riesgo("Estimaciones de tiempo poco realistas", 3, 2),
        Riesgo("Falta de habilidades técnicas en el equipo", 2, 3),
        Riesgo("Deuda técnica acumulada", 2, 4),
        Riesgo("Mala implementación del backlog", 3, 5),
        Riesgo("La documentación no refleja el codigo o no existe", 5, 2),
        Riesgo("Falta de implementación de pruebas o testing", 3, 5),
        Riesgo("Dificultad en la integración con otros sistemas", 2, 3),
        Riesgo("Reuniones de Scrum ineficientes", 3, 2),
        Riesgo("Reducción de productividad por Micromanagement", 4, 5),
        Riesgo("El cliente no se compromete con la creación de Historias de Usuario", 3, 5)
    ]

def main():
    """Función principal que maneja el flujo del programa y la interfaz de usuario."""
    riesgos = cargar_riesgos()
    gestor = GestorRiesgos(riesgos)
    reporte = ReporteRiesgos()
    
    
    
    while True:
        # Menú de opciones
        limpiar_pantalla()
        print("=== Simulador de Riesgos en Sprints Scrum ===")
        
        print("\nOpciones:")
        print("1. Simular un sprint")
        print("2. Simular múltiples sprints")
        print("3. Mostrar riesgo más prioritario")
        print("4. Mostrar todos los riesgos ordenados por prioridad")
        print("5. Mostrar riesgos por nivel de prioridad")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        # Lógica de manejo de opciones
        if opcion == "1":
            limpiar_pantalla()
            resultados = gestor.simular_sprint()
            print("\n" + reporte.generar_reporte(resultados))
            input("\nPresione Enter para continuar...")
            
        elif opcion == "2":
            limpiar_pantalla()
            try:
                num_sprints = int(input("Ingrese el número de sprints a simular: "))
                resultados = gestor.simular_sprint(num_sprints)
                limpiar_pantalla()
                print("\n" + reporte.generar_reporte(resultados))
                input("\nPresione Enter para continuar...")
            except ValueError:
                print("Por favor ingrese un número válido.")
                input("\nPresione Enter para continuar...")
        elif opcion == "3":
            limpiar_pantalla()
            riesgo = gestor.obtener_riesgo_mas_prioritario()
            mitigacion = MitigacionStrategy.generar_mitigacion(riesgo)
            print("\n" + reporte.generar_reporte_prioritario(riesgo, mitigacion))
            input("\nPresione Enter para continuar...")
        elif opcion == "4":
            limpiar_pantalla()
            print("\n=== Todos los riesgos ordenados por prioridad ===")
            for i, riesgo in enumerate(gestor.obtener_todos_riesgos_ordenados(), 1):
                mitigacion = MitigacionStrategy.generar_mitigacion(riesgo)
                print(f"{i}. {riesgo.nombre} - Prioridad: {riesgo.prioridad} ({riesgo.nivel_prioridad})")
                print(f"   Mitigación: {mitigacion}\n")
            input("\nPresione Enter para continuar...")
        elif opcion == "5":
            limpiar_pantalla()
            print("\nSeleccione nivel de prioridad:")
            print("1. Baja (1-6)")
            print("2. Media (7-14)")
            print("3. Alta (15-25)")
            sub_opcion = input("Opción: ")
            
            if sub_opcion == "1":
                riesgos_nivel = gestor.obtener_riesgos_por_nivel("Baja")
                riesgos_con_mitigacion = [(r, MitigacionStrategy.generar_mitigacion(r)) for r in riesgos_nivel]
                print("\n" + reporte.generar_reporte_por_nivel(riesgos_con_mitigacion, "Baja"))
                input("\nPresione Enter para continuar...")
            elif sub_opcion == "2":
                riesgos_nivel = gestor.obtener_riesgos_por_nivel("Media")
                riesgos_con_mitigacion = [(r, MitigacionStrategy.generar_mitigacion(r)) for r in riesgos_nivel]
                print("\n" + reporte.generar_reporte_por_nivel(riesgos_con_mitigacion, "Media"))
                input("\nPresione Enter para continuar...")
            elif sub_opcion == "3":
                riesgos_nivel = gestor.obtener_riesgos_por_nivel("Alta")
                riesgos_con_mitigacion = [(r, MitigacionStrategy.generar_mitigacion(r)) for r in riesgos_nivel]
                print("\n" + reporte.generar_reporte_por_nivel(riesgos_con_mitigacion, "Alta"))
                input("\nPresione Enter para continuar...")
            else:
                print("Opción no válida.")
                input("\nPresione Enter para continuar...")
                
        elif opcion == "6":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor seleccione una opción del 1 al 6.")
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()