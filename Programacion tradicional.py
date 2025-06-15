# Programa Tradicional para calcular el promedio semanal del clima

def ingresar_temperaturas():
    """Función para ingresar las temperaturas diarias."""
    temperaturas = []
    for dia in range(1, 8):  # 7 días de la semana
        temp = float(input(f"Ingrese la temperatura del día {dia}: "))
        temperaturas.append(temp)
    return temperaturas

def calcular_promedio(temperaturas):
    """Calcula el promedio de la lista de temperaturas."""
    total = sum(temperaturas)
    promedio = total / len(temperaturas)
    return promedio

def main():
    """Función principal del programa tradicional."""
    print("=== Programa Tradicional ===")
    temperaturas = ingresar_temperaturas()
    promedio = calcular_promedio(temperaturas)
    print(f"El promedio semanal de temperatura es: {promedio:.2f}°C")

# Ejecutar el programa
if __name__ == "__main__":
    main()
