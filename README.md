# Sistema de Gestión Aduanera

Este es un sistema desarrollado en *Django* para la gestión de procesos aduaneros. Incluye funcionalidades de CRUD (Crear, Leer, Actualizar, Eliminar) distribuidas en seis apartados principales. Cada segmento está diseñado para ser amigable con el usuario, implementando una interfaz intuitiva y un flujo eficiente.

*Visualización del proyecto:* https://aduanaco.site

## Características principales

1. *Modelo Vista Controlador (MVC):*
   - Separación clara entre lógica de negocio, controladores y vistas para mantener el código organizado y fácil de escalar.

2. *CRUD Completo:*
   - Operaciones de gestión para diferentes segmentos, como cargas, exportaciones, usuarios, transportes, controles, etc.

3. *Interfaz amigable:*
   - Enfocada en minimizar el número de clics necesarios.
   - Selección intuitiva de IDs relacionados mediante listas desplegables.

4. *Seguridad:*
   - Control de acceso basado en roles (por ejemplo, supervisores).
   - Redirección automática en caso de intentos de acceso no autorizado.

5. *Frontend intuitivo:*
   - Uso de plantillas HTML estilizadas con CSS para proporcionar una experiencia de usuario optimizada.

---

## Estructura del proyecto
```
DesarrolloWeb-Django/
├── Aduanas/                # Carpeta principal del proyecto Django
│   ├── Aduanas/            # Configuración del proyecto
│   │   ├── settings.py     # Configuración general del proyecto
│   │   ├── urls.py         # Enrutamiento principal
│   │   ├── asgi.py         # Configuración ASGI
│   │   └── wsgi.py         # Configuración WSGI
│   ├── Estacion/           # Aplicación principal del sistema
│   │   ├── admin.py        # Configuración del administrador Django
│   │   ├── models.py       # Definición de modelos y relaciones
│   │   ├── views.py        # Lógica de vistas
│   │   ├── urls.py         # Enrutamiento específico de la aplicación
│   │   ├── templates/      # Plantillas HTML
│   │   ├── static/         # Archivos estáticos (CSS, imágenes)
│   │   └── migrations/     # Archivos de migración de la base de datos
│   └── manage.py           # Archivo principal para comandos Django
├── db.sqlite3              # Base de datos SQLite (reemplazar por PostgreSQL)
└── requirements.txt        # Dependencias del proyecto
```

---

## Instalación y configuración

### 1. *Clonar el repositorio*
   Clona el repositorio en tu máquina local:
   ```bash
   git clone https://github.com/alegria666/DesarrolloWeb-Django.git
   cd Aduanas
   ```

### 2. Configurar las dependencias

Instala los paquetes necesarios usando pip:
```bash
pip install -r requirements.txt
```

### 3. Configurar la base de datos (PostgreSQL)

Este proyecto utiliza PostgreSQL como sistema de gestión de bases de datos. A continuación, se presenta una configuración adaptada para que funcione correctamente con los modelos del proyecto.

#### Paso 1: Configurar PostgreSQL

1. Instala PostgreSQL y pgAdmin4 en tu máquina local.

2. Crea una base de datos en PostgreSQL, sugerencia:
```sql
CREATE DATABASE Aduana;
CREATE USER user WITH PASSWORD '1234';
ALTER ROLE user SET client_encoding TO 'utf8';
ALTER ROLE user SET default_transaction_isolation TO 'read committed';
ALTER ROLE user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE Aduana TO user;
```

#### Paso 2: Configurar `settings.py`

Modifica el archivo `settings.py` para usar PostgreSQL con los parámetros específicos configurados anteriormente o como los configures respetando los parámetros creados:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'Aduana',        # Nombre de la base de datos
        'USER': 'user',           # Usuario de la base de datos
        'PASSWORD': '1234',       # Contraseña del usuario
        'HOST': 'localhost',              # Dirección del servidor
        'PORT': '5433',                   # Puerto de PostgreSQL
    }
}
```

#### Paso 3: Migrar los modelos

Ejecuta las migraciones de la base de datos para generar las tablas necesarias:
```bash
python manage.py migrate
```

---

### 4. Ejecutar el servidor

Inicia el servidor local para probar el sistema:
```bash
python manage.py runserver
```

Accede a la aplicación en [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Apartados principales

1. **Inicio**  
   Página principal del sistema.

2. **Login**  
   Gestión de autenticación y control de acceso basado en roles.

3. **Servicios**  
   Módulo para acceder a las diferentes funcionalidades del sistema.

4. **CRUD de entidades**  
   - **Cargas**: Gestión de mercancías ingresadas.
   - **Usuarios**: Gestión de usuarios del sistema.
   - **Exportaciones**: Control de mercancías exportadas.
   - **Importaciones**: Seguimiento de mercancías ingresadas.
   - **Transportes**: Registro y seguimiento de vehículos.
   - **Controles**: Supervisión y monitoreo de actividades específicas.

5. **Reportes**  
   Generación y consulta de informes sobre las actividades realizadas.

---

## Tecnologías utilizadas

**Backend:**
- Django (framework principal)
- PostgreSQL (base de datos)

**Frontend:**
- HTML, CSS (diseño responsivo y estilizado)

**Gestión de dependencias:**
- Archivo `requirements.txt` para mantener un entorno limpio.

---

## Buenas prácticas implementadas

1. **Modelo Vista Controlador (MVC):**
   - Separación clara entre la lógica de negocio, la presentación y el control.

2. **Llaves foráneas y relaciones:**
   - Selección simplificada de IDs relacionados para evitar errores y facilitar el flujo del usuario.

3. **Seguridad en vistas:**
   - Decoradores para proteger accesos no autorizados.

4. **Manejo de errores:**
   - Páginas específicas para estados como acceso no autorizado o errores en el sistema.

---

## Créditos

Desarrollado por Daniel Esteban Alegría Zamora como un sistema completo para la gestión aduanera. Si tienes preguntas o necesitas soporte, no dudes en contactarme.

