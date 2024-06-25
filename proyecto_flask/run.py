import sys
import os
from flask_socketio import SocketIO

# Agregar el directorio 'app' al sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app

socketio = SocketIO()

app = create_app()
socketio.init_app(app, manage_session=True)

if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0')
