# PICM Django REST API

Este proyecto es una API RESTful construida con Django y Django REST Framework para la plataforma de gestión de inventario PICM, como proyecto para el curso Desarrollo de Software

## Características

### 🔐 Autenticación y Usuarios
- Autenticación JWT (JSON Web Tokens)
- Login/logout de usuarios
- Refresh token para renovación automática
- Recuperación de contraseña por correo electrónico

### 📦 Gestión de Productos
- CRUD completo de productos
- Gestión de categorías
- Control de stock e inventario
- Búsqueda y filtrado avanzado
- Paginación de resultados
- Cálculo de valor total del inventario

### 🏭 Gestión de Suministros
- CRUD completo de suministros
- Gestión de proveedores
- Control de stock de suministros
- Cálculo de valor total del inventario de suministros

### 📊 Movimientos y Transacciones
- Registro de movimientos de productos
- Registro de movimientos de suministros
- Historial completo de transacciones
- Tipos de movimientos (entrada, salida, ajuste)

### 📈 Estadísticas y Reportes
- Estadísticas de productos más vendidos
- Estadísticas de productos con más entradas
- Volumen de movimientos por producto
- Estadísticas de suministros
- Movimientos mensuales
- Distribución por categorías
- Generación de reportes en PDF

### 🛡️ Seguridad y Configuración
- Protección CORS para frontend separado
- Configuración de variables de entorno
- Soporte para múltiples bases de datos (SQLite, PostgreSQL)
- Cache con Redis
- Deploy en Render.com

## Instalación

1. Clona el repositorio:
   ```bash
   git clone <url-del-repo>
   cd PICM-DJANGO-REST
   ```
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Realiza migraciones:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Crea un superusuario:
   ```bash
   python manage.py createsuperuser
   ```
5. Ejecuta el servidor:
   ```bash
   python manage.py runserver
   ```

## 📋 Endpoints de la API

### 🔐 Autenticación (`/api/auth/`)
- `POST /api/auth/login` — Login de usuario (obtiene JWT token)
- `POST /api/auth/refresh-token` — Renovar token de acceso
- `POST /api/auth/password-reset` — Solicitud de recuperación de contraseña

### 📦 Productos (`/api/products/`)
- `GET /api/products/get` — Listado de productos (paginado, con filtros)
- `GET /api/products/get/<id>` — Obtener producto por ID
- `GET /api/products/get-products-name` — Obtener nombres de productos
- `POST /api/products/create` — Crear nuevo producto
- `PUT /api/products/update/<id>` — Actualizar producto
- `PUT /api/products/update-stock/<id>` — Actualizar stock de producto
- `DELETE /api/products/delete/<id>` — Eliminar producto
- `GET /api/products/total-stock` — Obtener stock total
- `GET /api/products/total-stock-value` — Obtener valor total del inventario

#### Categorías de Productos
- `GET /api/products/get-categories` — Listado de categorías activas
- `GET /api/products/get-categories-all` — Listado de todas las categorías
- `GET /api/products/get-category/<id>` — Obtener categoría por ID
- `POST /api/products/create-category` — Crear nueva categoría
- `PUT /api/products/update-category/<id>` — Actualizar categoría
- `DELETE /api/products/delete-category/<id>` — Eliminar categoría

### 🏭 Suministros (`/api/supplies/`)
- `GET /api/supplies/get-paginated` — Listado de suministros (paginado)
- `GET /api/supplies/get/<id>` — Obtener suministro por ID
- `GET /api/supplies/get-supplies-name` — Obtener nombres de suministros
- `POST /api/supplies/create` — Crear nuevo suministro
- `PUT /api/supplies/update/<id>` — Actualizar suministro
- `PUT /api/supplies/update-stock/<id>` — Actualizar stock de suministro
- `DELETE /api/supplies/delete/<id>` — Eliminar suministro
- `GET /api/supplies/total-stock` — Obtener stock total de suministros
- `GET /api/supplies/total-inventory-value` — Obtener valor total del inventario

#### Proveedores
- `GET /api/supplies/get-suppliers` — Listado de proveedores
- `GET /api/supplies/get-suppliers-paginated` — Listado de proveedores (paginado)
- `GET /api/supplies/get-supplier/<id>` — Obtener proveedor por ID
- `POST /api/supplies/create-supplier` — Crear nuevo proveedor
- `PUT /api/supplies/update-supplier/<id>` — Actualizar proveedor
- `DELETE /api/supplies/delete-supplier/<id>` — Eliminar proveedor

### 📊 Movimientos (`/api/movements/`)
- `GET /api/movements/get-movements` — Listado de movimientos
- `GET /api/movements/get-movement/<id>/<tipo>` — Obtener movimiento por ID y tipo
- `POST /api/movements/create-movement/<tipo>` — Crear nuevo movimiento
- `PUT /api/movements/update-movement/<id>/<tipo>` — Actualizar movimiento
- `DELETE /api/movements/delete-movement/<id>/<tipo>` — Eliminar movimiento

