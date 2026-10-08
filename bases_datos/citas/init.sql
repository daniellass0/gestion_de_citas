CREATE TABLE IF NOT EXISTS citas (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  paciente_id INT NOT NULL,          -- referencia lógica al servicio Usuarios
  medico_id   INT NOT NULL,          -- referencia lógica al servicio Usuarios
  fecha       DATE NOT NULL,
  hora        TIME NOT NULL,
  motivo      VARCHAR(255),
  valor       DECIMAL(10,2) NOT NULL,
  estado      ENUM('pendiente_pago','confirmada','cancelada','completada') NOT NULL DEFAULT 'pendiente_pago',
  pago_id     INT NULL,              -- referencia lógica al servicio Pagos
  creado_en   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_medico_fecha (medico_id, fecha, hora),
  INDEX idx_paciente (paciente_id)
);
