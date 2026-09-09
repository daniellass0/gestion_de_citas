# gestion_de_citas

## Problema que resuelve

Actualmente el consultorio agenda las citas de forma manual (llamadas telefónicas o agenda física), lo que genera cruces de horario, citas duplicadas, olvidos y errores al registrar información. Este sistema centraliza el agendamiento, la confirmación y el recordatorio de citas médicas en una sola plataforma.

## Servicios del sistema

1. Usuarios
2. Autenticación
3. Citas
4. Notificaciones
5. Pagos

## Comunicación entre servicios

1. Qué servicio necesita información de otro
Citas necesita datos de Usuarios para validar al paciente y al médico y de Autenticación para confirmar que quien agenda está autorizado.

2. Quién solicita datos
Citas es el servicio que más solicita información a los demás servicios.

3. Quién responde
Usuarios, Autenticación y Pagos responden confirmando o negando la información solicitada.

## Arquitectura del sistema

Para este proyecto se seleccionó una arquitectura basada en **microservicios**, porque cada servicio (usuarios, autenticación, citas, notificaciones y pagos) tiene una responsabilidad distinta y puede desarrollarse, desplegarse y escalarse por separado. El servicio de **Citas** actúa como orquestador principal, ya que es el que más solicita información a los demás servicios para validar y completar una cita.

![Diagrama de arquitectura](docs/img/arquitectura.png)

## Bases de datos y gestión de la información

### Entidades principales
El sistema maneja los siguientes datos fundamentales:
* Usuarios: pacientes (nombre, documento, contacto), médicos (especialidad, horario) y administrativos.
* Citas: agenda (fecha, hora) y estado de la cita.
* Pagos: registro de transacciones.

## Usuarios del sistema
- Paciente
- Médico
- Administrador
- Administrador del sistema

## Riesgos y fallas posibles
- Servicio de pagos: no se podrían procesar cobros en línea; la cita quedaría en estado "pendiente de pago" en lugar de bloquear el agendamiento, permitiendo pagar luego en el consultorio.
- Base de datos: se perdería el acceso a citas, historiales y datos de usuarios; el sistema no podría registrar ni consultar información nueva hasta restaurar el servicio.
- Servidor principal: todo el sistema quedaría fuera de línea: ni pacientes ni personal podrían agendar, consultar o cancelar citas, obligando a volver temporalmente a métodos manuales.
