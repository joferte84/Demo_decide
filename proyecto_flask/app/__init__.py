from flask import Flask
from flask_socketio import SocketIO
from datetime import timedelta
import os
from dotenv import load_dotenv

socketio = SocketIO()

def create_app():
    load_dotenv() 
    print("Cargando variables de entorno...")
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
    print(f"SECRET_KEY configurada: {app.config['SECRET_KEY']}")
    app.config['UPLOAD_FOLDER'] = 'uploads/'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    from .routes.upload_routes import upload_bp
    from .routes.progress_routes import progress_bp
    from .routes.download_routes import download_bp
    from .routes.analysis_routes import analysis_bp

    app.register_blueprint(upload_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(download_bp)
    app.register_blueprint(analysis_bp)

    socketio.init_app(app, manage_session=True)

    return app
