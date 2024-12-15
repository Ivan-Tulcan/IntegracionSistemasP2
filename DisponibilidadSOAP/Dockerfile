# Dockerfile para el servicio SOAP (DisponibilidadSoap.py)

# 1. Imagen base con Python
FROM python:3.11.9-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar el script Python al contenedor
COPY DisponibilidadSoap.py .

# 4. Copiar el archivo de dependencias
COPY requirements.txt .

# 5. Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 6. Exponer el puerto 8000 (el puerto del servicio SOAP)
EXPOSE 8000

# 7. Comando para ejecutar el servicio
CMD ["python", "DisponibilidadSoap.py"]
