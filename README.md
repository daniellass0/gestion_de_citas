# gestion_de_citas

## Problema que resuelve

Actualmente el consultorio agenda las citas de forma manual (llamadas telefónicas o agenda física), lo que genera cruces de horario, citas duplicadas, olvidos y errores al registrar información. Este sistema centraliza el agendamiento, la confirmación y el recordatorio de citas médicas en una sola plataforma.

## Servicios del sistema

1. Usuarios
2. Autenticación
3. Citas
4. Notificaciones
5. Pagos

## Arquitectura

El sistema está basado en **microservicios**, porque cada servicio (usuarios, autenticación, citas, notificaciones y pagos) tiene una responsabilidad distinta y puede desarrollarse, desplegarse y escalarse por separado.

El servicio de **Citas** es el que más se comunica con los demás, ya que necesita validar al paciente, al médico, la sesión y el pago antes de confirmar una cita.

El diagrama completo, la definición de cada servicio y la tabla de comunicación entre servicios están en [`docs/arquitectura/arquitectura.md`](docs/arquitectura/arquitectura.md).

## Bases de datos y gestión de la información

* **Usuarios:** pacientes (nombre, documento, contacto), médicos (especialidad, horario) y administrativos.
* **Citas:** fecha, hora y estado de la cita.
* **Pagos:** registro de transacciones.

Cada servicio maneja su propia base de datos, siguiendo el enfoque de microservicios.

## Usuarios del sistema

- Paciente
- Médico
- Administrador

## Riesgos y posibles fallas

- **Servicio de pagos:** no se podrían procesar cobros en línea; la cita quedaría en estado "pendiente de pago" en vez de bloquear el agendamiento.
- **Base de datos:** se perdería el acceso a citas, historiales y datos de usuarios hasta restaurar el servicio.
- **Servidor principal:** todo el sistema quedaría fuera de línea, obligando a volver temporalmente a métodos manuales.

## Docker

Actualmente el componente **Home** está contenerizado y funcionando. Los demás servicios están definidos en `docker-compose.yml`, pendientes de implementar su lógica.

## Docker Compose

Para levantar el proyecto:

```bash
docker compose up --build
```

## Estado actual

- **Implementado:** vista Home, ejecutándose en un contenedor.
- **Definido, pendiente de lógica:** Usuarios, Autenticación, Citas, Notificaciones, Pagos.
- **Pendiente:** login real, base de datos funcional, pagos reales, notificaciones reales.
