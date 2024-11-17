# Open Split - Divisor de Gastos

Esta aplicación te ayuda a dividir gastos entre un grupo de personas de manera flexible y equitativa. Puedes especificar diferentes formas de dividir cada gasto, desde división equitativa hasta montos específicos por persona.

## Instrucciones

1. **Preparar la Hoja de Cálculo**:
   - Crea una hoja de cálculo en Google Sheets con las siguientes columnas:
     - `item`: Descripción del gasto (ej: "Supermercado", "Gasolina")
     - name: Nombre de quien realizó el pago
     - amount: Monto total del gasto
     - `participants`: Quiénes participan en el gasto y cómo se divide (opcional)

2. **Compartir la Hoja de Cálculo**:
   - Asegúrate de que la hoja de cálculo sea visible públicamente para que la aplicación pueda acceder a ella.

3. **Usar la Aplicación**:
   - Introduce la URL de tu hoja de cálculo en el campo proporcionado en la aplicación.
   - Haz clic en el botón "Calcular" para procesar los datos y obtener los resultados.

## Ejemplos de División de Gastos

### 1. División Equitativa entre Todos
Deja la columna 'participants' vacía para dividir el gasto equitativamente entre todos los participantes.

### 2. División Equitativa entre Algunos
Lista los nombres de los participantes separados por comas:

| item     | name | amount | participants      |
|----------|------|--------|-------------------|
| Gasolina | Luis | 720    | Luis,Ana,María    |


### 3. División con Montos Específicos
Usa el símbolo `=` para asignar montos específicos:

| item    | name | amount | participants           |
|---------|------|--------|------------------------|
| Almuerzo| Ana  | 1500   | Ana=500,Luis=500,María=500 |


### 4. División Mixta
Combina montos específicos con división equitativa del resto:

| item  | name | amount | participants           |
|-------|------|--------|------------------------|
| Super | Ana  | 950    | Ana=400,Luis=400,María |

En este ejemplo, María pagará los $150 restantes.

## Consejos y Advertencias

- Para una división equitativa entre varios participantes, simplemente lista sus nombres separados por comas sin usar el símbolo `=`.
- La suma de los montos específicos no puede exceder el monto total del gasto.
- Si algunos participantes tienen montos específicos y otros no, el monto restante se dividirá equitativamente entre los participantes sin monto específico.
- Todos los nombres en la columna 'participants' deben corresponder exactamente a los nombres de los participantes del grupo.

## Ejemplos de Casos Comunes

### Caso 1: Alguien paga más por una razón específica

| item | name | amount | participants |
|------|------|--------|--------------|
| Cena | Pedro | 1200 | Pedro=500,Ana,Luis,María |

Pedro pagará $500, y el resto ($700) se divide entre Ana, Luis y María ($350 cada una).

### Caso 2: Gasto compartido entre parejas

| item | name | amount | participants |
|------|------|--------|--------------|
| Hospedaje | Ana | 2000 | Ana=1000,Luis=1000 |

Revisa siempre el resumen generado por la aplicación para verificar que los gastos se hayan dividido como esperas.
