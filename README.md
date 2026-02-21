# UpsideRolls: StrangerRPG Documentación

## Configuración rápida del proyecto con PostgreSQL
**No usar ninguna de las credenciales de ejemplo**


### Paso 1 - Crear entorno virtual
```
python -m venv venv
```
### Paso 2 - Activar entorno virtua
```
source venv/bin/activate
```
### Paso 3 - Instalar las dependencias

Ejectuamos el siguiente comando en nuestro entorno virtual
```
pip install -r requirements.txt
```

### Paso 4 - Instalar PostgreSQL en el sistema

```
sudo apt update
sudo apt install postgresql postgresql-contrib
```
Verificar que está activo:
```
sudo systemctl status postgresql
```

### Paso 5 - Entrar como superusuario de PostgreSQL
```
sudo -u postgres psql
```
### Paso 6 - Crear usuario para Django
```
CREATE USER usuario_ejemplo WITH PASSWORD '1234';
```
### Paso 7 – Crear base de datos con owner
```
CREATE DATABASE db_ejemplo OWNER usuario_ejemplo;
```

### Paso 8 - Creamos un archivo .env para nuestras variables de entorno

```
DB_NAME=db_ejemplo
DB_USER=usuario_ejemplo
DB_PASSWORD=1234
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=clave_secreta
DEBUG=True
```

### Paso 9 - Aplicar migraciones
```
python manage.py migrate
```