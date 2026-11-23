# claude-code-director-harness

[Read in English](README.md)

> **Proyecto en desarrollo.** Este repositorio todavía está tomando forma y en pruebas, así que puede cambiar. No acepta contribuciones (los issues y los pull requests están cerrados), pero eres libre de copiarlo y adaptarlo a tus necesidades; esa es la idea.

## Instálalo con tu agente de IA

Abre Claude Code en tu proyecto y dile: «Instala el harness de director de https://github.com/enadan-gh/claude-code-director-harness en este proyecto.» Necesitas Claude Code, porque el harness se compone de skills y agentes de Claude Code.

### Instrucciones para el agente

Si un usuario te ha dado la URL de este repositorio y te ha pedido instalarlo en su proyecto, haz esto, en orden:

1. No instales nada todavía en el proyecto del usuario. Explícale, en una o dos frases sencillas, qué es esto (una sesión director que planifica con él y reparte el trabajo entre agentes auxiliares, revisando lo que ha cambiado de verdad y llevando un informe escrito) y que ahora vas a hacerle una entrevista para construir su propia versión.
2. Averigua si el usuario usa git. Si no lo usa, explícale en dos frases sencillas qué le aporta (puede deshacer cualquier cosa y ver exactamente qué ha cambiado la IA) y respeta su decisión; la skill init-harness se ocupa del resto.
3. Consigue una copia local de este repositorio FUERA del proyecto del usuario. Antes de descargar o clonar nada, pregúntale al usuario dónde ponerla (propón, por ejemplo, `~/claude-code-director-harness`). Después, si hay git disponible, ejecuta `git clone https://github.com/enadan-gh/claude-code-director-harness.git` en esa carpeta; sin git, descarga y descomprime allí <https://github.com/enadan-gh/claude-code-director-harness/archive/refs/heads/main.zip>.
4. Copia `global/skills/init-harness/` de esa copia a `~/.claude/skills/init-harness/`. Avisa al usuario de que aparecerá una petición de permiso porque `~/.claude` está protegida, y de que es lo esperado. Si esa carpeta ya existe, no la sobrescribas: díselo al usuario y usa la existente solo si es idéntica a la copia; si no, pregunta.
5. Una skill copiada durante una sesión se detecta en esa misma sesión: ejecuta `/init-harness` ahora, usando la copia local del paso 3 como repositorio de referencia (`<repo>`). Si `/init-harness` no está disponible, lee la copia `~/.claude/skills/init-harness/SKILL.md` y síguela paso a paso. No le pidas al usuario que reinicie.
6. Sigue las reglas de esa skill: lenguaje sencillo, pocas preguntas cada vez y en el chat, enseña cada fichero antes de escribirlo y no sobrescribas nunca.

Es la misma ruta guiada que se describe en «Cómo empezar», conducida por tu agente.

Así es como trabajo con Claude Code. Desarrollo productos reales yo solo, con Claude Code dentro de VS Code, y unos amigos me preguntaron cómo lo organizo. En lugar de explicarlo una y otra vez, he dejado aquí los ficheros que uso de verdad, limpios de todo lo personal y con comentarios sobre por qué existe cada pieza.

## Qué es

Un ejemplo comentado de una forma de trabajar: una sesión de Claude Code hace de **director**, que habla conmigo, decide conmigo y reparte el trabajo entre **agentes que se ejecutan en segundo plano**, y luego revisa lo que entregan. En una línea: es como hablar con un jefe de proyecto que ha repartido el trabajo entre su equipo.

El repositorio contiene los ficheros que lo hacen posible: una skill para el director, dos definiciones de agente (`worker` y `quick-fixer`), los comandos de flujo de trabajo que siguen los agentes, plantillas para comandos de cada proyecto y un ejemplo completo de lo que lleva el repositorio de un proyecto (su `CLAUDE.md`, perfiles de trabajo, un hook propio y un comando de despliegue).

No contiene skills de lenguajes ni de frameworks, y no es un paquete que se instale.

## Para quién es

Para quien ya usa Claude Code en trabajo real y quiere ver una manera concreta de organizarlo: cómo mantener vivo un hilo largo de decisiones a través de compactaciones y chats nuevos, cómo delegar tareas en agentes en segundo plano sin perder el control y cómo evitar que las peticiones de permiso te interrumpan todo el día.

Si estás empezando con Claude Code, la documentación oficial es mejor primer paso. Esto viene después.

## Adapta, no copies

Esto es lo que me funciona a mí, en mi contexto: una persona, varios productos, un único árbol de trabajo por proyecto. No es una receta, y no está pensado para instalarlo y usarlo tal cual.

Varias piezas son preferencias personales (cómo me hace preguntas el agente, qué modelo usa cada agente, cuándo se escriben los tests, cuánta limpieza puede hacer un agente). En la [guía](docs/guia.md) las presento como opciones y explico por qué elegí cada una, para que decidas qué encaja con tu forma de trabajar o la de tu equipo. Quédate con las ideas, lee los ficheros y reescríbelos a tu manera.

## El modelo de trabajo

Abro una sesión de Claude Code en el proyecto y activo el perfil de director. A partir de ahí yo solo hablo y decido. El director lee el código real antes de opinar, me plantea las opciones con su coste real y una recomendación, y registra cada decisión que tomo, con mi motivo y con mis propias palabras.

