# Procesador de PDFs

## Descripción

El Procesador de PDFs es una aplicación web desarrollada en Flask que permite a los usuarios cargar múltiples facturas de la luz en PDF, procesarlos y extraer información clave usando la API de OpenAI. Los resultados se pueden visualizar y analizar en una página de resultados.

## Características

- Carga de múltiples Archivos PDF: Permite cargar varios archivos PDF a la vez.
- Procesamiento de PDF: Utiliza la API de OpenAI para extraer información clave de los PDFs y muestra en una tabla los datos extraídos.
- GIF de Carga: Muestra un GIF animado mientras se procesan los archivos.
- Análisis de JSON: Permite visualizar y analizar los resultados en formato JSON.

## Requisitos
- Python 3.12
- Flask
- Flask-SocketIO
- OpenAI API Key
- Docker (para despliegue con Docker)

# Instalación 

1. Clonar el repositorio

```bash
git clone <Demo_decide>
cd <Demo_decide>
```

2. Crear el entorno virtual (opcional pero recomendado)

```bash
python -m venv env
source env/bin/activate 
```

3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno
Crear un archivo `.env` en el directorio raíz con las siguientes variables:

```bash
SECRET_KEY=your-very-secret-key
API_KEY=your-valid-api-key
```

5. Construye y levanta los servicios de Docker:
```bash
docker-compose up --build
```
## Uso

### Ejecución local

1. Accede a la aplicación en tu navegador web:
```plaintext
http://localhost:5000
```

2. Sube las facturas PDF y proporciona tu clave API de OpenAI

3. Haz clic en "Upload" y espera a que los archivos se procesen. El progreso se mostrará mediante un GIF animado.

4. Revisa los resultados en la página de resultados.

5. Cuando tengas los json suficientes, ve a la pestaña de analisis e ingresa los json.

## Estructura del proyecto

```plaintext
proyecto_flask/
├── app/
│   ├── __init__.py
│   ├── all_openai.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── analysis_routes.py
│   │   ├── download_routes.py
│   │   ├── progress_routes.py
│   │   └── upload_routes.py
│   ├── static/
│   │   ├── css/
│   │   ├── images/
│   │   │   ├── decide.png
│   │   │   └── giphy.webp
│   │   └── js/
│   ├── templates/
│   │   ├── analysis.html
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── results.html
│   │   └── upload_success.html
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── date_utils.py
│   │   ├── energy_utils.py
│   │   ├── openai_client.py
│   │   └── pdf_processor.py
├── .dockerignore
├── .env
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.py
└── setup_flask.sh
```































