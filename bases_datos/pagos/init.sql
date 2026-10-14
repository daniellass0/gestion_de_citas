CREATE TABLE IF NOT EXISTS pagos (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id INT NOT NULL,
  monto      DECIMAL(10,2) NOT NULL,
  metodo     ENUM('efectivo','tarjeta','transferencia') NOT NULL,
  estado     ENUM('pendiente','pagado','cancelado') NOT NULL DEFAULT 'pendiente',
  concepto   VARCHAR(150),
  fecha      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO pagos (usuario_id, monto, metodo, estado, concepto) VALUES
(1, 80000.00,  'tarjeta',       'pagado',    'Consulta cardiología'),
(1, 45000.00,  'efectivo',      'pendiente', 'Examen de laboratorio'),
(2, 60000.00,  'transferencia', 'pagado',    'Consulta medicina general'),
(2, 120000.00, 'tarjeta',       'cancelado', 'Electrocardiograma');