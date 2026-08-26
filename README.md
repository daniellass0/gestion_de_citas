# gestion_de_citas

# Arquitectura del sistema: Sistema de Gestion de citas de un consultorio

## Problema que resuelve 

 Actualmente el consultorio agenda las citas de forma manual llamadas telefonicas o agenda fisica, lo que genera cruces de horario, citas duplicadas, olvidos y perdida de tiempo para pacientes y personal administrativo. El sistema centraliza y automatiza el agendamiento, la confirmacion y el recordatorio de citas medica

 ## Servicios del sistema 

 1. usuarios 
 2. autenticacion 
 3. citas 
 4. notificaciones  
 5. historial clinico
 6. Pagos

## Conexion entre servicios 

- Que servicio necesita informacion de otro?
Citas necesita datos de Usuarios para validar al paciente y al medico y de Autenticacion para confirmar que quien agenda esta autorizado.

- Quien solicita datos?
Citas es el servicio que mas solicita informacion a los demas servicios.

- Quien responde? 
Usuarios, Autenticacion y Pagos responden confirmando o negando la informacion solicitada.


## Tipo de arquitectura 

- Microservicios 

- Cuantos usuarios tendra el sistema? 
Un numero moderado: los pacientes del consultorio, pocos medicos y un equipo administrativo pequeno, con posibilidad de crecer si el consultorio abre nuevas sedes.

- Necesita escalar? 
No de forma masiva a corto plazo, pero el diseno debe permitirlo sin tener que reescribir el sistema completo.

- Es un sistema pequeno o grande? 
Actualmente es un sistema pequeno-mediano.

## Arquitectura del Sistema

Para este proyecto hemos seleccionado una arquitectura basada en **Microservicios**. 

### Contexto del Sistema
* **Usuarios estimados:** Un numero moderado (pacientes del consultorio, cuerpo medico y un equipo administrativo pequeno), con posibilidad de crecimiento si se abren nuevas sedes.
* **Escalabilidad:** Aunque no se requiere un escalado masivo a corto plazo, el diseno permite el crecimiento sin necesidad de reescribir el sistema completo.
* **Tamano actual:** Sistema de tamano pequeno-mediano.

### Justificacion de la Arquitectura
Se eligio el enfoque de microservicios porque cada funcion principal del sistema tiene responsabilidades y ciclos de vida distintos:
* Usuarios
* Citas
* Notificaciones
* Historial Clinico
* Pagos

Separar estas funciones en servicios independientes garantiza que una falla en uno (por ejemplo, *Notificaciones*) no afecte la disponibilidad de los demas. Ademas, permite que servicios con mayor demanda (como *Citas* en horas pico) puedan escalar de forma independiente. Aunque el consultorio es pequeno hoy, esta separacion tecnica facilita su crecimiento futuro y permite actualizaciones sin redisenar el sistema desde cero.

---

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

### Arquitectura de Datos (Database-per-service)
Acorde a nuestra arquitectura, **cada microservicio maneja su propia base de datos** (Base de datos para Usuarios, para Citas, para Historial Clinico, etc.). 

Esto evita que la caida de una base de datos afecte a todo el sistema simultaneamente. La informacion entre los distintos servicios se coordina y relaciona mediante identificadores compartidos (como el `ID` del paciente) y la comunicacion se realiza de forma segura a traves de APIs, evitando consultas directas (queries cruzadas) entre las bases de datos de diferentes servicios.

## usuarios del sistema
 -paciente
 -medico
 -administrador

## riesgos y fallas posibles 
    -Servicio de pagos: no se podrian procesar cobros en linea; la cita quedaria en estado "pendiente de pago" en lugar de bloquear el agendamiento, permitiendo pagar luego en el consultorio.
    -Base de datos: se perderia el acceso a citas, historiales y datos de usuarios; el
    sistema no podria registrar ni consultar informacion nueva hasta restaurar el
    servicio.
    -Servidor principal: todo el sistema quedaria fuera de linea: ni pacientes ni
    personal podrian agendar, consultar o cancelar citas, obligando a volver
    temporalmente a metodos manuales.