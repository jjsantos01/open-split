from pyscript import fetch, display
from pyscript.web import page
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
            # URL formato: https://docs.google.com/spreadsheets/d/[ID]/edit?gid=0
            doc_id = url.split('/d/')[1].split('/')[0]
            gid = url.split('gid=')[1] if 'gid=' in url else '0'
        else:
            raise ValueError("No se pudo extraer el ID del documento de la URL")
        # Construir la URL de exportación CSV
        csv_url = f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv&gid={gid}"
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

def parse_participants(participants_str, total_amount, all_participants):
    """
    Parsea la cadena de participantes y sus montos.
    Retorna un diccionario con los montos asignados a cada participante.
    """
    if not participants_str:
        # Si no hay participantes especificados, dividir entre todos equitativamente
        amount_per_person = total_amount / len(all_participants)
        return {p: amount_per_person for p in all_participants}

    # Inicializar el diccionario de participantes y montos
    participant_amounts = {}
    participants_without_amount = []
    remaining_amount = total_amount

    # Procesar cada participante
    for part in participants_str.split(','):
        part = part.strip()
        if '=' in part:
            # Participante con monto específico
            name, amount = part.split('=')
            name = name.strip()
            amount = float(amount.strip())
            if name not in all_participants:
                raise ValueError(f"Participante inválido: {name}")
            participant_amounts[name] = amount
            remaining_amount -= amount
        else:
            # Participante sin monto específico
            if part not in all_participants:
                raise ValueError(f"Participante inválido: {part}")
            participants_without_amount.append(part)

    # Verificar que el monto total no exceda el gasto
    if remaining_amount < 0:
        raise ValueError("La suma de los montos especificados excede el total del gasto")

    # Distribuir el monto restante entre los participantes sin monto específico
    if participants_without_amount:
        amount_per_remaining = remaining_amount / len(participants_without_amount)
        for participant in participants_without_amount:
            participant_amounts[participant] = amount_per_remaining

    return participant_amounts

def balance_transactions(gastos, participantes, display_summary=True):
    # Inicializar el total de gastos por persona
    gastos_por_persona = {persona: 0 for persona in participantes}

    # Para cada gasto, calcular cuánto debe pagar cada participante
    for gasto in gastos:
        try:
            # Determinar los montos por participante
            participantes_montos = parse_participants(
                gasto.get('participants', ''),
                gasto['amount'],
                participantes
            )

            # Asignar los gastos a cada participante
            for persona, monto in participantes_montos.items():
                gastos_por_persona[persona] += monto

        except Exception as e:
            raise ValueError(f"Error en gasto '{gasto['item']}': {str(e)}")

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

    if display_summary:
        display("\nGastos realizados:", target="results", append=False)
        for gasto in gastos:
            participantes_montos = parse_participants(
                gasto.get('participants', ''),
                gasto['amount'],
                participantes
            )
            desglose = ", ".join([f"{p}: ${m:.2f}" for p, m in participantes_montos.items()])
            display(f"- {gasto['name']} gastó ${gasto['amount']:,.2f} en {gasto['item']}", target="results")
            display(f"  -- Desglose: {desglose}", target="results")

        display("\nGasto total por persona (lo que debe pagar cada uno):", target="results")
        for persona, gasto in gastos_por_persona.items():
            display(f"- {persona}: ${gasto:,.2f}", target="results")

        display("\nPagos realizados por persona:", target="results")
        for persona, pago in pagos_realizados.items():
            display(f"- {persona}: ${pago:,.2f}", target="results")

        display("\nBalance final por persona:", target="results")
        for persona, balance in balances.items():
            display(f"- {persona}: ${balance:,.2f}", target="results")

        display("\nPagos pendientes:", target="results")
        for transaccion in transacciones:
            display(f"- {transaccion}", target="results")

    return transacciones

async def calculate_from_url(url):
    url = page["#sheet-url"][0].value
    results_div = page["#results"][0]
    results_div.innerHTML = "Calculando..."
    gastos = await read_google_sheet(url)
    participantes = list(set(gasto["name"] for gasto in gastos))
    balance_transactions(gastos, participantes)
