import PyPDF2 

def extract_info_from_pdf(path):
    """
    Extrae el texto de un archivo PDF ubicado en la ruta especificada.
    
    Args:
        path (str): Ruta al archivo PDF.
    
    Returns:
        str: Texto extraído del archivo PDF.
    """
    with open(path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
