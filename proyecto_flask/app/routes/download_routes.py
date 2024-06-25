from flask import Blueprint, send_file, session, jsonify
import zipfile
from io import BytesIO

download_bp = Blueprint('download', __name__)

@download_bp.route('/download_all_jsons')
def download_all_jsons():
    results = session.get('results', [])
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for idx, result in enumerate(results):
            filename = f'result_{idx + 1}.json'
            json_data = jsonify(result).get_data(as_text=True)
            zf.writestr(filename, json_data)
    memory_file.seek(0)
    return send_file(memory_file, mimetype='application/zip', as_attachment=True, download_name='all_results.zip')

@download_bp.route('/download_json/<int:index>')
def download_json(index):
    results = session.get('results', [])
    if 0 <= index < len(results):
        json_data = jsonify(results[index]).get_data(as_text=True)
        return send_file(BytesIO(json_data.encode()), mimetype='application/json', as_attachment=True, download_name=f'result_{index + 1}.json')
    return "Index out of range", 404

@download_bp.route('/download_zip_single/<int:index>')
def download_zip_single(index):
    results = session.get('results', [])
    if 0 <= index < len(results):
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            filename = f'result_{index + 1}.json'
            json_data = jsonify(results[index]).get_data(as_text=True)
            zf.writestr(filename, json_data)
        memory_file.seek(0)
        return send_file(memory_file, mimetype='application/zip', as_attachment=True, download_name=f'result_{index + 1}.zip')
    return "Index out of range", 404
