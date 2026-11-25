# Guía

[English version](guide.md) · [Volver al README](../README.es.md)

Esta guía explica cómo encajan las piezas de este repositorio y por qué son como son. Describe mi configuración; donde algo es una preferencia y no un requisito del modelo, lo digo y explico la alternativa.

## 1. Los roles

**El director** es la sesión de Claude Code con la que hablo. Lo activo con la skill `profile-director` (`global/skills/profile-director/SKILL.md`). Su contrato es sencillo: yo hablo y decido; él hace todo lo demás a través de agentes. Analiza el código antes de opinar, presenta opciones con una recomendación y su coste real, escribe los briefs, lanza los agentes, revisa lo que entregan y mantiene el informe. Nunca implementa tareas él mismo y nunca me convierte en mensajero: no se me pide pegar un brief en otra ventana ni traerle de vuelta el resumen de un agente.

El director y todos los agentes que lanza trabajan dentro del proyecto: su repositorio, `~/.claude`, el scratchpad y los ficheros temporales de la sesión. No van a otro repositorio, a otra carpeta de la máquina ni a otra sesión de Claude Code por iniciativa propia; solo van cuando yo lo pido y nombro el destino, y esa petición ya es la autorización. Poder llegar no es estar en el alcance: las reglas de permisos, los directorios de trabajo adicionales de la configuración o las rutas que aparecen en los ficheros no amplían el proyecto. Dentro de él se trabaja como siempre; es un límite, no un control más.

**El worker** (`global/agents/worker.md`) ejecuta una tarea a partir de un brief, de principio a fin, en segundo plano. Lee el `CLAUDE.md` del proyecto, activa el perfil que indica el brief, ejecuta el flujo que indica el brief (`/new-feature`, `/rework`, `/fix-bug` y después `/do-feature`), verifica, hace commit y push, cierra la documentación y termina con un informe de 20 líneas como máximo. No toma decisiones de producto ni reabre las que están cerradas. Si decide algo por su cuenta, lo anota y lo reporta, y el director lo ratifica o lo corrige.

**El quick-fixer** (`global/agents/quick-fixer.md`) aplica un único arreglo que el director ya ha diagnosticado y yo ya he aprobado: un bug localizado, un retoque de estilo, un cambio menor de configuración. Alcance estricto: si el arreglo resulta más grande de lo que dice el brief, necesita una migración, cruza backend y frontend o merece un test de regresión, se para sin tocar nada y lo reporta. No escribe tests nuevos. Funciona con un modelo menos capaz que el worker, porque un arreglo acotado y ya diagnosticado no necesita el más capaz.

**Los perfiles de proyecto** son skills que viven en cada proyecto (`project-example/.claude/skills/profile-*`): `profile-backend`, `profile-frontend`, `profile-planner`, `profile-auditor` y `profile-tester`. No son tipos de agente. Un perfil es un fichero markdown que define un rol, una lista de lectura y un ámbito de edición; el worker activa el que indica su brief y puede cambiar de perfil en la misma sesión cuando una tarea pasa de un área a otra.

**Los agentes opcionales.** `optional/agents/Explore.md` sustituye al agente Explore integrado en Claude Code solo para elegir modelo y esfuerzo; `optional/agents/web-fetch.md` es un agente adicional que lee páginas web públicas con un modelo elegido para ese trabajo, no una sustitución. Los trato en la sección 8.

## 2. El informe

Todo el modelo descansa en un único documento vivo por línea de trabajo: el informe del director. Los informes viven en `docs/director-streams/` del proyecto (o en la carpeta que nombre su `CLAUDE.md`), un fichero por línea de trabajo, con un nombre corto y descriptivo en kebab-case que yo recuerde, como `docs/director-streams/checkout-redesign.md`. El nombre se acuerda al activar el director: si mi mensaje dice cuál es el trabajo y coincide con una línea existente, el director lee ese informe y la retoma; si es trabajo nuevo, propone un nombre, me lo dice en una línea para que pueda cambiarlo y crea el informe; si solo activo el perfil, me enseña las líneas que hay y me pregunta si retomo una o abro otra. Su estructura:

- **Contexto y diagnóstico**: de qué trata la línea de trabajo y cómo estaba el código al empezar.
- **Modelo de trabajo**: cómo funciona esta línea (en serie o no, quién hace commit de qué).
- **Tabla de decisiones**: fecha, decisión y motivo, una fila por decisión.
- **Cola de tareas**: tareas numeradas, cada una con su estado (`launched` → `delivered` → `in correction` → `approved and closed`), su brief pegado entero, el identificador del agente, el veredicto de la revisión y los hashes de los commits.
- **Diario de sesión**: cronológico, solo se añade.
- **Guion de pruebas acumulado**: cada tarea cerrada añade sus casos numerados, con referencias concretas, para que la prueba manual final sea hacer clic y no buscar.

