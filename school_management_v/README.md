# Módulo de Gestión Educativa (School Management)

## Introducción

Este módulo para Odoo 16 proporciona una solución integral para la gestión de instituciones educativas. Permite administrar estudiantes, profesores, materias, inscripciones y el proceso de facturación asociado a través de contratos estudiantiles.

## Características Principales

*   **Gestión de Contactos:** Distingue entre Estudiantes y Profesores directamente en el modelo de Contactos de Odoo, añadiendo campos y vistas específicas.
*   **Administración de Materias:** Permite crear materias, asignarles un código único y asociar los profesores que pueden impartirlas.
*   **Horarios Flexibles:** Cada materia puede tener múltiples horarios disponibles, definidos por día de la semana, hora de inicio, hora de fin y el profesor a cargo.
*   **Proceso de Inscripción:** Flujo de trabajo completo para las inscripciones de los estudiantes, con estados (Borrador, Confirmado, Cancelado).
*   **Generación de Contratos:** A partir de una inscripción confirmada, se genera un contrato que detalla las materias inscritas y sus costos.
*   **Facturación Integrada:** Permite crear facturas de Odoo directamente desde los contratos estudiantiles, manteniendo un seguimiento del estado de pago.
*   **Consulta de Horarios:** Los estudiantes pueden consultar su horario de clases consolidado.
*   **Dashboard:** Incluye la base para un dashboard, con una implementación de ejemplo para incrustar un reporte externo (ej. Power BI).

## Modelos Principales

*   `res.partner`: Se extiende para añadir los roles de `Estudiante` (`is_student`) y `Profesor` (`is_teacher`).
*   `school.subject`: Almacena la información de las materias, incluyendo los profesores que la imparten y los horarios disponibles.
*   `school.enrollment`: Gestiona el proceso de inscripción de un estudiante a una materia y horario específico.
*   `school.contract`: Representa el acuerdo financiero con el estudiante. Agrupa las materias de una inscripción y calcula el monto total a pagar.
*   `school.student.schedule`: Modelo de solo lectura que muestra el horario final de un estudiante basado en sus inscripciones confirmadas.

## Configuración

Antes de utilizar el módulo, es necesario realizar la siguiente configuración:

1.  Vaya al menú **Educación -> Configuración**.
2.  **Crear Profesores:** Cree nuevos contactos (o edite existentes), marque la casilla **"Es Profesor"** y, en la pestaña "Educación", asigne las materias que puede impartir.
3.  **Crear Estudiantes:** Cree nuevos contactos (o edite existentes) y marque la casilla **"Es Estudiante"**.
4.  **Crear Materias:** Vaya a **Configuración -> Materias**. Cree las materias, asigne profesores y defina los horarios disponibles para cada una en la pestaña "Horarios Disponibles".

## Flujo de Trabajo (Uso)

El flujo de trabajo principal es el siguiente:

1.  **Crear una Inscripción:**
    *   Vaya a **Educación -> Inscripciones** y haga clic en "Crear".
    *   Seleccione el `Estudiante`.
    *   Seleccione el `Horario` deseado. El sistema completará automáticamente la `Materia` y el `Profesor` correspondientes.
    *   Guarde la inscripción. Estará en estado "Borrador".

2.  **Confirmar la Inscripción:**
    *   Abra la inscripción en estado "Borrador" y haga clic en el botón **"Confirmar"**.
    *   El estado cambiará a "Confirmado". En este punto, se crea automáticamente un `Contrato` y se genera el `Horario del Estudiante`.

3.  **Gestionar el Contrato y la Factura:**
    *   Desde la inscripción confirmada, puede acceder al contrato a través del botón inteligente **"Contratos"**.
    *   Abra el contrato. Verá las líneas con las materias y costos.
    *   Haga clic en **"Confirmar"** en el contrato.
    *   Una vez confirmado, haga clic en **"Crear Factura"** para generar la factura correspondiente en el módulo de Contabilidad.
    *   El estado del contrato y el estado de pago se actualizarán automáticamente a medida que la factura se procese y pague.

4.  **Consultar Horarios:**
    *   Vaya a **Educación -> Horarios de Estudiantes** para ver una lista de solo lectura de todos los horarios de clase de los estudiantes.

5.  **Acceder al Dashboard:**
    *   Vaya a **Educación -> Dashboard** para visualizar los reportes configurados.

## Dependencias

*   `account`: Requerido para la funcionalidad de creación de facturas.

## Autor

Jose Silva

## Licencia

LGPL-3