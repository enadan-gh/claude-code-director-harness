# claude-code-director-harness

[Read in English](README.md)

> **En evolución constante.** Este repositorio es un punto de partida que cada persona adapta a su forma de trabajar. No acepta contribuciones (los issues y los pull requests están cerrados), pero eres libre de copiarlo y adaptarlo a tus necesidades; esa es la idea.

## Instálalo con tu agente de IA

Abre Claude Code en tu proyecto y dile: «Instala el harness de director de https://github.com/enadan-gh/claude-code-director-harness en este proyecto.» También puedes darle el enlace sin más, con tus palabras, y preguntarle si te encaja. Necesitas Claude Code, porque el harness se compone de skills y agentes de Claude Code.

### Instrucciones para el agente

Si un usuario te ha dado la URL de este repositorio y te ha pedido instalarlo en su proyecto, haz esto, en orden. Siempre que necesites algo del usuario, pregúntaselo en el chat, con palabras sencillas, y deja que conteste con sus propias palabras.

1. No instales nada todavía en el proyecto del usuario. Tu primer mensaje al usuario es esta explicación, en su idioma, en un mensaje propio, enviado antes de cualquier pregunta o acción que le necesite: «En vez de pedirle cosas a la IA y revisar tú cada resultado, hablas con ella como con un jefe de proyecto. Le cuentas lo que quieres, lo decidís juntos, y ella encarga el trabajo a otros agentes de IA, que lo hacen mientras seguís hablando. Cuando terminan, comprueba lo que han cambiado de verdad antes de contártelo. Y lo va apuntando todo en un documento dentro de tu proyecto: lo que habéis decidido, lo que está hecho y lo que queda. Así, mañana abres un chat nuevo y sigue donde lo dejasteis. A ese papel lo llamamos "director".» Dala entera: puedes adaptarla a su idioma, pero no quites ni resumas ninguna parte. Después dile que ahora vas a hacerle una entrevista para construir su propia versión.
2. Consigue una copia local de este repositorio FUERA del proyecto del usuario. Puedes leer este repositorio como necesites para seguir estos pasos; lo que acuerdas antes con el usuario es dónde va la copia local que se queda en su equipo (propón, por ejemplo, `~/claude-code-director-harness`). Después, si git está instalado, ejecuta `git clone https://github.com/enadan-gh/claude-code-director-harness.git` en esa carpeta; si el equipo no tiene git, descarga y descomprime allí <https://github.com/enadan-gh/claude-code-director-harness/archive/refs/heads/main.zip>. De si el usuario usa git o no se ocupa después la skill init-harness.
3. Copia `global/skills/init-harness/` de esa copia a `~/.claude/skills/init-harness/`. Avisa al usuario de que aparecerá una petición de permiso porque `~/.claude` está protegida, y de que es lo esperado, y sigue adelante: instalarla es lo que te ha pedido, y la petición de permiso es donde acepta o rechaza. Si esa carpeta ya existe, no la sobrescribas: díselo al usuario y usa la existente solo si es idéntica a la copia; si no, pregunta.
4. Una skill copiada durante una sesión se detecta en esa misma sesión: ejecuta `/init-harness` ahora, usando la copia local del paso 2 como repositorio de referencia (`<repo>`). Si `/init-harness` no está disponible, lee la copia `~/.claude/skills/init-harness/SKILL.md` y síguela paso a paso. No le pidas al usuario que reinicie.
5. Sigue las reglas de esa skill: lenguaje sencillo, pocas preguntas cada vez y en el chat, enseña lo que vas a escribir antes de escribirlo y no sobrescribas nunca.

Es la misma ruta que se describe en «Ruta guiada», dentro de «Cómo empezar», conducida por tu agente.

Así es como trabajo con Claude Code. Desarrollo productos reales yo solo, con Claude Code dentro de VS Code, y unos amigos me preguntaron cómo lo organizo. En lugar de explicarlo una y otra vez, he dejado aquí los ficheros que uso de verdad, limpios de todo lo personal y con comentarios sobre por qué existe cada pieza.

## Qué es

Un ejemplo comentado de una forma de trabajar: una sesión de Claude Code hace de **director**, que habla conmigo, decide conmigo y reparte el trabajo entre **agentes que se ejecutan en segundo plano**, y luego revisa lo que entregan. En una línea: es como hablar con un jefe de proyecto que ha repartido el trabajo entre su equipo.

No es un agente ni un harness completo. El harness es Claude Code: el bucle, las herramientas, los permisos. Esto es una capa de método por encima: quién decide, quién ejecuta, cómo se revisa el trabajo y dónde se guarda el hilo. Las ideas se podrían adaptar a otras herramientas como Codex, pero los ficheros están escritos para Claude Code y solo se han probado ahí.

