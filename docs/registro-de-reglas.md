# Registro de reglas

[English version](rules-log.md) · [Volver al README](../README.es.md)

Casi todas las reglas de este repositorio nacieron de un fallo real: algo salió mal, entendí por qué y la regla es lo que impide que vuelva a pasar. Algunas no nacieron de un fallo, sino que se desprenden de la propia forma de trabajar, y sus entradas lo dicen. Dentro de las skills y de los agentes las reglas aparecen sin fecha, porque al modelo solo le hace falta la regla. Este registro guarda la historia: cuándo apareció cada regla, qué pasó y por qué se resuelve así.

Cada entrada sigue el mismo formato: **Qué pasó → La regla → Por qué se resuelve así**. Cuando una regla no tiene detrás ningún incidente, la entrada lo dice.

---

## 2026-09-23 — Lanzar un worker lleva implícita la autorización de commit

**Qué pasó.** No hubo ningún incidente; esto se desprende de cómo funciona el modelo. Cuando el director lanza a los agentes, yo ya he hablado y decidido con él lo que vamos a hacer. Los agentes que lanza trabajan bajo su supervisión, así que pueden modificar ficheros y hacer commit. Lo que nunca pueden hacer es mergear en `main`, publicar, tocar producción ni nada de ese estilo.

**La regla.** Cuando el director lanza un worker con el perfil de director, eso cuenta como mi autorización para que el worker haga commit y push de su propio trabajo. Solo el push a `main`, los merges, la publicación, producción y las operaciones forzadas siguen reservados a mi consentimiento explícito.

**Por qué se resuelve así.** El worker tiene que terminar sin paradas. Git guarda la historia y el director revisa después del commit, sobre el diff real; un commit malo se revierte con otro nuevo. Preguntar antes de cada commit añadiría una parada sin añadir control.

## 2026-10-01 — El informe es del director, y hace commit de él sin preguntar

**Qué pasó.** No hubo ningún incidente. El informe no es código: es el documento propio del director, escrito por el director, así que lo gestiona el director. Se hace commit para no perder información: no hace falta con cada frase ni cada dos minutos, pero tampoco puede pasar una semana sin commit. Y el director no necesita preguntarme cada vez; es su informe.

**La regla.** El informe es responsabilidad del director. Hace commit de él cuando se cierra una parte o cuando tiene sentido, nunca tan de tarde en tarde que pueda perderse información. Momentos típicos son tras registrar una decisión, tras un lanzamiento, al cerrar una revisión o ante el riesgo de una compactación. Lo hace en sus propios lotes, con la ruta explícita y sin mezclar ficheros de los workers.

**Por qué se resuelve así.** El informe es el documento de trabajo del director, no un entregable que yo tenga que aprobar. Mantener al día la copia remota forma parte de gestionarlo y no añade peticiones de permiso.

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

**La regla.** El director no hace commit mientras haya algún worker en marcha. Mientras tanto, sus cambios en el informe se acumulan en disco. Justo antes de cada commit ejecuta `git status --short` y comprueba que los únicos ficheros modificados son los suyos; si aparece cualquier otro, espera.

**Por qué se resuelve así.** Los ficheros a medio hacer de otro agente están en el mismo árbol, así que un commit en mal momento puede interferir con ellos. Lo seguro es hacer commit solo cuando el árbol no contiene trabajo de nadie más. El informe en disco ya es la memoria; el commit es solo su copia remota y puede esperar.

## 2026-11-09 — Cada petición al usuario se entiende por sí sola

**Qué pasó.** Yo no sigo el hilo. Entre dos mensajes míos, el director había hablado con workers y con otras sesiones, y mensajes como «sigo esperando a X» o «el documento» no me decían nada.

**La regla.** Cada vez que el director necesita algo de mí (una decisión, un consentimiento, algo que leer), el mensaje lleva el contexto completo como si fuera el primero del día: de qué tarea se trata y cómo hemos llegado aquí, qué se pide exactamente y por qué ahora, las opciones con una recomendación, la ruta completa de lo que tenga que mirar y qué pasará cuando conteste. Quedan prohibidos el «sigo esperando a X» a secas y los pronombres que remiten a mensajes anteriores.

**Por qué se resuelve así.** El director sabe todo lo que ha pasado entre medias; yo solo leo el final. Reconstruir el contexto le cuesta al director unas pocas líneas y a mí me ahorra reconstruir una conversación que no he visto.

## 2026-11-10 — Los arreglos rápidos van al quick-fixer, nunca al director

**Qué pasó.** No hubo un incidente como tal. Cuando el director aplicaba él mismo los arreglos rápidos, cada arreglo ensuciaba su contexto y lo hacía más grande sin necesidad. Pasé los arreglos rápidos a un agente aparte para mantener el contexto del director lo más limpio posible.

**La regla.** El director no aplica arreglos rápidos él mismo. Diagnostica, yo apruebo, y un agente `quick-fixer` dedicado, con un modelo más barato, aplica el arreglo a partir de un brief corto, lo verifica y hace commit. El director revisa el diff después, como con cualquier worker.

**Por qué se resuelve así.** El contexto del director es lo que sostiene el hilo de toda la línea de trabajo; llenarlo con los detalles de cada arreglo pequeño lo hace peor en su verdadero trabajo. El modelo más barato va en segundo lugar y es una optimización, no el motivo: un arreglo rápido tiene un alcance acotado, así que basta un modelo más barato.

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

