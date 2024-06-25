from datetime import datetime
import locale

def reformat_date(date_str):
    """
    Reformatea una fecha en string a un formato estándar "dd.mm.yyyy".
    
    Args:
        date_str (str): Fecha en formato string.
    
    Returns:
        str: Fecha reformateada o el string original si el formato no es reconocido.
    """
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    date_formats = [
        "%d/%m/%Y", "%Y-%m-%d", "%d-%b-%Y",
        "%d de %B de %Y", "%d de %b de %Y", "%d de %m de %Y",
        "%B %d, %Y", "%b %d, %Y", # En inglés
        "%d de enero de %Y", "%d de febrero de %Y", "%d de marzo de %Y",  
        "%d de abril de %Y", "%d de mayo de %Y", "%d de junio de %Y",
        "%d de julio de %Y", "%d de agosto de %Y", "%d de septiembre de %Y",
        "%d de octubre de %Y", "%d de noviembre de %Y", "%d de diciembre de %Y" # En español
    ]

    for fmt in date_formats:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            return parsed_date.strftime("%d.%m.%Y")
        except ValueError:
            continue
    return date_str
