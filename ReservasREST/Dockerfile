# Dockerfile para el servicio REST (ReservasRest.py)

# 1. Imagen base con Python
FROM python:3.11-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar los archivos necesarios al contenedor
COPY ReservasRest.py .
COPY requirements.txt .

# 4. Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Exponer el puerto 5000 (el puerto del servicio REST)
EXPOSE 5000

# 6. Comando para ejecutar el servicio
CMD ["python", "ReservasRest.py"]
