FROM python:3.12-slim

# Instalar dependencias del sistema necesarias para Odoo
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libldap2-dev \
    libsasl2-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    libpq-dev \
    postgresql-client \
    node-less \
    npm \
    git \
    && rm -rf /var/lib/apt/lists/*

# Crear el usuario odoo
RUN useradd -m -d /opt/odoo -s /bin/bash odoo

# Establecer el directorio de trabajo
WORKDIR /opt/odoo

# Copiar el archivo requirements.txt primero (para aprovechar la caché de Docker)
COPY requirements.txt /opt/odoo/
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente
COPY . /opt/odoo/

# Asegurar permisos correctos
RUN chown -R odoo:odoo /opt/odoo

# Crear carpeta para data externa de ser necesario (opcional)
RUN mkdir -p /var/lib/odoo && chown -R odoo:odoo /var/lib/odoo

# Cambiar al usuario odoo
USER odoo

# Exponer el puerto de Odoo
EXPOSE 8069

# Comando por defecto para iniciar Odoo
CMD ["python3", "odoo-bin", "-c", "despliegue/config/odoo.conf"]
