# gestion_de_citas

# Arquitectura del sistema: Sistema de Gestion de citas medicas
## Problema que resuelve 

    Actualmente el consultorio agenda las citas de forma manual llamadas telefonicas o agenda fisica

    Es comun que se presenten cruces de horarios, citas duplicadas, olvidos de parte de los pacientes o incluso errores al registrar la informacion. Ademas, gran parte del tiempo del personal se destina a tareas repetitivas como confirmar citas, reorganizar horarios o responder consultas sobre disponibilidad.

    Para solucionar estos inconvenientes, se propone un sistema de gestion de citas medicas que centralice toda la informacion en una unica plataforma.

 ## Servicios del sistema 

 1. usuarios 
 2. autenticacion 
 3. citas 
 4. notificaciones
 5. Pagos

## Comunicacion entre servicios 
1. Que servicio necesita informacion de otro?
Citas necesita datos de Usuarios para validar al paciente y al medico y de Autenticacion para confirmar que quien agenda esta autorizado.

2. Quien solicita datos?
Citas es el servicio que mas solicita informacion a los demas servicios.

3. Quien responde? 
Usuarios, Autenticacion y Pagos responden confirmando o negando la informacion solicitada.


## Arquitectura del Sistema

Para este proyecto hemos seleccionado una arquitectura basada en Microservicios. 


## Bases de Datos y Gestion de la Informacion

### Entidades Principales
El sistema maneja los siguientes datos fundamentales:
* **Usuarios:** Pacientes (nombre, documento, contacto), medicos (especialidad, horario) y administrativos.
* **Citas:** Agenda (fecha, hora) y estado de la cita.
* **Historial Clinico:** Registro de la atencion medica.
* **Pagos:** Registro de transacciones.

### Datos Criticos y Gestion de Riesgos
Los datos mas sensibles y criticos para la operacion son la **programacion de citas** y los **datos de identificacion/contacto** de los pacientes. 

La perdida de esta informacion es inaceptable, ya que implicaria:
* Perdida de la trazabilidad de citas e historial medico.
* Cruces de horarios y caos administrativo.
* Perdida de confianza por parte de los pacientes.
* Posibles implicaciones legales, al tratarse de informacion medica confidencial.


## usuarios del sistema
 -paciente
 -medico
 -administrador
 -administrador del sistema

## riesgos y fallas posibles 
    -Servicio de pagos: no se podrian procesar cobros en linea; la cita quedaria en estado "pendiente de pago" en lugar de bloquear el agendamiento, permitiendo pagar luego en el consultorio.
    -Base de datos: se perderia el acceso a citas, historiales y datos de usuarios; el
    sistema no podria registrar ni consultar informacion nueva hasta restaurar el
    servicio.
    -Servidor principal: todo el sistema quedaria fuera de linea: ni pacientes ni
    personal podrian agendar, consultar o cancelar citas, obligando a volver
    temporalmente a metodos manuales.