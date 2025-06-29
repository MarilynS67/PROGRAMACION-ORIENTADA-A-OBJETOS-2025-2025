# Programa para calcular el área de un rectángulo
# Funcionalidad: solicita al usuario la base y la altura, calcula el área e indica si es mayor a 100.

# Función principal que calcula el área de un rectángulo
def calcular_area_rectangulo(base: float, altura: float) -> float:
    return base * altura

# Variables (identificadores descriptivos)
base_rectangulo = float(input("Ingrese la base del rectángulo (cm): "))
altura_rectangulo = float(input("Ingrese la altura del rectángulo (cm): "))

# Cálculo del área usando tipos float
area_total = calcular_area_rectangulo(base_rectangulo, altura_rectangulo)

# Verificación con tipo boolean
es_grande = area_total > 100

# Resultados (tipos string, float y boolean)
print("El área del rectángulo es:", area_total, "cm²")
print("¿El área es mayor a 100 cm²?", es_grande)
