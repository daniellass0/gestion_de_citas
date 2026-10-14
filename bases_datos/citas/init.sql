CREATE TABLE IF NOT EXISTS citas (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id INT NOT NULL,
  fecha      DATE NOT NULL,
  hora       VARCHAR(5) NOT NULL,
  motivo     VARCHAR(150),
  estado     ENUM('pendiente_pago','confirmada','cancelada') NOT NULL DEFAULT 'pendiente_pago',
  pago_id    INT
);

INSERT INTO citas (usuario_id, fecha, hora, motivo, estado, pago_id) VALUES
(1, '2026-10-20', '09:00', 'Consulta cardiología',        'confirmada',     1),
(1, '2026-10-22', '10:30', 'Examen de laboratorio',       'pendiente_pago', 2),
(2, '2026-10-21', '08:00', 'Consulta medicina general',   'confirmada',     3),
(2, '2026-10-25', '11:00', 'Electrocardiograma',          'cancelada',      4);