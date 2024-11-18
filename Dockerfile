# Usa una imagen base oficial de Python
FROM python:3.8-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo requirements.txt en el directorio de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación en el directorio de trabajo
COPY . .

# Configura las variables de entorno para Flask
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Expone el puerto en el que la aplicación correrá
EXPOSE 8023

# Comando para ejecutar la aplicación con Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=8023"]