Cuando algo queda decidido, el director escribe un **brief**: la descripción autocontenida de la tarea, con las decisiones cerradas, lo que queda fuera de alcance y cómo debe terminar. Lanza en segundo plano un agente `worker` con ese brief (o un `quick-fixer`, un agente más barato, para arreglos pequeños ya diagnosticados). El agente ejecuta la tarea entera sin pararse: plan, implementación, verificación, commit y push, cierre de documentación y un informe final breve. Mientras tanto, el director sigue disponible para mí y prepara el siguiente brief.

Cuando el agente termina, el director **revisa la entrega sobre el diff real**, nunca sobre el resumen del agente. Lee los commits, repite él mismo las comprobaciones clave y aprueba o devuelve correcciones al mismo agente. Cada ronda de esta revisión ha encontrado algo que el resumen no mencionaba.

Todo vive en un único **informe**: un fichero markdown en el proyecto con el contexto, la tabla de decisiones, la cola de tareas, el diario de sesión y un guion de pruebas acumulado. El informe es la memoria del director. Sobrevive a las compactaciones de contexto y a los chats nuevos: si mañana abro otra sesión, le señalo el informe al director y retoma el hilo. Además ahorra tokens después de una pausa: cuando la caché de prompts ha caducado, cualquier mensaje en la conversación antigua la vuelve a enviar entera, mientras que una sesión nueva solo tiene que leer el informe (detalles en la [guía](docs/guia.md)).

## Mapa del repositorio

| Carpeta | Qué contiene | Adónde va |
| --- | --- | --- |
| `global/` | La skill del director (`skills/profile-director/`), las tres skills de la ruta guiada (`skills/init-harness/`, `skills/harness-onboarding/`, `skills/harness-keeper/`), los agentes (`agents/worker.md`, `agents/quick-fixer.md`), los comandos de flujo (`commands/do-feature.md`, `commands/fix-bug.md`, `commands/rework.md`) y la skill `new-feature` con su índice de skills | `~/.claude/`, con las mismas subcarpetas |
| `global/templates/` | `commit.md` y `update-docs.md`: plantillas, no comandos | El original se queda en `~/.claude/templates/`; una copia adaptada va al `.claude/commands/` de cada proyecto |
| `optional/` | `Explore`, que sustituye al agente Explore integrado solo para elegir modelo y esfuerzo, y `web-fetch`, un agente ligero adicional que lee páginas web públicas con un modelo más barato | `~/.claude/agents/`, si los quieres |
| `project-example/` | Lo que lleva el repositorio de un proyecto: una plantilla de `CLAUDE.md`, cinco perfiles de trabajo (`.claude/skills/profile-*`), un hook que vigila los commits de ficheros protegidos, la configuración del proyecto y un comando `/deploy` | El repositorio de un proyecto, sustituyendo cada `<placeholder>` |
| `docs/` | Esta documentación: la guía y el registro de reglas, en inglés y en español | A ninguna parte; es para leer |

## Cómo empezar

1. **Lee antes de copiar.** Empieza por `global/skills/profile-director/SKILL.md` y `global/agents/worker.md`; ahí está todo el modelo.
2. **Copia y adapta la parte global.** Copia el contenido de `global/` en `~/.claude/`. Sustituye las entradas de ejemplo de `skills/new-feature/skills-index.md` por tus propias skills.
3. **Prepara un proyecto.** Copia `project-example/CLAUDE.md` y `project-example/.claude/` en tu proyecto y rellena los placeholders. Crea los comandos `/commit` y `/update-docs` del proyecto a partir de `global/templates/`. Quédate solo con los perfiles que tengan sentido para tu stack.
4. **Abre una sesión en el proyecto** y activa el director: «activa el perfil director» (puedes pedirlo con tus palabras y en tu idioma: el modelo se guía por el sentido).
5. **Dile lo que quieres**, como se lo dirías a un jefe de proyecto. Leerá el código, te preguntará lo que necesite para decidir y empezará a lanzar agentes.

**Ruta guiada.** En lugar de copiar a mano, puedes dejar que Claude Code construya contigo tu propia versión: clona o descarga este repositorio, copia `global/skills/init-harness/` en `~/.claude/skills/`, abre Claude Code en tu proyecto y ejecuta `/init-harness`. Te explica el modelo, te hace unas cuantas preguntas, propone solo las piezas que encajan con tu proyecto y te muestra cada fichero antes de escribirlo (te preguntará dónde has clonado este repositorio). También acuerda contigo una primera tarea pequeña. Después abre una sesión nueva en el proyecto y di «empieza el onboarding» (`/harness-onboarding`): hace contigo esa primera tarea tal como se harán todas, explicando cada parte la primera vez que aparece. Más adelante, para preguntar cómo funciona algo, añadir o quitar piezas o cambiar una preferencia, di «llama al harness keeper» (`/harness-keeper`).

## Para seguir leyendo

- [Guía](docs/guia.md): los roles, el informe, la vida de una tarea, los permisos, varios directores en paralelo y las preferencias opcionales.
- [Registro de reglas](docs/registro-de-reglas.md): cada regla con el fallo que la originó y por qué se resuelve así.

## Licencia

MIT. Consulta el fichero [LICENSE](LICENSE).
