# Imagen base
FROM python:3.9

# Crear directorio de trabajo
WORKDIR /app

# Copiar los archivos de la app
COPY . /app

# Instalar dependencias
RUN pip install -r requirements.txt

# Ejecutar la aplicación
CMD ["python", "contar_votos_6.py"]
