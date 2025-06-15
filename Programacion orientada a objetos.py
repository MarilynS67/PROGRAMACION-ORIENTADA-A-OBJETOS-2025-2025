# Programa con Programación Orientada a Objetos para calcular el promedio semanal del clima

class ClimaDiario:
    """Clase que representa la temperatura diaria."""
    def __init__(self):
        self.temperaturas = []

    def ingresar_temperaturas(self):
        """Método para ingresar temperaturas diarias."""
        for dia in range(1, 8):  # 7 días
            temp = float(input(f"Ingrese la temperatura del día {dia}: "))
            self.temperaturas.append(temp)

    def calcular_promedio(self):
        """Método que calcula el promedio semanal."""
        if not self.temperaturas:
            return 0
        return sum(self.temperaturas) / len(self.temperaturas)

class ClimaConDetalles(ClimaDiario):
    """Clase que hereda de ClimaDiario y muestra detalles adicionales."""

    def mostrar_resultado(self):
        """Método para mostrar el promedio calculado."""
        promedio = self.calcular_promedio()
        print(f"El promedio semanal de temperatura es: {promedio:.2f}°C")

def main():
    """Función principal del programa POO."""
    print("=== Programa Orientado a Objetos ===")
    clima = ClimaConDetalles()
    clima.ingresar_temperaturas()
    clima.mostrar_resultado()

# Ejecutar el programa
if __name__ == "__main__":
    main()