El repositorio contiene los ficheros que lo hacen posible: una skill para el director, dos definiciones de agente (`worker` y `quick-fixer`), los comandos de flujo de trabajo que siguen los agentes, plantillas para comandos de cada proyecto y un ejemplo completo de lo que lleva el repositorio de un proyecto (su `CLAUDE.md`, perfiles de trabajo, un hook propio y un comando de despliegue).

No contiene skills de lenguajes ni de frameworks, y no es un paquete que se instale.

**Skills para tu stack.** Cada lector trae las skills de sus propios lenguajes y frameworks. Si lo has montado con la ruta guiada y quieres algunas, pídeselo al harness keeper con tus palabras: mira las tecnologías de tu proyecto, busca skills ([skills.sh](https://skills.sh) es un sitio donde encontrarlas, no el único), te propone unas pocas, revisa cada una antes de instalarla y no instala nada sin tu sí.

## Para quién es

Necesitas Claude Code. A partir de ahí, hay dos formas de entrar.

**Si no programas, o no has trabajado en serio con agentes de IA**, tu forma de entrar es la ruta guiada. Le das a Claude Code el enlace en tu proyecto. Te explica la idea, te pregunta qué te sale mal hoy con la IA y te propone solo lo que encaja. Hace él mismo la parte técnica, copiar y adaptar los ficheros, y te enseña todo antes de escribirlo. También sirve en proyectos pequeños. Lo que resuelve no depende del tamaño: es que la IA toque lo que no debe, olvide lo que se decidió o diga que algo está hecho sin comprobarlo.

**Si eres técnico**, úsalo para completar tu propia metodología, o quédate solo con algunas piezas: por ejemplo el informe, los briefs o la revisión sobre el diff real. Para eso está la ruta manual.

En los dos casos, lo que tienes es una manera concreta de organizar el trabajo con Claude Code: cómo mantener vivo un hilo largo de decisiones a través de compactaciones y chats nuevos, cómo delegar tareas en agentes en segundo plano sin perder el control y cómo evitar que las peticiones de permiso te interrumpan todo el día.

## Adapta, no copies

Esto es lo que me funciona a mí, en mi contexto: una persona, varios productos, un único árbol de trabajo por proyecto. No es una receta, y no está pensado para instalarlo y usarlo tal cual.

Varias piezas son preferencias personales (cómo me hace preguntas el agente, qué modelo usa cada agente, cuándo se escriben los tests, cuánta limpieza puede hacer un agente). En la [guía](docs/guia.md) las presento como opciones y explico por qué elegí cada una, para que decidas qué encaja con tu forma de trabajar o la de tu equipo. Quédate con las ideas, lee los ficheros y reescríbelos a tu manera.

## El modelo de trabajo

Abro una sesión de Claude Code en el proyecto y activo el perfil de director. A partir de ahí yo solo hablo y decido. El director lee el código real antes de opinar, me plantea las opciones con su coste real y una recomendación, y registra cada decisión que tomo, con mi motivo y con mis propias palabras.

**Qué modelo para el director.** Es una recomendación, no un requisito: activa el director con el modelo más capaz que tengas, con un esfuerzo de razonamiento alto, elegido con `/model` antes de activar el perfil. El director entiende el problema, decide contigo, escribe los briefs y revisa sobre el diff real, así que un error ahí se propaga a todos los workers. Los workers reciben en el brief el razonamiento ya hecho, así que ahí un modelo menos capaz aguanta bien. La [guía](docs/guia.md) da un ejemplo con los modelos actuales.

Cuando algo queda decidido, el director escribe un **brief**: la descripción autocontenida de la tarea, con las decisiones cerradas, lo que queda fuera de alcance y cómo debe terminar. Lanza en segundo plano un agente `worker` con ese brief (o un `quick-fixer` para arreglos pequeños ya diagnosticados, que no necesitan el modelo más capaz). El agente ejecuta la tarea entera sin pararse: plan, implementación, verificación, commit y push, cierre de documentación y un informe final breve. Mientras tanto, el director sigue disponible para mí y prepara el siguiente brief.

Cuando el agente termina, el director **revisa la entrega sobre el diff real**, nunca sobre el resumen del agente. Lee los commits, repite él mismo las comprobaciones clave y aprueba o devuelve correcciones al mismo agente. Cada ronda de esta revisión ha encontrado algo que el resumen no mencionaba.

Todo vive en un único **informe**: un fichero markdown en el proyecto con el contexto, la tabla de decisiones, la cola de tareas, el diario de sesión y un guion de pruebas acumulado. El informe es la memoria del director. Sobrevive a las compactaciones de contexto y a los chats nuevos: si mañana abro otra sesión, le señalo el informe al director y retoma el hilo. Además ahorra tokens después de una pausa: cuando la caché de prompts ha caducado, cualquier mensaje en la conversación antigua la vuelve a enviar entera, mientras que una sesión nueva solo tiene que leer el informe (detalles en la [guía](docs/guia.md)).

## Mapa del repositorio

| Carpeta | Qué contiene | Adónde va |
| --- | --- | --- |
| `global/` | La skill del director (`skills/profile-director/`), las tres skills de la ruta guiada (`skills/init-harness/`, `skills/harness-onboarding/`, `skills/harness-keeper/`), los agentes (`agents/worker.md`, `agents/quick-fixer.md`), los comandos de flujo (`commands/do-feature.md`, `commands/fix-bug.md`, `commands/rework.md`) y la skill `new-feature` con su índice de skills | `~/.claude/`, con las mismas subcarpetas |
| `global/templates/` | `commit.md` y `update-docs.md`: plantillas, no comandos | El original se queda en `~/.claude/templates/`; una copia adaptada va al `.claude/commands/` de cada proyecto |
| `optional/` | `Explore`, que sustituye al agente Explore integrado solo para elegir modelo y esfuerzo, y `web-fetch`, un agente adicional que lee páginas web públicas con un modelo elegido para ese trabajo | `~/.claude/agents/`, si los quieres |
| `project-example/` | Lo que lleva el repositorio de un proyecto: una plantilla de `CLAUDE.md`, cinco perfiles de trabajo (`.claude/skills/profile-*`), un hook que vigila los commits de ficheros protegidos, la configuración del proyecto y un comando `/deploy` | El repositorio de un proyecto, sustituyendo cada `<placeholder>` |
| `docs/` | Esta documentación: la guía y el registro de reglas, en inglés y en español | A ninguna parte; es para leer |

## Cómo empezar

Hay dos rutas. La ruta guiada no necesita conocimientos técnicos. La ruta manual es para perfiles técnicos que quieren elegir y adaptar los ficheros ellos mismos.

### Ruta guiada (sin conocimientos técnicos)

Claude Code construye contigo tu propia versión y hace él mismo la parte técnica.

1. **Dale el enlace.** Abre Claude Code en tu proyecto y dale el enlace de este repositorio. Pídele que lo instale, o pregúntale sin más si te encaja. La frase de «Instálalo con tu agente de IA» también vale.
2. **Cuéntale qué te sale mal.** Te explica la idea y te hace unas cuantas preguntas, entre ellas qué te sale mal hoy con la IA. Eso es lo que decide si te ayuda. Te propone solo las piezas que encajan con tu proyecto.
3. **Revisa antes de que escriba.** Copia y adapta los ficheros él mismo. Te enseña lo que va a escribir antes de escribirlo y no sobrescribe tus ficheros. Claude Code te pide permiso cuando copia en `~/.claude`; es lo esperado.
4. **Haced juntos una primera tarea pequeña.** Acuerda contigo una primera tarea pequeña. Después abre una sesión nueva en el proyecto y di «empieza el onboarding» (`/harness-onboarding`). Hace contigo esa tarea tal como se harán todas y explica cada parte la primera vez que aparece.
5. **Ajústalo más adelante.** Para preguntar cómo funciona algo, añadir o quitar piezas o cambiar una preferencia, di «llama al harness keeper» (`/harness-keeper`).

Si prefieres arrancarlo a mano: clona o descarga este repositorio, copia `global/skills/init-harness/` en `~/.claude/skills/`, abre Claude Code en tu proyecto y ejecuta `/init-harness`. Te preguntará dónde has puesto la copia de este repositorio.

### Ruta manual (para perfiles técnicos)

1. **Lee antes de copiar.** Empieza por `global/skills/profile-director/SKILL.md` y `global/agents/worker.md`; ahí está todo el modelo.
2. **Copia y adapta la parte global.** Copia el contenido de `global/` en `~/.claude/`. Sustituye las entradas de ejemplo de `skills/new-feature/skills-index.md` por tus propias skills.
3. **Prepara un proyecto.** Copia `project-example/CLAUDE.md` y `project-example/.claude/` en tu proyecto y rellena los placeholders. Crea los comandos `/commit` y `/update-docs` del proyecto a partir de `global/templates/`. Quédate solo con los perfiles que tengan sentido para tu stack.
4. **Abre una sesión en el proyecto** y activa el director: «activa el perfil director» (puedes pedirlo con tus palabras y en tu idioma: el modelo se guía por el sentido).
5. **Dile lo que quieres**, como se lo dirías a un jefe de proyecto. Leerá el código, te preguntará lo que necesite para decidir y empezará a lanzar agentes.

## Para seguir leyendo

- [Guía](docs/guia.md): los roles, el informe, la vida de una tarea, los permisos, varios directores en paralelo y las preferencias opcionales.
- [Registro de reglas](docs/registro-de-reglas.md): cada regla con el fallo que la originó y por qué se resuelve así.

## Licencia

MIT. Consulta el fichero [LICENSE](LICENSE).
