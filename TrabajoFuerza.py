class OptimizadorFuerzaTrabajo:
    """
    Clase para optimizar el tamaño de la fuerza de trabajo utilizando programación dinámica.
    """

    def __init__(self, semanas, trabajadores_minimos, costo_exceso, costo_contratacion):
        """
        Inicializa la clase con los parámetros del problema.

        semanas: Número total de semanas a optimizar
        trabajadores_minimos: Lista con el número mínimo de trabajadores requeridos por semana
        costo_exceso: Costo por trabajador excedente por semana
        costo_contratacion: Tupla con (costo fijo de contratación, costo por trabajador contratado)
        """
        self.semanas = semanas
        self.trabajadores_minimos = trabajadores_minimos
        self.costo_exceso = costo_exceso
        self.costo_contratacion = costo_contratacion
        self.memo = {}  # Diccionario para memoización

    def optimizar(self):
        """
        Realiza la optimización de la fuerza de trabajo y escribe los resultados en un archivo.

        :return: Tupla con (costo total de la optimización, lista de decisiones óptimas)
        """
        costo_total = 0
        decisiones = []
        trabajadores_previos = 0

        # Abre el archivo para escribir los resultados
        with open("ResultadosTarea.txt", "w", encoding="utf-8") as archivo:
            archivo.write("Resultados de la optimización del tamaño de la fuerza de trabajo:\n\n")

            # Itera sobre cada semana
            for i in range(self.semanas):
                # Obtiene la decisión óptima para la semana actual
                costo, trabajadores = self._funcion_optimizacion(i, trabajadores_previos)
                # Calcula el costo real de la decisión
                costo_actual = self._calcular_costo(i, trabajadores_previos, trabajadores)
                costo_total += costo_actual
                decisiones.append(trabajadores)

                # Escribe los resultados de la semana actual
                self._escribir_resultados(archivo, i, trabajadores, trabajadores_previos, costo_actual)
                trabajadores_previos = trabajadores

            # Escribe el costo total de la optimización
            archivo.write(f"Costo total de la optimización: ${costo_total:.2f}\n")

        return costo_total, decisiones

    def _funcion_optimizacion(self, semana, trabajadores_previos):
        """
        Función recursiva para encontrar la decisión óptima para cada semana.

        semana: Semana actual
        trabajadores_previos: Número de trabajadores de la semana anterior
        return: Tupla con (costo mínimo, mejor decisión)
        """
        # Caso base: última semana
        if semana == self.semanas - 1:
            return self._calcular_costo(semana, trabajadores_previos, self.trabajadores_minimos[semana]), self.trabajadores_minimos[semana]

        # Verifica si ya se ha calculado este estado (memoización)
        if (semana, trabajadores_previos) in self.memo:
            return self.memo[(semana, trabajadores_previos)]

        costo_minimo = float('inf')
        mejor_decision = 0

        # Prueba todas las opciones posibles de fuerza de trabajo
        for trabajadores in range(self.trabajadores_minimos[semana], max(self.trabajadores_minimos) + 1):
            costo_actual = self._calcular_costo(semana, trabajadores_previos, trabajadores)
            costo_futuro, _ = self._funcion_optimizacion(semana + 1, trabajadores)
            costo_total = costo_actual + costo_futuro

            # Actualiza la mejor decisión si se encuentra un costo menor
            if costo_total < costo_minimo:
                costo_minimo = costo_total
                mejor_decision = trabajadores

        # Guarda el resultado en la memoria (memoización)
        self.memo[(semana, trabajadores_previos)] = (costo_minimo, mejor_decision)
        return costo_minimo, mejor_decision

    def _calcular_costo(self, semana, trabajadores_previos, trabajadores_actuales):
        """
        Calcula el costo de una decisión específica.

        semana: Semana actual
        trabajadores_previos: Número de trabajadores de la semana anterior
        trabajadores_actuales: Número de trabajadores para la semana actual
        :return: Costo total de la decisión
        """
        costo = 0
        # Calcula el costo por exceso de trabajadores
        if trabajadores_actuales > self.trabajadores_minimos[semana]:
            costo += (trabajadores_actuales - self.trabajadores_minimos[semana]) * self.costo_exceso
        # Calcula el costo por contratación
        if trabajadores_actuales > trabajadores_previos:
            costo += self.costo_contratacion[0] + (trabajadores_actuales - trabajadores_previos) * self.costo_contratacion[1]
        return costo

    def _escribir_resultados(self, archivo, semana, trabajadores, trabajadores_previos, costo):
        """
        Escribe los resultados de una semana en el archivo.

        archivo: Objeto de archivo abierto para escritura
        semana: Número de la semana actual
        trabajadores: Número de trabajadores decidido para la semana actual
        trabajadores_previos: Número de trabajadores de la semana anterior
        costo: Costo de la decisión para la semana actual
        """
        archivo.write(f"Semana {semana + 1}:\n")
        archivo.write(f"  Trabajadores mínimos requeridos: {self.trabajadores_minimos[semana]}\n")
        archivo.write(f"  Fuerza de trabajo óptima: {trabajadores}\n")
        archivo.write(f"  Costo de la decisión: ${costo:.2f}\n")

        # Determina la acción tomada (contratar, despedir o mantener)
        if trabajadores > trabajadores_previos:
            archivo.write(f"  Acción: Contratar {trabajadores - trabajadores_previos} trabajadores\n")
        elif trabajadores < trabajadores_previos:
            archivo.write(f"  Acción: Despedir {trabajadores_previos - trabajadores} trabajadores\n")
        else:
            archivo.write("  Acción: Mantener la fuerza de trabajo actual\n")

        archivo.write("\n")

# Uso de la clase
if __name__ == "__main__":
    # Definición de los parámetros del problema
    semanas = 5
    trabajadores_minimos = [5, 7, 8, 4, 6]
    costo_exceso = 300
    costo_contratacion = (400, 200)  # (costo fijo, costo por trabajador)

    # Creación de la instancia del optimizador
    optimizador = OptimizadorFuerzaTrabajo(semanas, trabajadores_minimos, costo_exceso, costo_contratacion)
    
    # Ejecución de la optimización
    costo_total, fuerza_trabajo_optima = optimizador.optimizar()

    # Impresión de los resultados
    print(f"Costo total de la optimización: ${costo_total:.2f}")
    print(f"Fuerza de trabajo óptima por semana: {fuerza_trabajo_optima}")