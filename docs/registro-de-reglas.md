# Registro de reglas

[English version](rules-log.md) · [Volver al README](../README.es.md)

Casi todas las reglas de este repositorio nacieron de un fallo real: algo salió mal, entendí por qué y la regla es lo que impide que vuelva a pasar. Dentro de las skills y de los agentes las reglas aparecen sin fecha, porque al modelo solo le hace falta la regla. Este registro guarda la historia: cuándo apareció cada regla, qué pasó y por qué se resuelve así.

Cada entrada sigue el mismo formato: **Qué pasó → La regla → Por qué se resuelve así**. Cuando no tengo apuntada la historia de una regla, la entrada lo dice y describe en su lugar contra qué protege.

---

## 2026-09-23 — Lanzar un worker lleva implícita la autorización de commit

**Qué pasó.** No hay un incidente concreto registrado para esta regla. Protege contra un worker que, al final de su tarea, se para a pedir permiso para hacer commit cuando no hay nadie mirando.

**La regla.** Cuando el director lanza un worker con el perfil de director, eso cuenta como mi autorización para que el worker haga commit y push de su propio trabajo. Solo el push a `main`, los merges, producción y las operaciones forzadas siguen reservados a mi consentimiento explícito.

**Por qué se resuelve así.** El worker tiene que terminar sin paradas. Git guarda la historia y el director revisa después del commit, sobre el diff real; un commit malo se revierte con otro nuevo. Preguntar antes de cada commit añadiría una parada sin añadir control.

## 2026-10-01 — El informe es del director, y hace commit de él sin preguntar

**Qué pasó.** No hay un incidente concreto registrado para esta regla. Protege la memoria del director: un informe que solo existe en disco, sin commit, se puede perder, y un director que tiene que preguntar antes de cada commit del informe o me interrumpe o deja que el informe se quede atrás.

**La regla.** El informe es responsabilidad del director. Él decide cuándo merece la pena un commit (tras registrar una decisión, tras un lanzamiento, al cerrar una revisión o ante el riesgo de una compactación) y lo hace en sus propios lotes, con la ruta explícita y sin mezclar ficheros de los workers.

**Por qué se resuelve así.** El informe es el documento de trabajo del director, no un entregable que yo tenga que aprobar. Dejarlo a su criterio mantiene al día la copia remota sin añadir peticiones de permiso.

## 2026-10-01 — Todos los borrados al final, con un inventario

**Qué pasó.** Un borrado en mitad de una tarea disparó una petición de permiso de un hook y el worker se quedó parado, esperando a alguien que no estaba mirando.

**La regla.** Durante una tarea no se borra nada. El agente lleva un inventario de todo lo que ha creado y debe desaparecer (qué, dónde, cómo se borra) y ejecuta todos los borrados en un único paso final, justo antes de su informe. Si aun así algo se bloquea ahí, el informe lleva el inventario pendiente y lo resuelve el director.

**Por qué se resuelve así.** La petición de permiso no siempre se puede evitar, pero sí su momento. Al final, un borrado bloqueado para al agente con el trabajo ya hecho y con su commit; a mitad, para la tarea entera.

## 2026-10-16 — Los tests no usan recursos externos sin aprobación

**Qué pasó.** Una batería de tests agotó la cuota mensual de un servicio externo.

**La regla.** Las baterías de tests solo tocan recursos locales y desechables y dobles en proceso. Cualquier test o fixture que fuera a llegar a algo fuera de la máquina (una API externa, un servicio de pago o con cuota, la base de datos de producción), directamente o como efecto secundario del arranque de la aplicación, se valida antes conmigo, indicando su coste y su cuota. Los interruptores externos se neutralizan en la preparación de los tests antes de que se cargue la configuración de la aplicación. La regla vive en el perfil de tester (`project-example/.claude/skills/profile-tester/SKILL.md`).

**Por qué se resuelve así.** El daño viene de efectos secundarios que nadie ve leyendo un test suelto. Neutralizar los interruptores antes de cargar la configuración cierra esa puerta para todos los tests a la vez, en lugar de confiar en que cada test se acuerde.

## 2026-11-01 — Cero peticiones de permiso evitables

**Qué pasó.** Me seguían saltando peticiones de permiso aunque Bash estaba permitido. La documentación oficial confirmó después el motivo: los comandos compuestos se comprueban subcomando a subcomando, así que un `cd` o una cadena de operaciones de git pueden pedir permiso por sí solos.

**La regla.** Nada de `cd` en los comandos (se usa `git -C <ruta>` o rutas absolutas). Una operación de git por llamada. Mensajes de commit con `-m`, sin heredocs. Nada que vaya a parar un hook del proyecto (ficheros protegidos, borrados a mitad de tarea). Y la herramienta `Monitor` queda prohibida para los agentes: cada uso dispara una petición de permiso y no aporta nada que no dé ya un comando en primer plano con su timeout o un comando en segundo plano.

**Por qué se resuelve así.** Cada petición de un agente en segundo plano cae en mi sesión y para al agente hasta que contesto. Escribir los comandos con una forma que ya cubren las reglas de permitir quita la petición en origen, en lugar de aprobarla una y otra vez.

