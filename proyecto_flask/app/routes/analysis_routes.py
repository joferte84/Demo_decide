from flask import Blueprint, render_template, request, flash, redirect, url_for
import matplotlib
matplotlib.use('Agg')  # Cambia el backend de matplotlib a 'Agg'
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import json
from werkzeug.utils import secure_filename

analysis_bp = Blueprint('analysis', __name__)

provincia_to_comunidad = {
    "A Coruña": "Galicia",
    "Álava": "País Vasco",
    "Albacete": "Castilla-La Mancha",
    "Alicante": "C. Valenciana",
    "Almería": "Andalucía",
    "Asturias": "Asturias",
    "Ávila": "Castilla y León",
    "Badajoz": "Extremadura",
    "Baleares": "Islas Baleares",
    "Barcelona": "Cataluña",
    "Burgos": "Castilla y León",
    "Cáceres": "Extremadura",
    "Cádiz": "Andalucía",
    "Cantabria": "Cantabria",
    "Castellón": "C. Valenciana",
    "Ceuta": "Ceuta",
    "Ciudad Real": "Castilla-La Mancha",
    "Córdoba": "Andalucía",
    "Cuenca": "Castilla-La Mancha",
    "Girona": "Cataluña",
    "Granada": "Andalucía",
    "Guadalajara": "Castilla-La Mancha",
    "Guipúzcoa": "País Vasco",
    "Huelva": "Andalucía",
    "Huesca": "Aragón",
    "Jaén": "Andalucía",
    "La Rioja": "La Rioja",
    "Las Palmas": "Canarias",
    "León": "Castilla y León",
    "Lleida": "Cataluña",
    "Lugo": "Galicia",
    "Madrid": "Madrid",
    "Málaga": "Andalucía",
    "Melilla": "Melilla",
    "Murcia": "Murcia",
    "Navarra": "Navarra",
    "Ourense": "Galicia",
    "Palencia": "Castilla y León",
    "Pontevedra": "Galicia",
    "Salamanca": "Castilla y León",
    "Santa Cruz de Tenerife": "Canarias",
    "Segovia": "Castilla y León",
    "Sevilla": "Andalucía",
    "Soria": "Castilla y León",
    "Tarragona": "Cataluña",
    "Teruel": "Aragón",
    "Toledo": "Castilla-La Mancha",
    "Valencia": "C. Valenciana",
    "Valladolid": "Castilla y León",
    "Vizcaya": "País Vasco",
    "Zamora": "Castilla y León",
    "Zaragoza": "Aragón"
}

def get_comunidad(provincia):
    # Intentar con el nombre completo
    comunidad = provincia_to_comunidad.get(provincia)
    if comunidad:
        return comunidad
    
    # Intentar con la primera palabra
    primera_palabra = provincia.split('/')[0]
    comunidad = provincia_to_comunidad.get(primera_palabra)
    if comunidad:
        return comunidad
    
    # Intentar con la segunda palabra si existe
    if '/' in provincia:
        segunda_palabra = provincia.split('/')[1]
        comunidad = provincia_to_comunidad.get(segunda_palabra)
        if comunidad:
            return comunidad
    
    return "Desconocida"

@analysis_bp.route('/analysis', methods=['GET', 'POST'])
def analysis():
    if request.method == 'POST':
        files = request.files.getlist('files')
        if not files:
            flash('No se han subido archivos para analizar.')
            return redirect(url_for('analysis.analysis'))

        results = []
        for file in files:
            if file and file.filename.endswith('.json'):
                filename = secure_filename(file.filename)
                file_content = file.read().decode('utf-8')
                try:
                    data_dict = json.loads(file_content)
                    results.append(data_dict)
                except json.JSONDecodeError as e:
                    flash(f'Error decodificando JSON para el archivo {filename}: {str(e)}')
                    return redirect(url_for('analysis.analysis'))
            else:
                flash(f'{file.filename} no es un archivo JSON válido.')
                return redirect(url_for('analysis.analysis'))

        # Crear gráficos de análisis
        graphs = []

        # Gráfico de comunidades autónomas de clientes
        comunidades_cliente = [get_comunidad(result.get('provincia_cliente')) for result in results if result.get('provincia_cliente') is not None]
        comunidades_cliente.sort()  # Ordenar alfabéticamente
        plt.figure(figsize=(12, 6))  # Ajustar tamaño de la figura
        plt.hist(comunidades_cliente, bins=len(set(comunidades_cliente)), edgecolor='black')
        plt.title('Distribución de Comunidades Autónomas de Clientes')
        plt.xlabel('Comunidad Autónoma')
        plt.ylabel('Frecuencia')
        plt.xticks(rotation=45, ha='right')
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        graphs.append(f'data:image/png;base64,{image_base64}')
        plt.close()

        # Gráfico de comunidades autónomas de comercializadoras
        comunidades_comercializadora = [get_comunidad(result.get('provincia_comercializadora')) for result in results if result.get('provincia_comercializadora') is not None]
        comunidades_comercializadora.sort()  # Ordenar alfabéticamente
        plt.figure(figsize=(12, 6))  # Ajustar tamaño de la figura
        plt.hist(comunidades_comercializadora, bins=len(set(comunidades_comercializadora)), edgecolor='black')
        plt.title('Distribución de Comunidades Autónomas de Comercializadoras')
        plt.xlabel('Comunidad Autónoma')
        plt.ylabel('Frecuencia')
        plt.xticks(rotation=45, ha='right')
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        graphs.append(f'data:image/png;base64,{image_base64}')
        plt.close()

        # Gráfico de importes de factura
        importes_factura = [float(result['importe_factura'].replace('€', '').replace(',', '.').strip()) for result in results if result.get('importe_factura') is not None]
        plt.figure(figsize=(12, 6))  # Ajustar tamaño de la figura
        plt.hist(importes_factura, bins=10, edgecolor='black')
        plt.title('Distribución de Importes de Factura')
        plt.xlabel('Importe (€)')
        plt.ylabel('Frecuencia')
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        graphs.append(f'data:image/png;base64,{image_base64}')
        plt.close()

        # Gráfico de consumo en el periodo
        consumos_periodo = [result.get('consumo_periodo') for result in results if result.get('consumo_periodo') is not None]
        plt.figure(figsize=(12, 6))  # Ajustar tamaño de la figura
        plt.hist(consumos_periodo, bins=10, edgecolor='black')
        plt.title('Distribución de Consumos en el Periodo')
        plt.xlabel('Consumo (kWh)')
        plt.ylabel('Frecuencia')
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        graphs.append(f'data:image/png;base64,{image_base64}')
        plt.close()

        # Gráfico de potencia contratada
        potencias_contratadas = [float(result['potencia_contratada'].replace('kW', '').replace(',', '.').strip()) for result in results if result.get('potencia_contratada') is not None]
        plt.figure(figsize=(12, 6))  # Ajustar tamaño de la figura
        plt.hist(potencias_contratadas, bins=10, edgecolor='black')
        plt.title('Distribución de Potencia Contratada')
        plt.xlabel('Potencia (kW)')
        plt.ylabel('Frecuencia')
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        graphs.append(f'data:image/png;base64,{image_base64}')
        plt.close()

        return render_template('analysis.html', graphs=graphs, show_back_button=True)

    return render_template('analysis.html', graphs=None, show_back_button=True)
