# Informe Técnico: Sistema de Gestión de Equipos de TI

## 1. Introducción

En el contexto de una universidad pública, la gestión eficiente de los recursos tecnológicos es crítica para garantizar la continuidad operativa académica y administrativa. El presente proyecto tiene como objetivo desarrollar e implementar una solución web integral para la administración del ciclo de vida de los equipos de TI.

La problemática abordada incluye la dispersión de la información de inventario, la falta de seguimiento en los mantenimientos preventivos y correctivos, y la dificultad para gestionar garantías y proveedores. Este sistema busca centralizar esta información, automatizar alertas mediante agentes inteligentes y proporcionar herramientas de análisis para la toma de decisiones.

## 2. Materiales y Métodos

### 2.1 Stack Tecnológico

Para el desarrollo de esta solución se seleccionó un stack tecnológico moderno, robusto y de código abierto, priorizando la escalabilidad y la facilidad de despliegue.

*   **Lenguaje de Programación:** Python 3.9+. Elegido por su versatilidad, amplio ecosistema de librerías y facilidad para implementar tanto lógica de backend como scripts de automatización.
*   **Frontend:** **Streamlit**. Framework que permite la creación rápida de aplicaciones web de datos interactivas utilizando solo Python, facilitando el desarrollo de dashboards y formularios sin necesidad de conocimientos profundos de HTML/CSS/JS.
*   **Backend:** **FastAPI**. Framework moderno y de alto rendimiento para la construcción de APIs. Se utilizó para desarrollar una arquitectura de microservicios, garantizando una comunicación eficiente y asíncrona.
*   **Base de Datos:** **PostgreSQL**. Sistema de gestión de bases de datos relacional objeto, seleccionado por su robustez, integridad de datos y soporte para consultas complejas.
*   **Orquestación y Contenedores:** **Docker** y **Docker Compose**. Utilizados para empaquetar cada microservicio y sus dependencias en contenedores aislados, asegurando la consistencia entre los entornos de desarrollo y producción.

### 2.2 Arquitectura del Sistema

Se implementó una **Arquitectura de Microservicios** para desacoplar las funcionalidades del sistema, permitiendo un mantenimiento y escalado independiente. Los componentes principales son:

1.  **API Gateway (Puerto 8000):** Punto de entrada único que gestiona el enrutamiento de solicitudes hacia los servicios correspondientes.
2.  **Microservicio de Equipos (Puerto 8001):** Gestiona el inventario, categorías, ubicaciones y movimientos de los activos.
3.  **Microservicio de Proveedores (Puerto 8002):** Administra la información de proveedores y contratos.
4.  **Microservicio de Mantenimiento (Puerto 8003):** Controla el registro de mantenimientos preventivos y correctivos.
5.  **Microservicio de Reportes (Puerto 8004):** Genera estadísticas y documentos exportables (PDF/Excel).
6.  **Agent Service (Puerto 8005):** Servicio de background que ejecuta tareas automatizadas.

### 2.3 Metodología de Desarrollo

El desarrollo siguió un enfoque iterativo e incremental. Se utilizaron prácticas de **DevOps** mediante la contenerización desde las etapas iniciales. La comunicación entre servicios se realiza vía HTTP (REST API). Se implementó el patrón de **Agentes Inteligentes** para la proactividad del sistema, donde procesos en segundo plano monitorean constantemente el estado de la base de datos para generar alertas.

## 3. Resultados

Se logró desarrollar y desplegar una aplicación web funcional que cumple con los requerimientos establecidos:

### 3.1 Módulos Funcionales
*   **Gestión de Inventario:** Permite el registro detallado de equipos (marca, modelo, serie, especificaciones), clasificación por categorías y asignación a ubicaciones físicas y usuarios responsables.
*   **Control de Mantenimiento:** Se implementó un flujo completo para registrar incidencias, programar mantenimientos y cerrar órdenes de servicio, manteniendo un historial de costos y acciones realizadas.
*   **Administración de Proveedores:** Base de datos centralizada de proveedores con historial de contratos y evaluaciones de desempeño.
*   **Dashboards y Reportes:** Visualización en tiempo real de métricas clave (KPIs) como disponibilidad de equipos, costos mensuales y distribución por estado. Capacidad de exportar reportes formales.

### 3.2 Automatización con Agentes
El sistema cuenta con 4 agentes inteligentes activos:
1.  **Agente de Mantenimiento:** Notifica automáticamente sobre mantenimientos programados próximos (7 días) o vencidos.
2.  **Agente de Obsolescencia:** Identifica equipos que han superado su vida útil contable o técnica.
3.  **Agente de Garantías:** Alerta 60 días antes del vencimiento de garantías de proveedores.
4.  **Agente de Costos:** Detecta anomalías financieras, como equipos cuyo costo de reparación acumulado supera el 50% de su valor de adquisición.

### 3.3 Despliegue
La aplicación fue desplegada exitosamente en un entorno de nube utilizando Docker Compose, demostrando la portabilidad de la solución. La base de datos PostgreSQL se expuso de manera segura para administración remota.

## 4. Conclusiones

1.  **Eficiencia Operativa:** La centralización de la información y la automatización de alertas reducen significativamente la carga administrativa y el riesgo de error humano en la gestión de activos de TI.
2.  **Escalabilidad:** La arquitectura de microservicios adoptada permite que el sistema crezca modularmente. Nuevos servicios pueden ser agregados sin afectar la estabilidad de los existentes.
3.  **Toma de Decisiones:** Los dashboards y reportes proporcionan a la dirección de TI datos concretos sobre costos y estado de la infraestructura, facilitando la planificación presupuestaria y la renovación tecnológica.
4.  **Robustez Tecnológica:** El uso de Docker y PostgreSQL garantiza un entorno estable, seguro y fácil de replicar o migrar en el futuro.

El sistema desarrollado satisface integralmente las necesidades de gestión de equipos de TI de la universidad, proporcionando una herramienta moderna y eficaz para la administración de recursos tecnológicos.
