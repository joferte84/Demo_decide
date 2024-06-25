def convert_kwh_to_int(consumo_str):
    """
    Convierte un string de consumo eléctrico en kWh a un entero.
    
    Args:
        consumo_str (str): Consumo en kWh como string.
    
    Returns:
        int: Consumo en kWh como entero.
    """
    if consumo_str is None:
        return 0
    try:
        consumo_int = int(float(consumo_str.replace("kWh", "").strip()))
        return consumo_int
    except ValueError:
        print(f"Error converting {consumo_str} to int.")
        return 0
    
def replace_decimal_points(data_dict):
    """
    Reemplaza los puntos decimales en los campos numéricos específicos de un diccionario por comas.
    
    Args:
        data_dict (dict): Diccionario con los datos.
    
    Returns:
        dict: Diccionario con los puntos decimales reemplazados por comas en los campos numéricos.
    """
    numeric_fields = ["importe_factura", "potencia_contratada"]
    
    for field in numeric_fields:
        if field in data_dict and isinstance(data_dict[field], str):
            data_dict[field] = data_dict[field].replace('.', ',')
    return data_dict
