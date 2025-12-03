# Sistema de Gestión de Equipos de TI - Universidad

## 📋 Descripción
Sistema integral para la gestión de equipos de tecnología en universidades públicas, implementado con arquitectura de microservicios. Este sistema permite administrar el ciclo de vida completo de los activos de TI, desde su adquisición hasta su baja, incluyendo mantenimiento, ubicación y proveedores.

## 🏗️ Arquitectura

### Microservicios
- **API Gateway** (Puerto 8000): Punto de entrada único, enrutamiento y orquestación.
- **Equipos Service** (Puerto 8001): Gestión de inventario, categorías y ubicaciones.
- **Proveedores Service** (Puerto 8002): Gestión de proveedores y contratos.
- **Mantenimiento Service** (Puerto 8003): Gestión de mantenimientos preventivos y correctivos.
- **Reportes Service** (Puerto 8004): Generación de dashboards y reportes (PDF/Excel).
- **Agent Service** (Puerto 8005): Agentes inteligentes para tareas en segundo plano (alertas, recordatorios).
- **Frontend Streamlit** (Puerto 8501): Interfaz de usuario interactiva.
- **PostgreSQL** (Puerto 5432): Base de datos relacional centralizada.

## 🚀 Instalación y Despliegue

### Prerrequisitos
- Docker Desktop 20.10+
- Docker Compose 2.0+
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd examenu3
   ```

2. **Construir y levantar servicios**
   ```bash
   docker-compose build
   docker-compose up -d
   ```

3. **Inicialización de Base de Datos**
   El sistema está configurado para **inicializarse automáticamente**. 
   - Al iniciar el contenedor `api-gateway`, este ejecutará automáticamente los scripts de creación de tablas (`schema.sql`) y carga de datos de prueba (`seeds.sql`).
   - No es necesario ejecutar comandos manuales de inicialización.

4. **Acceder a la aplicación**
   - **Frontend:** http://localhost:8501
   - **API Gateway Docs:** http://localhost:8000/docs

## 📊 Estructura del Proyecto

```
examenu3/
├── frontend/                 # Interfaz de usuario (Streamlit)
│   ├── app.py               # Punto de entrada
│   ├── pages/               # Páginas de la aplicación
│   └── requirements.txt
├── services/                 # Microservicios (FastAPI)
│   ├── api_gateway/
│   ├── equipos_service/
│   ├── proveedores_service/
│   ├── mantenimiento_service/
│   ├── reportes_service/
│   └── agent_service/
├── database/                 # Scripts SQL
│   ├── schema.sql           # Estructura de la BD
│   └── seeds.sql            # Datos de prueba
├── scripts/                  # Scripts de utilidad (Python)
├── docker-compose.yml        # Orquestación de contenedores
└── README.md
```

## 🔧 Funcionalidades

### 1. Gestión de Proveedores
- ✅ Registro y actualización de proveedores.
- ✅ Gestión de contratos y documentos.
- ✅ Historial de compras asociadas.

### 2. Gestión de Equipos
- ✅ Inventario detallado con especificaciones técnicas.
- ✅ Control de ubicaciones y movimientos.
- ✅ Trazabilidad de estados (Operativo, En Reparación, Obsoleto).
- ✅ Asignación a usuarios responsables.

### 3. Gestión de Mantenimiento
- ✅ Registro de mantenimientos preventivos y correctivos.
- ✅ Control de costos y tiempos de reparación.
- ✅ Historial completo por equipo.

### 4. Reportes y Análisis
- ✅ Dashboard interactivo con KPIs en tiempo real.
- ✅ Gráficos de distribución por estado, ubicación y categoría.
- ✅ Exportación de reportes a Excel y PDF.

### 5. Agentes Inteligentes (Automatización)
- ✅ **Recordatorios de Mantenimiento:** Alertas automáticas 7 días antes.
- ✅ **Control de Obsolescencia:** Detección de equipos que superaron su vida útil.
- ✅ **Vencimiento de Garantías:** Notificaciones preventivas.
- ✅ **Análisis de Costos:** Alerta sobre equipos con costos de reparación excesivos (>50% valor compra).

### 🚀 Próximamente
- 💡 **Análisis Predictivo:** Modelos de ML para predecir fallos de hardware.
- 📈 **Tendencias:** Proyección de gastos futuros.

## 🔐 Seguridad
- Arquitectura de red aislada (Bridge Network).
- Base de datos no expuesta directamente a internet (solo a través de servicios).
- Variables de entorno para configuración sensible.

## 🛠️ Solución de Problemas

Si la base de datos no se inicializa correctamente (ej. tablas vacías):

1. Verificar logs del api-gateway:
   ```bash
   docker-compose logs api-gateway
   ```
2. Ejecutar script de carga manual (requiere Python local):
   ```bash
   pip install asyncpg
   python scripts/seed_db.py
   ```

## 👥 Equipo de Desarrollo
Examen Unidad III - Ingeniería de Software