### 📈 Estadísticas (`/api/statistics/`)
#### Estadísticas de Productos
- `GET /api/statistics/top-products-sales/` — Productos más vendidos
- `GET /api/statistics/top-products-entries/` — Productos con más entradas
- `GET /api/statistics/product-movements-volume/` — Volumen de movimientos por producto

#### Estadísticas de Suministros
- `GET /api/statistics/top-supplies-sales/` — Suministros más vendidos
- `GET /api/statistics/top-supplies-entries/` — Suministros con más entradas
- `GET /api/statistics/supply-movements-volume/` — Volumen de movimientos por suministro

#### Estadísticas Generales
- `GET /api/statistics/monthly-movements/` — Movimientos mensuales
- `GET /api/statistics/category-distribution/` — Distribución por categorías

### 📄 Reportes (`/api/reports/`)
- `GET /api/reports/product_movements_pdf` — Descargar reporte de movimientos de productos (PDF)
- `GET /api/reports/download-product-report/<id>` — Descargar reporte de producto específico
- `GET /api/reports/download-supply-report/<id>` — Descargar reporte de suministro específico

## 🛠️ Tecnologías y Dependencias

### Backend
- **Django 5.2.6** — Framework web principal
- **Django REST Framework 3.16.1** — API REST
- **djangorestframework-simplejwt 5.3.1** — Autenticación JWT
- **django-cors-headers 4.0.0** — Configuración CORS
- **python-dotenv 1.1.0** — Gestión de variables de entorno

### Base de Datos y Cache
- **psycopg2-binary 2.9.7** — Adaptador PostgreSQL
- **django-redis 5.4.0** — Cache con Redis
- **SQLite** — Base de datos por defecto (desarrollo)

### Despliegue y Producción
- **gunicorn 20.1.0** — Servidor WSGI
- **whitenoise 6.5.0** — Servir archivos estáticos
- **pytz 2023.3** — Manejo de zonas horarias

## ⚙️ Configuración

### Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Base de datos
DATABASE_URL=postgresql://user:password@localhost:5432/picm_db

# Email (para recuperación de contraseñas)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password

# Redis (para cache)
REDIS_URL=redis://localhost:6379/1

# Django
SECRET_KEY=tu-secret-key-super-segura
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,tu-dominio.com

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Configuración de Email
Para desarrollo, puedes usar el backend de consola:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Para producción, configura SMTP:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```

## 🚀 Despliegue

### Render.com
El proyecto incluye configuración para despliegue en Render.com:

1. **render.yaml** — Configuración de servicios
2. **build.sh** — Script de construcción
3. **prod.env** — Variables de entorno de producción

### Comandos de Despliegue
```bash
# Construcción
./build.sh

# Migraciones en producción
python manage.py migrate

# Recopilar archivos estáticos
python manage.py collectstatic --noinput
```

## 📱 Uso con Frontend

### CORS Configuration
La API está configurada para trabajar con frontends separados:
- **Vite/React** — `http://localhost:5173`
- **Next.js** — `http://localhost:3000`
- **Vue.js** — `http://localhost:8080`

### Autenticación JWT
```javascript
// Ejemplo de uso en frontend
const login = async (credentials) => {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials)
  });
  const data = await response.json();
  localStorage.setItem('access_token', data.access);
  localStorage.setItem('refresh_token', data.refresh);
};
```

## 📊 Estructura del Proyecto

```
picm_rest/
├── products/          # Gestión de productos y categorías
├── supplies/          # Gestión de suministros y proveedores
├── movements/         # Registro de movimientos
├── stats/            # Estadísticas y análisis
├── reports/          # Generación de reportes PDF
├── users/            # Autenticación y usuarios
├── picm_rest/        # Configuración principal
├── requirements.txt  # Dependencias
├── render.yaml       # Configuración de despliegue
└── build.sh         # Script de construcción
```

## 🔧 Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Cargar datos de prueba
python manage.py loaddata fixtures/initial_data.json

# Ejecutar tests
python manage.py test

# Recopilar archivos estáticos
python manage.py collectstatic
```

## 📝 Notas de Desarrollo

- El frontend puede estar en cualquier tecnología (Vite, React, Vue, Angular, etc.)
- La API devuelve respuestas en formato JSON
- Todos los endpoints requieren autenticación JWT (excepto login)
- La paginación está configurada con 10 elementos por página por defecto
- Los reportes se generan en formato PDF usando la librería integrada

---

**Desarrollado por:** _kew1n  
**Versión:** 1.5.0  
**Licencia:** MIT
