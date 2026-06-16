# Etapa base
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias Python 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Codigo fuente
COPY . .

# Recolectar archivos estáticos de Django
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Comando para arrancar la aplicación
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn myproject.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120 --access-logfile - --error-logfile -"]
