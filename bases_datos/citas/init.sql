CREATE TABLE IF NOT EXISTS citas (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id INT NOT NULL,     
  fecha       DATE NOT NULL,
  hora        TIME NOT NULL,
  motivo      VARCHAR(255),
  estado      ENUM('pendiente_pago','confirmada','cancelada','completada') NOT NULL DEFAULT 'pendiente_pago',
<<<<<<< HEAD
  pago_id     INT NULL
);
=======
  pago_id     INT NULL,         
);
>>>>>>> main
