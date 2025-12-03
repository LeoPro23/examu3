-- Seed data for IT Management System

-- Usuarios adicionales
INSERT INTO usuarios (username, email, password_hash, rol, nombre_completo) VALUES 
('tecnico1', 'tecnico1@universidad.edu', 'hashed_password', 'tecnico', 'Juan Técnico'),
('tecnico2', 'tecnico2@universidad.edu', 'hashed_password', 'tecnico', 'Maria Soporte'),
('usuario1', 'usuario1@universidad.edu', 'hashed_password', 'usuario', 'Pedro Profesor'),
('usuario2', 'usuario2@universidad.edu', 'hashed_password', 'usuario', 'Ana Administrativa')
ON CONFLICT (username) DO NOTHING;

-- Categorías adicionales
INSERT INTO categorias_equipos (nombre, descripcion, vida_util_anos) VALUES 
('Proyectores', 'Proyectores multimedia y ecran', 5),
('Servidores', 'Servidores rack y torre', 4),
('Tablets', 'Tablets para uso académico', 3)
ON CONFLICT (nombre) DO NOTHING;

-- Ubicaciones adicionales
INSERT INTO ubicaciones (edificio, aula_oficina, descripcion) VALUES 
('Edificio A', 'Aula 102', 'Aula teórica'),
('Edificio B', 'Biblioteca', 'Sala de cómputo biblioteca'),
('Edificio C', 'Auditorio', 'Auditorio principal'),
('Edificio C', 'Almacén TI', 'Almacén principal de equipos')
ON CONFLICT DO NOTHING;

-- Proveedores
INSERT INTO proveedores (razon_social, ruc, direccion, telefono, email, contacto_nombre, contacto_telefono, sitio_web, calificacion, notas) VALUES 
('Tecnología Global S.A.C.', '20123456789', 'Av. Javier Prado 1234, Lima', '01-222-3333', 'ventas@tecglobal.com', 'Carlos Vendedor', '999888777', 'www.tecglobal.com', 4.5, 'Proveedor principal de PCs'),
('Redes y Soluciones E.I.R.L.', '20987654321', 'Jr. Los Pinos 456, Lima', '01-444-5555', 'contacto@redesysol.com', 'Luis Redes', '987654321', 'www.redesysol.com', 4.0, 'Especialistas en cableado'),
('Importaciones Tech', '20555666777', 'Calle Las Begonias 789, Lima', '01-666-7777', 'info@importtech.pe', 'Ana Importadora', '955444333', 'www.importtech.pe', 3.8, 'Buenos precios en periféricos');

-- Contratos
INSERT INTO contratos (proveedor_id, numero_contrato, tipo, fecha_inicio, fecha_fin, monto_total, estado, descripcion) VALUES 
((SELECT id FROM proveedores WHERE ruc='20123456789'), 'CTR-2024-001', 'Adquisición', '2024-01-15', '2024-12-31', 50000.00, 'vigente', 'Compra anual de computadoras'),
((SELECT id FROM proveedores WHERE ruc='20987654321'), 'CTR-2024-002', 'Mantenimiento', '2024-02-01', '2025-01-31', 12000.00, 'vigente', 'Mantenimiento preventivo de red');

-- Equipos
-- PCs
INSERT INTO equipos (codigo_inventario, categoria_id, nombre, marca, modelo, numero_serie, proveedor_id, fecha_compra, costo_compra, fecha_garantia_fin, ubicacion_actual_id, estado_operativo, estado_fisico, asignado_a_id) VALUES 
('PC-001', (SELECT id FROM categorias_equipos WHERE nombre='Computadoras'), 'PC Laboratorio 01', 'Dell', 'Optiplex 7090', 'SERIE-001', (SELECT id FROM proveedores WHERE ruc='20123456789'), '2024-01-20', 1200.00, '2027-01-20', (SELECT id FROM ubicaciones WHERE aula_oficina='Lab 101'), 'operativo', 'excelente', NULL),
('PC-002', (SELECT id FROM categorias_equipos WHERE nombre='Computadoras'), 'PC Laboratorio 02', 'Dell', 'Optiplex 7090', 'SERIE-002', (SELECT id FROM proveedores WHERE ruc='20123456789'), '2024-01-20', 1200.00, '2027-01-20', (SELECT id FROM ubicaciones WHERE aula_oficina='Lab 101'), 'operativo', 'excelente', NULL),
('PC-003', (SELECT id FROM categorias_equipos WHERE nombre='Computadoras'), 'PC Laboratorio 03', 'Dell', 'Optiplex 7090', 'SERIE-003', (SELECT id FROM proveedores WHERE ruc='20123456789'), '2024-01-20', 1200.00, '2027-01-20', (SELECT id FROM ubicaciones WHERE aula_oficina='Lab 101'), 'en_reparacion', 'bueno', NULL),
('LAP-001', (SELECT id FROM categorias_equipos WHERE nombre='Computadoras'), 'Laptop Administrativa', 'Lenovo', 'ThinkPad T14', 'SERIE-LAP-01', (SELECT id FROM proveedores WHERE ruc='20123456789'), '2023-05-10', 1500.00, '2026-05-10', (SELECT id FROM ubicaciones WHERE aula_oficina='Oficina TI'), 'operativo', 'bueno', (SELECT id FROM usuarios WHERE username='usuario2'));

