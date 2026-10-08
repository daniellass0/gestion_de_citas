CREATE TABLE IF NOT EXISTS pagos (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  cita_id     INT NOT NULL,          -- referencia lógica al servicio Citas
  paciente_id INT NOT NULL,          -- referencia lógica al servicio Usuarios
  monto       DECIMAL(10,2) NOT NULL,
  metodo      ENUM('tarjeta','transferencia','efectivo') NOT NULL DEFAULT 'tarjeta',
  estado      ENUM('aprobado','rechazado','pendiente') NOT NULL,
  creado_en   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_cita (cita_id)
);
