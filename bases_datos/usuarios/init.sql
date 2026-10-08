CREATE TABLE IF NOT EXISTS usuarios (
  id           INT AUTO_INCREMENT PRIMARY KEY,
  nombre       VARCHAR(100) NOT NULL,
  documento    VARCHAR(30)  NOT NULL UNIQUE,
  email        VARCHAR(120),
  telefono     VARCHAR(30),
  rol          ENUM('paciente','medico','administrador') NOT NULL,
  especialidad VARCHAR(80),
  horario      VARCHAR(80),
  creado_en    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO usuarios (nombre, documento, email, telefono, rol, especialidad, horario) VALUES
('Ana Torres',        '1001', 'ana@correo.com',    '3001112222', 'paciente',      NULL,              NULL),
('Carlos Pérez',      '1002', 'carlos@correo.com', '3003334444', 'paciente',      NULL,              NULL),
('Dra. Camila Rojas', '2001', 'camila@clinica.com','3005556666', 'medico',        'Cardiología',     'Lun-Vie 8:00-16:00'),
('Dr. Andrés Mora',   '2002', 'andres@clinica.com','3007778888', 'medico',        'Medicina general','Lun-Sab 7:00-13:00'),
('Laura Admin',       '3001', 'admin@clinica.com', '3009990000', 'administrador', NULL,              NULL);
