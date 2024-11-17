from pyscript import fetch, display
from pyscript.web import page
import csv
from urllib.parse import urlparse
from io import StringIO

print("Analiza gastos")

async def leer_google_sheets(url):
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
        response = await fetch(
            f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv",
            method="GET"
        ).text()
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

def calcular_deudas(gastos, participantes, print_summary=True):
    # Calcular el gasto total
    total_gastos = sum(gasto['amount'] for gasto in gastos)
    # Calcular el gasto equitativo por persona
    gasto_ideal = total_gastos / len(participantes)

    # Calcular cuánto ha pagado cada participante
    pagos_realizados = {persona: 0 for persona in participantes}
    for gasto in gastos:
        pagos_realizados[gasto['name']] += gasto['amount']

    # Calcular el balance de cada participante
    balances = {persona: pagos_realizados[persona] - gasto_ideal for persona in participantes}

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
        transacciones.append(f"{deudor} debe pagarle a {acreedor} ${pago:.2f}")

        deudores[i] = (deudor, deuda - pago)
        acreedores[j] = (acreedor, credito - pago)

        if deudores[i][1] == 0:
            i += 1
        if acreedores[j][1] == 0:
            j += 1

    if print_summary:
        display("Gastos realizados:", target="result", append=True)
        for line in gastos:
            display(f'- {line["name"]} gastó {line["amount"]:,} en {line["item"]}', target="result", append=True)

        display("Gastos por persona:")
        for persona, gasto in pagos_realizados.items():
            display(f"- \t{persona}: ${gasto:,.2f}")
        display(f"Total de gastos: ${total_gastos:,.2f}")
        display(f"Gasto equitativo por persona: ${gasto_ideal:,.2f}")
        display("Pagos pendientes:")
        for r in transacciones:
            display(r)

    return transacciones

async def calculate_from_url(url):
    url = page["#new-task-content"][0].value
    gastos = await leer_google_sheets(url)
    participantes = list(set(gasto["name"] for gasto in gastos))
    calcular_deudas(gastos, participantes)
