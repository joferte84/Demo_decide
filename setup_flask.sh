@echo off

REM Crear estructura de carpetas
mkdir proyecto_flask\app\static\css
mkdir proyecto_flask\app\static\js
mkdir proyecto_flask\app\templates

REM Crear archivos
echo from flask import Flask^

def create_app():^
    app = Flask(__name__)^
    from .routes import main^
    app.register_blueprint(main)^
    return app > proyecto_flask\app\__init__.py

echo from flask import Blueprint, render_template, request, redirect, url_for^
from werkzeug.utils import secure_filename^
import os^

main = Blueprint('main', __name__)^

@main.route('/')^
def index():^
    return render_template('index.html')^

@main.route('/upload', methods=['POST'])^
def upload_pdf():^
    if 'pdf' not in request.files:^
        return redirect(request.url)^
    file = request.files['pdf']^
    if file.filename == '':^
        return redirect(request.url)^
    if file and file.filename.endswith('.pdf'):^
        filename = secure_filename(file.filename)^
        file.save(os.path.join('path/to/save', filename))^
        return render_template('results.html', filename=filename)^
    return redirect(url_for('main.index')) > proyecto_flask\app\routes.py

echo from app import create_app^

app = create_app()^

if __name__ == '__main__':^
    app.run(debug=True) > proyecto_flask\run.py

REM Crear el archivo requirements.txt
type nul > proyecto_flask\requirements.txt

echo Flask project structure is ready.
