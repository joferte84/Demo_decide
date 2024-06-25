from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, session
from werkzeug.utils import secure_filename
import os
import json
from ..all_openai import extract_info_from_pdf, query_openai_api, convert_kwh_to_int, replace_decimal_points
from .. import socketio

upload_bp = Blueprint('upload', __name__)

def ordenar_datos(data_dict):
    keys_order = [
        "nombre_cliente", "dni_cliente", "calle_cliente", "cp_cliente", "población_cliente", "provincia_cliente",
        "nombre_comercializadora", "cif_comercializadora", "dirección_comercializadora", "cp_comercializadora",
        "población_comercializadora", "provincia_comercializadora", "número_factura", "inicio_periodo", "fin_periodo",
        "importe_factura", "fecha_cargo", "consumo_periodo", "potencia_contratada"
    ]
    ordered_data = [(key, data_dict.get(key, '')) for key in keys_order]
    return ordered_data

def to_pretty_json(data):
    return json.dumps(data, indent=4, ensure_ascii=False)

def guardar_resultados(results):
    extraction_folder = os.path.join(current_app.root_path, 'extracción')
    if not os.path.exists(extraction_folder):
        os.makedirs(extraction_folder)

    for idx, result in enumerate(results):
        file_path = os.path.join(extraction_folder, f'result_{idx + 1}.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

def process_pdf(file_path, api_key):
    try:
        extracted_text = extract_info_from_pdf(file_path)
        extracted_data = query_openai_api(extracted_text, api_key)
        if extracted_data:
            data_dict = json.loads(extracted_data)
            data_dict['consumo_periodo'] = convert_kwh_to_int(data_dict.get('consumo_periodo', '0 kWh'))
            data_dict = replace_decimal_points(data_dict)
            return data_dict, None
    except Exception as e:
        return None, str(e)
    return None, "No data returned from API"

@upload_bp.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('files')
        api_key = request.form['api_key']
        session['api_key'] = api_key
        results = []
        total_files = len(files)
        session['progress'] = 0
        max_retries = 3

        for idx, file in enumerate(files):
            if file and file.filename.endswith('.pdf'):
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
                    os.makedirs(current_app.config['UPLOAD_FOLDER'])
                file.save(file_path)

                for attempt in range(max_retries):
                    try:
                        extracted_text = extract_info_from_pdf(file_path)
                        extracted_data = query_openai_api(extracted_text, api_key)
                        if extracted_data:
                            data_dict = json.loads(extracted_data)
                            data_dict['consumo_periodo'] = convert_kwh_to_int(data_dict.get('consumo_periodo', '0 kWh'))
                            data_dict = replace_decimal_points(data_dict)
                            data_dict = ordenar_datos(data_dict)
                            results.append(data_dict)
                            break
                        else:
                            raise ValueError("Failed to get valid response from API")
                    except Exception as e:
                        flash(f'Attempt {attempt + 1} failed for {filename}: {str(e)}')
                        if attempt == max_retries - 1:
                            flash(f'File {filename} failed after {max_retries} attempts.')

                progress = int(((idx + 1) / total_files) * 100)
                session['progress'] = progress
                socketio.emit('progress_update', {'progress': progress}, namespace='/')

        session['results'] = results
        guardar_resultados(results)
        socketio.emit('progress_update', {'progress': 100}, namespace='/')
        return redirect(url_for('upload.results'))

    api_key = session.get('api_key', '')
    return render_template('index.html', api_key=api_key, show_back_button=False)

@upload_bp.route('/results')
def results():
    results = session.get('results', [])
    results_json = [json.loads(to_pretty_json(result)) for result in results]
    return render_template('results.html', data=results_json, show_back_button=True)

@upload_bp.route('/analysis')
def analysis():
    return render_template('analysis.html', show_back_button=True)
