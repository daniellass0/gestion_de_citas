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