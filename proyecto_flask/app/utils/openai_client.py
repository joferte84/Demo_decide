import openai

def query_openai_api(text, api_key, max_retries=5):
    """
    Consulta a la API de OpenAI para obtener datos estructurados a partir de texto desestructurado.
    
    Args:
        text (str): Texto desestructurado.
        api_key (str): Clave de API de OpenAI.
        max_retries (int): Número máximo de reintentos en caso de fallo.
    
    Returns:
        str: Respuesta de la API con los datos estructurados.
    """
    openai.api_key = api_key

    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a virtual assistant skilled in extracting structured data from unstructured text. Please extract the following fields from the text provided:"},
                    {"role": "user", "content": text},
                    {"role": "system", "content": """
                        Extract and list the following fields:
                        - Nombre del cliente (nombre_cliente),
                        - DNI del cliente (dni_cliente),
                        - Calle del cliente (calle_cliente),
                        - Código postal del cliente (cp_cliente),
                        - Población del cliente (población_cliente),
                        - Provincia del cliente (provincia_cliente),
                        - Nombre de la empresa comercializadora (nombre_comercializadora),
                        - CIF de la comercializadora (cif_comercializadora),
                        - Dirección de la comercializadora (dirección_comercializadora),
                        - Código postal de la comercializadora (cp_comercializadora),
                        - Población de la comercializadora (población_comercializadora),
                        - Provincia de la comercializadora (provincia_comercializadora),
                        - Número de factura (número_factura),
                        - Inicio del periodo de facturación (inicio_periodo),
                        - Fin del periodo de facturación (fin_periodo),
                        - Importe de la factura (importe_factura),
                        - Fecha del cargo (fecha_cargo) en formato fecha,
                        - Consumo en el periodo (consumo_periodo),
                        - Potencia contratada (potencia_contratada).
                    """}
                ],
                max_tokens=1000
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {str(e)}")
            if attempt == max_retries - 1:
                raise