-- Impresoras
INSERT INTO equipos (codigo_inventario, categoria_id, nombre, marca, modelo, numero_serie, proveedor_id, fecha_compra, costo_compra, fecha_garantia_fin, ubicacion_actual_id, estado_operativo, estado_fisico) VALUES 
('IMP-001', (SELECT id FROM categorias_equipos WHERE nombre='Impresoras'), 'Impresora Secretaría', 'HP', 'LaserJet Pro', 'SERIE-IMP-01', (SELECT id FROM proveedores WHERE ruc='20555666777'), '2023-02-15', 400.00, '2024-02-15', (SELECT id FROM ubicaciones WHERE aula_oficina='Oficina TI'), 'operativo', 'regular');

-- Proyectores
INSERT INTO equipos (codigo_inventario, categoria_id, nombre, marca, modelo, numero_serie, proveedor_id, fecha_compra, costo_compra, fecha_garantia_fin, ubicacion_actual_id, estado_operativo, estado_fisico) VALUES 
('PRJ-001', (SELECT id FROM categorias_equipos WHERE nombre='Proyectores'), 'Proyector Auditorio', 'Epson', 'PowerLite', 'SERIE-PRJ-01', (SELECT id FROM proveedores WHERE ruc='20555666777'), '2022-08-20', 800.00, '2024-08-20', (SELECT id FROM ubicaciones WHERE aula_oficina='Auditorio'), 'obsoleto', 'malo');

-- Mantenimientos
INSERT INTO mantenimientos (equipo_id, tipo, fecha_programada, fecha_realizada, tecnico_id, proveedor_id, descripcion, problema_reportado, solucion_aplicada, costo, estado, prioridad) VALUES 
((SELECT id FROM equipos WHERE codigo_inventario='PC-003'), 'correctivo', '2024-11-01', '2024-11-02', (SELECT id FROM usuarios WHERE username='tecnico1'), NULL, 'Falla de disco duro', 'PC no inicia', 'Cambio de HDD por SSD', 80.00, 'completado', 'alta'),
((SELECT id FROM equipos WHERE codigo_inventario='IMP-001'), 'preventivo', '2024-12-15', NULL, NULL, (SELECT id FROM proveedores WHERE ruc='20555666777'), 'Limpieza general y cambio de toner', NULL, NULL, 0.00, 'programado', 'media'),
((SELECT id FROM equipos WHERE codigo_inventario='PRJ-001'), 'correctivo', '2024-10-10', '2024-10-12', (SELECT id FROM usuarios WHERE username='tecnico2'), NULL, 'Cambio de lámpara', 'Imagen oscura', 'Reemplazo de lámpara', 150.00, 'completado', 'media');

-- Movimientos
INSERT INTO movimientos_equipos (equipo_id, ubicacion_origen_id, ubicacion_destino_id, usuario_responsable_id, motivo, observaciones) VALUES 
((SELECT id FROM equipos WHERE codigo_inventario='PC-003'), (SELECT id FROM ubicaciones WHERE aula_oficina='Lab 101'), (SELECT id FROM ubicaciones WHERE aula_oficina='Oficina TI'), (SELECT id FROM usuarios WHERE username='tecnico1'), 'Reparación', 'Se lleva a taller para cambio de disco'),
((SELECT id FROM equipos WHERE codigo_inventario='PC-003'), (SELECT id FROM ubicaciones WHERE aula_oficina='Oficina TI'), (SELECT id FROM ubicaciones WHERE aula_oficina='Lab 101'), (SELECT id FROM usuarios WHERE username='tecnico1'), 'Retorno', 'Equipo reparado y devuelto');