El informe es lo que sobrevive. Las compactaciones de contexto pierden detalle y un chat nuevo empieza de cero; el informe está en disco y en git. Cuando abro una sesión nueva, le digo al director en qué estoy trabajando (o le señalo un informe, esté donde esté) y lee ese informe entero antes de decir nada.

Las decisiones se anotan en el mismo turno en que se toman, y con mi motivo **en mis propias palabras** cuando lo doy. El ejemplo de la skill es «no vendemos pasta de dientes». Una paráfrasis pierde el peso del motivo: tres semanas después, un resumen como «alcance del producto» no impide que alguien reabra la decisión, y mi frase sí. Esas decisiones viajan a los briefs marcadas como cerradas, y los agentes no las reabren.

El informe es responsabilidad del director. Hace commit de él sin preguntarme, en sus propios commits, con la ruta explícita y nunca mientras haya un worker en marcha (la sección 4 explica por qué).

Un director y su informe sirven para una línea de trabajo, una tarea o un bloque de tareas relacionadas, no para el proyecto entero para siempre. Cuando el bloque termina, cierro la línea, y el siguiente bloque empieza con una sesión de director nueva y un informe nuevo. Un informe grande, incluso de unos 100k tokens, está bien si el trabajo es así de grande: releer el informe sigue siendo mucho más barato que releer la conversación que lo produjo, y de eso se trata.

### Retomar después de una pausa: la caché

