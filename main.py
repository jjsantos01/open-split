from pyscript import fetch, display
from pyscript.web import page
import js
import csv
from urllib.parse import urlparse
from io import StringIO

async def read_google_sheet(url: str) -> list[dict]:
    """
    Lee una hoja de cálculo pública de Google Sheets y la convierte en una lista de diccionarios.

    Args:
        url (str): URL completa de la hoja de Google Sheets compartida públicamente

    Returns:
        list: Lista de diccionarios donde cada diccionario representa una fila
              con pares clave-valor de columna:valor

    Raises:
        ValueError: Si la URL no es válida o no está compartida públicamente
        RequestException: Si hay problemas al acceder a la hoja
    """
    try:
        # Verificar si es una URL válida
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("URL inválida")

        # Extraer el ID del documento de la URL
        if '/d/' in url:
            # URL formato: https://docs.google.com/spreadsheets/d/[ID]/edit
            doc_id = url.split('/d/')[1].split('/')[0]
        else:
            raise ValueError("No se pudo extraer el ID del documento de la URL")
        # Construir la URL de exportación CSV
        csv_url = f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv"
        # Realizar la solicitud HTTP
        response = await fetch(csv_url, method="GET").text()
        # Usar CSV reader con StringIO para procesar el contenido
        csv_file = StringIO(response)
        csv_reader = csv.reader(csv_file)

        # Obtener los encabezados (primera fila)
        headers = next(csv_reader)
        headers = [header.strip() for header in headers]  # Limpiar espacios en blanco

        # Convertir las filas restantes en diccionarios
        records = []
        for row in csv_reader:
            # Crear diccionario para la fila actual
            record = {}
            for i, value in enumerate(row):
                # Intentar convertir a número si es posible
                try:
                    # Intentar convertir a float
                    float_value = float(value)
                    # Si es un número entero, convertir a int
                    if float_value.is_integer():
                        record[headers[i]] = int(float_value)
                    else:
                        record[headers[i]] = float_value
                except ValueError:
                    # Si no se puede convertir a número, dejar como string
                    record[headers[i]] = value.strip()
            records.append(record)

        return records
    except Exception as e:
        raise Exception(f"Error inesperado: {str(e)}")

def balance_transactions(gastos, participantes, print_summary=True):
    # Inicializar el total de gastos por persona
    gastos_por_persona = {persona: 0 for persona in participantes}

    # Para cada gasto, calcular cuánto debe pagar cada participante
    for gasto in gastos:
        # Determinar quiénes participan en este gasto
        participantes_gasto = participantes  # por defecto, todos participan
        if 'participants' in gasto and gasto['participants']:
            # Si hay participantes específicos, convertir string a lista
            participantes_gasto = [p.strip() for p in gasto['participants'].split(',')]
            # Verificar que todos los participantes sean válidos
            if not all(p in participantes for p in participantes_gasto):
                raise ValueError(f"Participantes inválidos en gasto {gasto['item']}")

        # Calcular el gasto por persona para esta transacción
        gasto_por_persona = gasto['amount'] / len(participantes_gasto)

        # Asignar el gasto a cada participante
        for persona in participantes_gasto:
            gastos_por_persona[persona] += gasto_por_persona

    # Calcular cuánto ha pagado cada participante en total
    pagos_realizados = {persona: 0 for persona in participantes}
    for gasto in gastos:
        pagos_realizados[gasto['name']] += gasto['amount']

    # Calcular el balance de cada participante
    balances = {persona: pagos_realizados[persona] - gastos_por_persona[persona]
                for persona in participantes}

    # Separar participantes en acreedores y deudores
    acreedores = [(persona, balance) for persona, balance in balances.items() if balance > 0]
    deudores = [(persona, -balance) for persona, balance in balances.items() if balance < 0]

    # Minimizar transferencias
    transacciones = []
    i, j = 0, 0
    while i < len(deudores) and j < len(acreedores):
        deudor, deuda = deudores[i]
        acreedor, credito = acreedores[j]

        pago = min(deuda, credito)
        if pago >= 0.01:  # Solo agregar transacciones significativas
            transacciones.append(f"{deudor} debe pagarle a {acreedor} ${pago:.2f}")

        deudores[i] = (deudor, deuda - pago)
        acreedores[j] = (acreedor, credito - pago)

        if deudores[i][1] < 0.01:
            i += 1
        if acreedores[j][1] < 0.01:
            j += 1

    if print_summary:
        display("\nGastos realizados:")
        for gasto in gastos:
            participantes_str = " (para: " + gasto['participants'] + ")" if 'participants' in gasto and gasto['participants'] else " (para: Todos)"
            display(f"- {gasto['name']} gastó ${gasto['amount']:,.2f} en {gasto['item']}{participantes_str}")

        display("\nGasto total por persona (lo que debe pagar cada uno):")
        for persona, gasto in gastos_por_persona.items():
            display(f"- {persona}: ${gasto:,.2f}")

        display("\nPagos realizados por persona:")
        for persona, pago in pagos_realizados.items():
            display(f"- {persona}: ${pago:,.2f}")

        display("\nBalance final por persona:")
        for persona, balance in balances.items():
            display(f"- {persona}: ${balance:,.2f}")

        display("\nPagos pendientes:")
        for transaccion in transacciones:
            display(f"- {transaccion}")

    return transacciones

async def calculate_from_url(url):
    url = page["#sheet-url"][0].value
    gastos = await read_google_sheet(url)
    participantes = list(set(gasto["name"] for gasto in gastos))
    balance_transactions(gastos, participantes)
