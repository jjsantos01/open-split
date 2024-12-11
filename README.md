# Open Split - Divisor de Gastos

Esta aplicación te ayuda a dividir gastos entre un grupo de personas de manera flexible y equitativa. Puedes especificar diferentes formas de dividir cada gasto, desde división equitativa hasta montos específicos por persona.

Disponible en: [https://jjsantos01.github.io//open-split/](https://jjsantos01.github.io//open-split/)

## Instrucciones

1. **Preparar la Hoja de Cálculo**:
   - Crea una hoja de cálculo en Google Sheets con las siguientes columnas:
     - `item`: Descripción del gasto (ej: "Supermercado", "Gasolina")
     - `name`: Nombre de quien realizó el pago
     - `amount`: Monto total del gasto
     - `participants`: Quiénes participan en el gasto y cómo se divide (opcional)

2. **Compartir la Hoja de Cálculo**:
   - Asegúrate de que la hoja de cálculo sea visible públicamente para que la aplicación pueda acceder a ella.

3. **Usar la Aplicación**:
   - Introduce la URL de tu hoja de cálculo en el campo proporcionado en la aplicación.
   - Haz clic en el botón "Calcular" para procesar los datos y obtener los resultados.
   - Puedes usar el campo de "participantes adicionales" para incluir a aquellos participantes que no hicieron un gasto o cuyo nombre no aparece en la hoja de cálculo. Estos participantes solo serán considerados en todos los gastos donde participan todos. Los nombres de los participantes deben ponerse separados por comas.

## Ejemplos de División de Gastos

### 1. División Equitativa entre Todos
Si dejas la columna 'participants' vacía, el gasto se dividirá equitativamente entre todos los participantes registrados (incluyendo los participantes adicionales que hayas agregado).

### 2. División Equitativa entre Algunos
Lista los nombres de los participantes separados por comas:

| item     | name | amount | participants |
|----------|------|--------|--------------|
| Gasolina | Luis | 720    | Luis,Ana     |

En este caso, el gasto se dividirá equitativamente solo entre Luis y Ana. Los demás participantes no participarán en este gasto.

### 3. División con Montos Específicos
Usa el símbolo `=` para asignar montos específicos:

| item     | name | amount | participants              |
|----------|------|--------|---------------------------|
| Almuerzo | Ana  | 1500   | Ana=1000,Luis=200,María=300 |

En este caso, Ana pagará $1000, Luis $200 y María $300.

### 4. División Mixta
Combina montos específicos con división equitativa del resto:

| item  | name | amount | participants      |
|-------|------|--------|-------------------|
| Super | Ana  | 950    | Ana=250,Luis,María |

En este ejemplo, Ana pagará $250 y el resto ($700) se dividirá equitativamente entre Luis y María, es decir, $350 cada uno.

## Consejos y Advertencias

- Para una división equitativa entre varios participantes, simplemente lista sus nombres separados por comas sin usar el símbolo `=`.
- La suma de los montos específicos no puede exceder el monto total del gasto.
- Si algunos participantes tienen montos específicos y otros no, el monto restante se dividirá equitativamente entre los participantes sin monto específico.
- Todos los nombres en la columna 'participants' deben corresponder exactamente a los nombres de los participantes del grupo.
- Los participantes adicionales que agregues solo serán considerados en los gastos donde participan todos (cuando la columna 'participants' está vacía).## Ejemplos de Casos Comunes

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

## Sitio renderizado
![Open Split](/images/Open-split.png)
