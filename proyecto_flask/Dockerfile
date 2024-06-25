# Usa una imagen base de Python 3.12
FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos y los archivos del proyecto al contenedor
COPY requirements.txt requirements.txt
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Expone el puerto en el que correrá la aplicación
EXPOSE 5000

# Define el comando para correr la aplicación
CMD ["gunicorn", "-k", "eventlet", "-w", "4", "--timeout", "120", "-b", "0.0.0.0:5000", "run:app"]
