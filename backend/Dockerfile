# Imagen base ligera de Python
FROM python:3.8

# Buenas prácticas: no generar .pyc y salida sin buffer (logs en tiempo real)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1) Instalar dependencias primero para aprovechar la caché de capas de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copiar el código fuente de la aplicación
COPY . .

# El contenedor expone el puerto interno 5050
EXPOSE 5050

# Servidor de PRODUCCIÓN (Gunicorn) con 2 procesos de trabajo
CMD ["gunicorn", "--bind", "0.0.0.0:5050", "--workers", "2", "app:app"]