## 2026-11-06 — El director no hace commit mientras hay un worker en marcha

**Qué pasó.** Pasó más de una vez. El framework pre-commit guarda en un stash todos los cambios no preparados antes de un commit y los restaura después. Con ficheros a medio hacer de un worker en el árbol, cada commit del director los sacaba y los volvía a poner, y una restauración fallida los habría destruido.

**La regla.** El director no hace commit mientras haya algún worker en marcha. Mientras tanto, sus cambios en el informe se acumulan en disco. Justo antes de cada commit ejecuta `git status --short` y comprueba que los únicos ficheros modificados son los suyos; si aparece cualquier otro, espera. Si hay que hacer commit del informe con un worker activo, primero se le pide al worker que haga commit de lo que tenga. Tampoco se hace commit durante una fase de pruebas manuales con el servidor de desarrollo arrancado.

**Por qué se resuelve así.** El stash es cómo funciona el framework pre-commit, y desactivarlo supondría saltarse los hooks, que está prohibido. Así que lo seguro es hacer commit solo cuando el árbol no contiene trabajo de nadie más. El informe en disco ya es la memoria; el commit es solo su copia remota y puede esperar.

## 2026-11-09 — Cada petición al usuario se entiende por sí sola

**Qué pasó.** Yo no sigo el hilo. Entre dos mensajes míos, el director había hablado con workers y con otras sesiones, y mensajes como «sigo esperando a X» o «el documento» no me decían nada.

**La regla.** Cada vez que el director necesita algo de mí (una decisión, un consentimiento, algo que leer), el mensaje lleva el contexto completo como si fuera el primero del día: de qué tarea se trata y cómo hemos llegado aquí, qué se pide exactamente y por qué ahora, las opciones con una recomendación, la ruta completa de lo que tenga que mirar y qué pasará cuando conteste. Quedan prohibidos el «sigo esperando a X» a secas y los pronombres que remiten a mensajes anteriores.

**Por qué se resuelve así.** El director sabe todo lo que ha pasado entre medias; yo solo leo el final. Reconstruir el contexto le cuesta al director unas pocas líneas y a mí me ahorra reconstruir una conversación que no he visto.

## 2026-11-10 — Los arreglos rápidos van al quick-fixer, nunca al director

**Qué pasó.** No hay un incidente concreto registrado para esta regla. Protege el contexto del director y evita que los arreglos pequeños crezcan.

**La regla.** El director no aplica arreglos rápidos él mismo. Diagnostica, yo apruebo, y un agente `quick-fixer` dedicado, con un modelo más barato, aplica el arreglo a partir de un brief corto, lo verifica y hace commit. El director revisa el diff después, como con cualquier worker.

**Por qué se resuelve así.** Un arreglo rápido tiene un alcance acotado, así que basta un modelo más barato. Y el contexto del director es lo que sostiene el hilo de toda la línea de trabajo; llenarlo con los detalles de cada arreglo pequeño lo hace peor en su verdadero trabajo.

## 2026-11-18 — Boy Scout solo dentro de los ficheros del worker; ninguno para el quick-fixer

**Qué pasó.** La definición del worker y el `CLAUDE.md` de un proyecto se contradecían: una decía que no se tocara nada fuera del brief y el otro que se arreglara cualquier desorden encontrado por el camino.

**La regla.** El worker deja el código más limpio solo dentro de los ficheros que ya toca por su tarea. El quick-fixer no limpia nada. Lo que cualquiera de los dos vea mal fuera de eso va a su informe con `fichero:línea`, y el director me lo trae como decisión.

**Por qué se resuelve así.** Resuelve la contradicción manteniendo el diff de cada agente en su tarea, que es lo que revisa el director. Los problemas encontrados fuera de la tarea no se pierden: se convierten en decisiones.

## 2026-11-18 — /commit y /update-docs pasan a ser comandos de cada proyecto

**Qué pasó.** Los comandos globales `/commit` y `/update-docs` habían acumulado bloques que solo valían para proyectos concretos.

**La regla.** Los dos pasan a ser plantillas en `global/templates/`. Cada proyecto guarda su propia copia adaptada en `.claude/commands/`, con sus pasos específicos en la sección que la plantilla reserva para ello.

**Por qué se resuelve así.** Los comandos globales se cargan en todos los proyectos, así que los bloques propios de un proyecto eran ruido en el contexto y cadenas de decisiones sobre proyectos que no tenían nada que ver con el actual. El precio es que las mejoras de las plantillas se llevan a mano a cada proyecto.

## 2026-11-18 — (preferencia opcional) Preguntar en el chat, no con la herramienta de preguntas con opciones

**Qué pasó.** No hay un incidente concreto registrado. Es una preferencia, no un arreglo.

**La regla.** Los agentes me hacen sus preguntas en el chat, cuando han terminado su trabajo o se han parado ante un bloqueo real, en lugar de usar la herramienta de preguntas con opciones.

**Por qué se resuelve así.** La herramienta bloquea la sesión hasta que contesto, la pregunta llega en mitad del trabajo y, si no estoy delante, ese tiempo de ejecución se pierde. Otros pueden preferir la herramienta; consulta la sección 8 de la [guía](guia.md).
