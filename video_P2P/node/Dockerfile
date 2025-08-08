FROM python:3.11-slim

# Instalar dependencias del sistema si fueran necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

# Exponer puerto (Flask correrá en 0.0.0.0:$PORT)
EXPOSE 5000

CMD ["python", "app.py"]