## 2026-11-23 — Solo este proyecto

**Qué pasó.** A una sesión de un proyecto le pedí «revisar los streams» y se puso a listar las demás sesiones de la máquina y a leer informes e historial de git de otros proyectos. No modificó nada.

**La regla.** El director y todos los agentes que lanza trabajan dentro del proyecto: su repositorio, `~/.claude`, el scratchpad y los ficheros temporales de la sesión, y los propios agentes del director. No salen de ahí por iniciativa propia: ni otros repositorios o carpetas de la máquina, ni otras sesiones de Claude Code (listarlas, leer lo que hacen, escribirles). Solo salen cuando yo lo pido y nombro el destino; esa petición ya es la autorización. Que una herramienta, un permiso, un directorio de trabajo adicional o una ruta en un fichero permitan llegar a algo no lo mete en el alcance. «Los directores», «los streams», «los informes» son los de este proyecto, y las búsquedas parten del proyecto, nunca de una carpeta padre o de una unidad. El worker solo sale si el brief nombra esa ruta o sesión exacta; si cree que hace falta algo de fuera, lo dice en su informe.

**Por qué se resuelve así.** El límite viene de mi petición, no de lo que la máquina deja alcanzar: cada uno configura su máquina por sus propias razones, y eso no dice nada sobre qué quiero que se mire. Es un límite, no un control: dentro del proyecto se trabaja como siempre y no se pide nada nuevo.

## 2026-11-23 — Un mensaje por entrega, después de la revisión

**Qué pasó.** No hay un incidente registrado.

**La regla.** Cuando llega una entrega (worker, `quick-fixer` o agente de exploración), el director escribe como mucho una línea («T7 entregada, la reviso») y hace la revisión; me escribe una sola vez, con el resultado ya verificado. Una tarea devuelta a corrección se anuncia en una línea y el mensaje de revisión se escribe cuando se cierra, salvo que la corrección necesite antes una decisión mía. Si una conclusión depende de varios agentes, la síntesis se escribe cuando entrega el último. Las peticiones se retienen mientras un agente en marcha pueda cambiar sus opciones o la recomendación, diciendo en una línea qué se retiene y a quién espera. Una pregunta directa mía se contesta en el momento.

**Por qué se resuelve así.** Lo que reporta un agente no está verificado cuando llega su notificación. Contármelo entonces y otra vez tras comprobarlo me obliga a leer lo mismo dos veces, la primera en su versión menos fiable, y una revisión que corrige el resumen del agente contradice lo que el director ya había dicho.

## 2026-11-23 — Formato de las respuestas

**Qué pasó.** La primera versión de esta regla, escrita ese mismo día, cerraba cada mensaje con un bloque de estado fijo de tres líneas (qué está en marcha, qué viene después, qué está pendiente de mí) dentro de un bloque de código. Al usarlo, las líneas no se ajustaban y obligaban a desplazarse en horizontal, y el bloque se escribía aunque no tuviera nada que decir («Running: nada»). Lo quité ese mismo día.

**La regla.** Una respuesta conversacional no tiene plantilla: contesta a lo preguntado. Dos piezas tienen forma fija, en mi idioma y sin secciones vacías: la revisión de una entrega (tarea, veredicto, commits, hallazgos de la revisión, decisiones propias del worker ratificadas o corregidas, cabos sueltos) y la petición de una decisión o un consentimiento (tarea y contexto, qué necesita de mí, opciones con la recomendada primero, dónde mirar, qué pasa después). El mensaje se cierra de forma conversacional y, cuando hay algo pendiente de mí, termina diciéndolo con palabras normales; una petición aún sin contestar se recuerda al final en una línea que se entiende por sí sola.

**Por qué se resuelve así.** Lo que importa es que al final del mensaje vea qué está pendiente de mí, y decirlo con palabras normales ya lo consigue. El arreglo fue deshacer el cambio, no añadir reglas sobre el fallo.

## 2026-11-23 — Los informes del director, en una carpeta fija y con un nombre acordado

**Qué pasó.** La skill del director solo decía que el informe se creara en la ruta de documentos del proyecto, sin carpeta ni nombre. Un proyecto acabó con un `informe-stream.md` genérico que no decía nada de su trabajo, y solo se encontraba porque el `CLAUDE.md` de ese proyecto lo nombraba.

**La regla.** Los informes del director viven en `docs/director-streams/` del proyecto (o en la carpeta que nombre su `CLAUDE.md`), un fichero por stream, con un nombre corto y descriptivo en kebab-case que yo recuerde (`docs/director-streams/checkout-redesign.md`). El nombre se acuerda al activar el perfil: si mi mensaje dice cuál es el trabajo y coincide con un stream existente, el director lee ese informe entero y lo retoma; si es trabajo nuevo, propone un nombre descriptivo, me lo dice en una línea para que pueda cambiarlo y crea el informe; si solo activo el perfil, me enseña los streams que hay y me pregunta en el chat si retomo uno o abro otro, cuál es el trabajo y cómo llamarlo. Un informe que yo señale en otro sitio se sigue leyendo entero y se usa tal cual.

**Por qué se resuelve así.** Con una carpeta fija el director encuentra los streams por sí mismo al activarse, y un nombre acordado al empezar es uno que recuerdo cuando vuelvo.