Claude Code guarda la conversación en la caché de prompts durante un tiempo limitado. Según la [documentación oficial de configuración](https://code.claude.com/docs/en/settings) (el ajuste `promptCacheTtl`), en el momento de escribir esto el valor por defecto es de 1 hora con una suscripción de Claude (dentro de sus límites de uso) y de 5 minutos con una clave de API, Bedrock, Vertex o Foundry. Puede cambiar.

Una vez caducada la caché, cualquier mensaje nuevo en esa conversación, aunque sea un simple «hazme un resumen», vuelve a enviar y procesar la conversación entera. Si la conversación era larga, eso sale caro en tokens.

Con el informe no necesito volver a la conversación antigua. Abro una sesión nueva, activo el director y le digo qué línea de trabajo retomamos; el informe lo encuentra en su carpeta. El único coste es leer el informe, no volver a enviar una conversación que puede ser muy larga. Así que el informe no solo sobrevive a las compactaciones y a los chats nuevos: después de una pausa, además ahorra muchos tokens.

## 3. La vida de una tarea

1. **Brief.** Lo escribe el director y lo pega en el informe antes de lanzar, para que sobreviva a las compactaciones.
2. **Lanzamiento.** El director lanza el agente con la herramienta `Agent`, en segundo plano, con el brief como prompt. Sigue disponible para mí mientras el agente trabaja.
3. **Entrega.** Cuando el agente termina, llega una notificación con su informe final. Ese informe es el único canal de vuelta del agente y yo no lo veo: el director lo registra y, hasta terminar la revisión, me dice como mucho una línea («T7 entregada, la reviso»).
4. **Revisión sobre el diff real.** El director lee el diff completo de los commits de la tarea, lee enteros los ficheros críticos, repite él mismo las comprobaciones clave y revisa una a una las «decisiones tomadas por su cuenta» del agente. Nunca aprueba sobre el resumen.
5. **Correcciones.** Si hay que arreglar algo, el director envía las correcciones al mismo agente con `SendMessage` (conserva su contexto); el agente las aplica, verifica y vuelve a hacer commit, y el director revisa de nuevo. Una entrega rechazada se revierte con un commit nuevo o se rehace, nunca reescribiendo la historia.
6. **Cierre.** Solo tras un veredicto explícito la tarea pasa a cerrada en el informe.

Al agente no se le pide que espere a que se apruebe su plan ni a la revisión antes de hacer commit. Git guarda la historia y el director revisa después, sobre el commit. Eso es lo que permite que el agente trabaje sin pararse.

### Cómo me informa el director

Lo que reporta un agente no está verificado cuando llega, así que el director me cuenta una entrega una sola vez, después de la revisión: un mensaje con el resultado ya verificado, nunca un resumen del informe del agente seguido de un segundo mensaje que lo corrige. Una tarea devuelta a corrección se anuncia en una línea, y el mensaje de revisión llega cuando la tarea se cierra, salvo que la corrección necesite antes una decisión mía. Cuando una conclusión depende de varios agentes, se escribe una vez, cuando ha entregado el último, y una petición de decisión se retiene mientras un agente en marcha todavía pueda cambiar sus opciones. Una pregunta directa mía se contesta en el momento, esté lo que esté en marcha.

Las respuestas normales no tienen plantilla: contestan a lo que he preguntado. Dos piezas tienen forma fija: la revisión de una entrega (tarea, veredicto, commits, hallazgos de la revisión, decisiones propias del agente ratificadas o corregidas, cabos sueltos) y la petición de una decisión o un consentimiento (tarea y contexto, qué necesita de mí, opciones con la recomendada primero, dónde mirar, qué pasa después). La petición completa se escribe una vez; mientras siga abierta, los mensajes siguientes la recuerdan en una línea que se entiende por sí sola. Cada mensaje se cierra de forma conversacional y, cuando hay algo pendiente de mí, termina diciéndolo con palabras normales.

### Qué lleva un buen brief

El agente no ve la conversación, solo el brief, el repositorio y su documentación. Un buen brief:

- **No repite la documentación del proyecto.** Lleva solo lo que `CLAUDE.md` y los documentos no cubren. Las instrucciones genéricas repetidas son ruido y acaban divergiendo.
- **Arranca sin preguntas.** Dice qué perfil activar, qué flujo ejecutar y sobre qué documento, y deja resuelto de antemano todo lo que preguntaría un flujo interactivo («el plan ya está aprobado por el director»).
- **Tiene una sección de decisiones cerradas** («tomada; no reabrir»). Si el agente encuentra un motivo para reabrir una, lo plantea en su informe.
- **Tiene un «fuera de alcance» explícito**, incluido lo que se aparcó a propósito y por qué, para que nadie lo arregle de paso.
- **Lleva un aviso de obsolescencia** cuando su material (una auditoría, un inventario) es anterior a otros cambios: cada punto se vuelve a comprobar contra el código actual antes de tocar nada.
- **Tiene un cierre sin paradas**: verificar, hacer commit, cerrar la documentación, informar. Frases como «espera a la aprobación» o «pregunta antes de X» están prohibidas salvo que X sea un bloqueo técnico real.
- **Deja todos los borrados para el final, con un inventario.** Durante la tarea no se borra nada; el agente apunta lo que ha creado y debe desaparecer (qué, dónde, cómo) y lo borra en un único paso final. Un borrado puede disparar una petición de permiso; al final, esa petición para al agente con el trabajo ya hecho y no a medias.
- **Da el contexto de concurrencia**: qué otros agentes están activos y qué ficheros ajenos puede encontrarse modificados.

## 4. Un único árbol de trabajo, sin worktrees

Los agentes trabajan en el mismo árbol de trabajo que el director, sin aislarse en worktrees. Lo elegí así porque trabajo solo: el director revisa cada entrega con `git show` y `git diff` en la misma rama y nunca hace falta un merge. Los merges son caros, y con una sola persona decidiendo no hay de quién aislarse.

El precio es un conjunto de reglas sobre los commits, porque varias sesiones comparten un mismo árbol:

- Cada agente hace commit solo de sus rutas, de forma explícita. Nunca `git add -A`.
- **El director no hace commit mientras hay un worker en marcha.** Los ficheros a medio hacer del worker están en el mismo árbol, así que un commit en mal momento puede interferir con ellos. El director deja que sus cambios en el informe se acumulen en disco y solo hace commit cuando no hay ningún worker en marcha, después de comprobar con `git status --short` que los únicos ficheros modificados son los suyos.
- Antes de cada commit, el agente ejecuta `git status --short` y comprueba que en el commit solo entran sus propios ficheros. Los ficheros ajenos siguen modificados y no se tocan.

Si trabajas en equipo, o quieres varios agentes implementando a la vez, puede que los worktrees te encajen mejor. La skill del director admite `isolation: "worktree"` cuando el usuario lo pide.

## 5. Varios directores en paralelo

A veces llevo dos líneas de trabajo a la vez, cada una con su director, en el mismo árbol de trabajo. Funciona, con algunas precauciones.

**La coordinación no está en la skill, a propósito.** Si la skill del director dijera «puede haber otros directores», el modelo lo comprobaría cada vez y llenaría su contexto con eso. En su lugar, cuando abro un segundo director se lo digo en una frase: «otro director se está ocupando de X; contactará contigo y os ponéis de acuerdo».

**Nombro un único coordinador principal.** Las decisiones sobre lo compartido (quién hace commit y cuándo, quién toca un fichero común) las toma un director, no todos hablando con todos.

**El riesgo conocido.** La regla «el director no hace commit mientras hay un worker en marcha» protege a los workers de ese director, no a los de otro. Un director que no sabe nada del worker del otro puede hacer commit en mitad de su tarea e interferir con sus ficheros a medio hacer. El coordinador decide quién hace commit y cuándo, y cada director ejecuta `git status --short` antes de cada commit y no lo hace si ve ficheros que no son suyos.

## 6. Comandos por proyecto a partir de plantillas

`/commit` y `/update-docs` no son comandos globales. Cada proyecto tiene su propia copia en `.claude/commands/`, generada a partir de las plantillas de `global/templates/` (que guardo en `~/.claude/templates/`), con los pasos propios del proyecto rellenados: ficheros que protege un hook, un token de aprobación, documentación adicional que hay que mantener al día al cerrar.

Por qué: antes eran globales y con el tiempo fueron acumulando bloques que solo valían para un proyecto u otro. Todas las sesiones de todos los proyectos los cargaban enteros. Eso es ruido en el contexto y, peor aún, le da al modelo cadenas de decisiones sobre proyectos en los que no está trabajando («si es el proyecto A, haz X»).

El precio: cuando mejoro una plantilla, tengo que llevar la mejora a mano a cada proyecto.

Los demás flujos (`/fix-bug`, `/rework`, `/do-feature` y la skill `new-feature`) siguen siendo globales porque no contienen nada propio de un proyecto: remiten al `CLAUDE.md` de cada uno para comandos, rutas y políticas.

## 7. Permisos

Lo que sigue se basa en la documentación oficial de Claude Code: [permisos](https://code.claude.com/docs/en/permissions), [modos de permisos](https://code.claude.com/docs/en/permission-modes) y [subagentes](https://code.claude.com/docs/en/sub-agents). Consulta esas páginas para el detalle actual; el comportamiento puede cambiar entre versiones.

**Los agentes en segundo plano se ejecutan en tu sesión.** Sus peticiones de permiso te llegan a ti, en la sesión del director, y una aprobación «para esta sesión» también los cubre. Por eso importa cada petición que dispara un agente: me interrumpe y, si no estoy mirando, el agente espera.

**Los comandos compuestos se comprueban subcomando a subcomando.** Las reglas de permisos de Bash se evalúan para cada subcomando de un comando compuesto, así que `cd algun-sitio && git commit ...` puede pedir permiso aunque Bash esté permitido. De ahí las reglas que siguen todos los agentes:

- nunca `cd` en un comando (se usa `git -C <ruta>` o rutas absolutas);
- una operación de git por llamada (`git add`, `git commit` y `git push` por separado, nunca encadenados con `&&`);
- mensajes de commit con `-m` (uno para el asunto y otro para el trailer), sin heredocs.

**Rutas protegidas.** La carpeta `.claude` (y `.git`, `.vscode` y algunas más) es una ruta protegida: las reglas de permitir no aprueban de antemano las escrituras en ella. En el modo por defecto las apruebas tú, y puedes aprobarlas para toda la sesión. El modo `auto` deriva esas escrituras a un clasificador. `bypassPermissions` se salta las comprobaciones, y yo solo lo usaría en un entorno aislado (un contenedor o una máquina desechable).

El ejemplo de proyecto trae un hook, `project-example/.claude/hooks/protected_commit_guard.py`, que pide permiso antes de cualquier commit que meta un fichero protegido (traducciones, textos legales), salvo que el comando lleve un token de aprobación. Los agentes dejan esos ficheros modificados y sin preparar, y el director hace commit de ellos tras revisarlos.

## 8. Preferencias opcionales

Son decisiones que tomé para mí. Cada una es una opción; el motivo está ahí para que decidas tú.

**(a) Preguntas en el chat en lugar de la herramienta de preguntas con opciones.** Claude Code tiene una herramienta para hacerte preguntas con opciones predefinidas. Yo prefiero que el agente me pregunte en el chat, en texto normal. La herramienta bloquea la sesión hasta que contesto, la pregunta llega en mitad del trabajo y, si no estoy delante, ese tiempo de ejecución se pierde. Prefiero que el agente termine su trabajo (o se pare ante un bloqueo real) y luego me pregunte en el chat. Si sueles estar delante de la pantalla, o te gusta contestar con un clic, puede que la herramienta te encaje mejor.

**(b) Modelo y esfuerzo por agente.** El frontmatter de `worker` y de `quick-fixer` trae valores sugeridos de `model` y `effort`, marcados como sugerencia: si los quitas, el agente hereda los de la sesión. Describo cada elección por si el trabajo sale bien, no por lo que cuesta: el quick-fixer usa un modelo menos capaz porque un arreglo acotado y ya diagnosticado no necesita el más capaz. `optional/agents/Explore.md` existe solo para elegir el modelo y el esfuerzo del agente Explore integrado: un agente de usuario o de proyecto llamado `Explore` sustituye al integrado y conserva su propio campo `model` ([documentación de subagentes](https://code.claude.com/docs/en/sub-agents), apartado «Built-in subagents»). `optional/agents/web-fetch.md` no sustituye a nada: es un agente adicional que lee páginas web públicas con un modelo elegido para ese trabajo. Si los valores por defecto te sirven, no necesitas ninguno de los dos.

El director no es un fichero de agente: es la propia sesión, así que su modelo es el que elijo con `/model` (ahí está también el control del esfuerzo, o `/effort`) antes de activar el perfil. Mi recomendación, no un requisito: el modelo más capaz que tengas, con esfuerzo alto. El director entiende el problema, decide conmigo, escribe los briefs y revisa sobre el diff real, así que un error ahí se propaga a todos los workers; los workers reciben en el brief el razonamiento ya hecho, así que ahí un modelo menos capaz aguanta bien. Por ejemplo, en el momento de escribir esto, la [página oficial de configuración de modelos](https://code.claude.com/docs/en/model-config) describe los modelos Fable como los más capaces de Claude Code y Opus como el modelo para razonamiento complejo; consúltala para ver los actuales. El campo `model` del frontmatter de una skill no sirve para esto: según la [documentación de skills](https://code.claude.com/docs/en/skills), solo se aplica durante el resto del turno que invoca la skill, y la sesión vuelve a su modelo con el siguiente mensaje.

**(c) Política de tests.** En mis proyectos los tests no se escriben durante la implementación: son una fase final, que lanzo yo a mano cuando he validado la funcionalidad, y que lleva `profile-tester`. El motivo: mientras una funcionalidad se sigue iterando, los tests se reescriben una y otra vez sin aportar nada. La única excepción es `/fix-bug`, cuyo test de regresión va con el arreglo. Es una política del `CLAUDE.md` del proyecto, no de los flujos globales: si un proyecto no la tiene, `/new-feature` y `/rework` planifican los tests dentro de cada fase. Mucha gente prefiere tests en cada fase; los dos enfoques funcionan con estos ficheros.

**(d) Boy Scout.** El `CLAUDE.md` del ejemplo de proyecto pide dejar el código más limpio de lo que estaba. Para los agentes acotados lo limito: el worker solo limpia dentro de los ficheros que ya toca por su tarea, y el quick-fixer no limpia nada. Lo que vean fuera va a su informe con `fichero:línea`, y el director me lo trae como decisión. El motivo: la definición del worker (no tocar nada fuera del brief) y el `CLAUDE.md` del proyecto (arregla cualquier desorden que encuentres) se contradecían, y esto lo resuelve. El diff del agente se queda en su tarea, que es lo que revisa el director, y lo que encuentra fuera me llega como decisión y no como un cambio que nadie ha pedido. Si quieres una limpieza más amplia, dale su propia tarea.

La ruta guiada son tres skills: `init-harness` monta el harness, `harness-onboarding` hace contigo una primera tarea y `harness-keeper` responde a cómo funcionan las cosas y hace los ajustes posteriores. Estas opciones se eligen con `harness-keeper` («llama al harness keeper», o `/harness-keeper`), que te ofrece cada una cuando lo que le cuentas la toca, o cuando le preguntas qué se puede ajustar; el catálogo en el que se apoya es [`global/skills/harness-keeper/optional-rules.md`](../global/skills/harness-keeper/optional-rules.md).

## 9. Ficheros compartidos en un commit

`worker.md` dice que en el commit del worker solo entran sus propios ficheros. La plantilla `commit.md` dice que si la tarea ha añadido contenido a un fichero compartido (un índice, un README, un documento de módulo), se hace commit del fichero entero, aunque contenga también cambios de otro agente. Parecen contradecirse, pero para mí no es así: quién escribe en un fichero compartido, y cuándo, lo decide el director.

El director implementa en serie por defecto y solo paraleliza tareas cuyas superficies ha comprobado en el código que son disjuntas. Si dos tareas comparten un fichero, decide el orden y van en serie, así que un fichero compartido nunca tiene a la vez cambios a medias de dos agentes. Si aun así se cuela algún solapamiento, el director lo detecta en la revisión.
