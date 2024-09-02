# Sistema de Gestión de Inventario

## Descripción del Problema

El objetivo es desarrollar un sistema de gestión de inventario que mejore la administración de productos en una bodega, permitiendo el registro y seguimiento de las operaciones de entrada y salida de productos. Este sistema utiliza identificadores únicos para cada artículo y se integra con una base de datos relacional para el almacenamiento de datos.

## Requerimientos Específicos

### Backend con Python

1. **Implementación de la API REST:**
   - Implementar una API REST en contenedores Docker para gestionar las operaciones del inventario.
   - Integrar una base de datos relacional (SQL Server, MariaDB o PostgreSQL) para el almacenamiento de datos.
   - Incluir funcionalidades para leer códigos QR y registrar entradas y salidas de productos, así como la gestión de productos defectuosos.

2. **Integración con una Base de Datos Relacional:**
   - Utilizar una base de datos relacional como PostgreSQL, MariaDB o SQL Server.
   - Implementar modelos de datos y migraciones para la estructura de la base de datos.

## Estado del Proyecto

Actualmente, el proyecto está en proceso de construcción. Se está trabajando en la integración de Swagger para la documentación de la API.

## Dockerfile

```dockerfile
FROM python:3.10

# Instala las dependencias del sistema necesarias
RUN apt-get update && \
    apt-get install -y \
    libzbar0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
```

## docker-compose.yml

```yaml
version: '3.8'
services:  
  db:    
    image: postgres:16
    environment:      
      POSTGRES_USER: postgres      
      POSTGRES_PASSWORD: 123456      
      POSTGRES_DB: productos_gestion    
    volumes:      
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"  # This line exposes the port
  web:    
    build: .    
    ports:
      - "5000:5000"    
    environment:      
      FLASK_APP: app.py      
      FLASK_ENV: development      
      DATABASE_URL: postgresql://postgres:123456@db:5432/productos_gestion    
    depends_on:      
      - db
    command: flask run --host=0.0.0.0 --port=5000
volumes:  
  postgres_data:
```

## Instrucciones de Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_PROYECTO>
   ```

2. **Crear un archivo `.env` con las variables de entorno necesarias (opcional):**

   ```bash
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=123456
   POSTGRES_DB=productos_gestion
   FLASK_APP=app.py
   FLASK_ENV=development
   DATABASE_URL=postgresql://postgres:123456@db:5432/productos_gestion
   ```

3. **Construir y levantar los contenedores con Docker:**
   ```bash
   docker-compose up --build
   ```

4. **Acceder a la API:**
   La API estará disponible en `http://localhost:5000`.

## Estructura del Proyecto

- `app.py`: Configuración principal de la aplicación Flask.
- `models.py`: Definición de los modelos de la base de datos.
- `routes.py`: Definición de las rutas de la API.
- `requirements.txt`: Dependencias del proyecto.
- `docker-compose.yml`: Archivo para definir y gestionar los servicios con Docker.
- `Dockerfile`: Archivo para construir la imagen Docker del backend.

## Ejemplo de Uso

Para probar las funcionalidades de la API, se pueden utilizar herramientas como Postman o cURL para realizar peticiones a las rutas definidas en `routes.py`. Por ejemplo, para añadir un nuevo producto:

```bash
curl -X POST http://localhost:5000/products -H "Content-Type: application/json" -d '{"name": "Producto A", "quantity": 10}'
```

## Notas Adicionales

- Asegúrate de tener Docker y Docker Compose instalados en tu máquina.
- Para administrar la base de datos, puedes utilizar herramientas como pgAdmin o DBeaver.
- La documentación de la API se añadirá utilizando Swagger en futuras versiones del proyecto.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

```

Este `README.md` cubre todos los aspectos mencionados y proporciona instrucciones claras para configurar y ejecutar el proyecto.
