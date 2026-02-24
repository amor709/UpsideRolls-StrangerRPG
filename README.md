# UpsideRolls: StrangerRPG Documentación

## Configuración rápida del proyecto con PostgreSQL
**No usar ninguna de las credenciales de ejemplo**


### Paso 1 - Revisar la instalación de Docker en tu sistema
```
docker --version
docker compose version
```

### Paso 2 - Creamos un archivo .env para nuestras variables de entorno

```
POSTGRES_DB=db_ejemplo
POSTGRES_USER=usuario_ejemplo
POSTGRES_PASSWORD=1234

DB_NAME=db_ejemplo
DB_USER=usuario_ejemplo
DB_PASSWORD=1234
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=clave_secreta
DEBUG=True
```


### Paso 4 - Construir y levantar los contenedores
```
docker compose up --build
```

### Paso 5 - Acceder a la aplicación
```
http://localhost:8000
```

