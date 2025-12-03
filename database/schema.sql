-- Schema for IT Management System

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL,
    nombre_completo VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultima_conexion TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categorias_equipos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    vida_util_anos INTEGER,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ubicaciones (
    id SERIAL PRIMARY KEY,
    edificio VARCHAR(50) NOT NULL,
    piso VARCHAR(20),
    aula_oficina VARCHAR(50) NOT NULL,
    descripcion TEXT,
    responsable_id INTEGER REFERENCES usuarios(id),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS proveedores (
    id SERIAL PRIMARY KEY,
    razon_social VARCHAR(100) NOT NULL,
    ruc VARCHAR(20) UNIQUE NOT NULL,
    direccion TEXT,
    telefono VARCHAR(20),
    email VARCHAR(100),
    contacto_nombre VARCHAR(100),
    contacto_telefono VARCHAR(20),
    sitio_web VARCHAR(100),
    calificacion DECIMAL(3,2),
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notas TEXT
);

CREATE TABLE IF NOT EXISTS contratos (
    id SERIAL PRIMARY KEY,
    proveedor_id INTEGER REFERENCES proveedores(id),
    numero_contrato VARCHAR(50) UNIQUE NOT NULL,
    tipo VARCHAR(50),
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    monto_total DECIMAL(12,2),
    estado VARCHAR(20),
    archivo_url VARCHAR(255),
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS equipos (
    id SERIAL PRIMARY KEY,
    codigo_inventario VARCHAR(50) UNIQUE NOT NULL,
    categoria_id INTEGER REFERENCES categorias_equipos(id),
    nombre VARCHAR(100) NOT NULL,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    numero_serie VARCHAR(100) UNIQUE,
    especificaciones JSONB,
    proveedor_id INTEGER REFERENCES proveedores(id),
    fecha_compra DATE,
    costo_compra DECIMAL(12,2),
    fecha_garantia_fin DATE,
    ubicacion_actual_id INTEGER REFERENCES ubicaciones(id),
    estado_operativo VARCHAR(20) DEFAULT 'operativo',
    estado_fisico VARCHAR(20) DEFAULT 'bueno',
    asignado_a_id INTEGER REFERENCES usuarios(id),
    notas TEXT,
    imagen_url VARCHAR(255),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS movimientos_equipos (
    id SERIAL PRIMARY KEY,
    equipo_id INTEGER REFERENCES equipos(id),
    ubicacion_origen_id INTEGER REFERENCES ubicaciones(id),
    ubicacion_destino_id INTEGER REFERENCES ubicaciones(id),
    usuario_responsable_id INTEGER REFERENCES usuarios(id),
    fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    motivo TEXT,
    observaciones TEXT
);

CREATE TABLE IF NOT EXISTS mantenimientos (
    id SERIAL PRIMARY KEY,
    equipo_id INTEGER REFERENCES equipos(id),
    tipo VARCHAR(20) NOT NULL, -- preventivo, correctivo
    fecha_programada DATE,
    fecha_realizada DATE,
    tecnico_id INTEGER REFERENCES usuarios(id),
    proveedor_id INTEGER REFERENCES proveedores(id),
    descripcion TEXT,
    problema_reportado TEXT,
    solucion_aplicada TEXT,
    costo DECIMAL(12,2),
    tiempo_fuera_servicio_horas DECIMAL(5,2),
    estado VARCHAR(20) DEFAULT 'programado',
    prioridad VARCHAR(20) DEFAULT 'media',
    partes_reemplazadas JSONB,
    observaciones TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS notificaciones (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50),
    titulo VARCHAR(100),
    mensaje TEXT,
    usuario_id INTEGER REFERENCES usuarios(id),
    equipo_id INTEGER REFERENCES equipos(id),
    mantenimiento_id INTEGER REFERENCES mantenimientos(id),
    leida BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_lectura TIMESTAMP
);

-- Insert initial data for testing
INSERT INTO usuarios (username, email, password_hash, rol, nombre_completo) VALUES 
('admin', 'admin@universidad.edu', 'hashed_password', 'admin', 'Administrador del Sistema');

INSERT INTO categorias_equipos (nombre, descripcion, vida_util_anos) VALUES 
('Computadoras', 'PCs de escritorio y laptops', 5),
('Impresoras', 'Impresoras láser y multifuncionales', 4),
('Redes', 'Routers, switches y access points', 7);

INSERT INTO ubicaciones (edificio, aula_oficina, descripcion) VALUES 
('Edificio A', 'Lab 101', 'Laboratorio de Computación 1'),
('Edificio B', 'Oficina TI', 'Oficina principal de TI');
