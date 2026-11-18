# claude-code-director-harness

[Read in English](README.md)

Así es como trabajo con Claude Code. Desarrollo productos reales yo solo, con Claude Code dentro de VS Code, y unos amigos me preguntaron cómo lo organizo. En lugar de explicarlo una y otra vez, he dejado aquí los ficheros que uso de verdad, limpios de todo lo personal y con comentarios sobre por qué existe cada pieza.

## Qué es

Un ejemplo comentado de una forma de trabajar: una sesión de Claude Code hace de **director**, que habla conmigo, decide conmigo y reparte el trabajo entre **agentes que se ejecutan en segundo plano**, y luego revisa lo que entregan. En una línea: es como hablar con un jefe de proyecto que ha repartido el trabajo entre su equipo.

El repositorio contiene los ficheros que lo hacen posible: una skill para el director, dos definiciones de agente (`worker` y `quick-fixer`), los comandos de flujo de trabajo que siguen los agentes, plantillas para comandos de cada proyecto, un hook de seguridad, una configuración de ejemplo y un ejemplo completo de lo que lleva el repositorio de un proyecto (su `CLAUDE.md`, perfiles de trabajo, un hook propio y un comando de despliegue).

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
| `global/` | La skill del director (`skills/profile-director/`), los agentes (`agents/worker.md`, `agents/quick-fixer.md`), los comandos de flujo (`commands/do-feature.md`, `commands/fix-bug.md`, `commands/rework.md`), la skill `new-feature` con su índice de skills, el hook `rm-md-guard.sh` y `settings.example.json` | `~/.claude/`, con las mismas subcarpetas. `settings.example.json` se fusiona con tu `~/.claude/settings.json`, no lo sustituye |
| `global/templates/` | `commit.md` y `update-docs.md`: plantillas, no comandos | El original se queda en `~/.claude/templates/`; una copia adaptada va al `.claude/commands/` de cada proyecto |
| `optional/` | `Explore`, que sustituye al agente Explore integrado solo para elegir modelo y esfuerzo, y `web-fetch`, un agente ligero adicional que lee páginas web públicas con un modelo más barato | `~/.claude/agents/`, si los quieres |
| `project-example/` | Lo que lleva el repositorio de un proyecto: una plantilla de `CLAUDE.md`, cinco perfiles de trabajo (`.claude/skills/profile-*`), un hook que vigila los commits de ficheros protegidos, la configuración del proyecto y un comando `/deploy` | El repositorio de un proyecto, sustituyendo cada `<placeholder>` |
| `docs/` | Esta documentación: la guía y el registro de reglas, en inglés y en español | A ninguna parte; es para leer |

## Cómo empezar

1. **Lee antes de copiar.** Empieza por `global/skills/profile-director/SKILL.md` y `global/agents/worker.md`; ahí está todo el modelo.
2. **Copia y adapta la parte global.** Copia el contenido de `global/` en `~/.claude/`. Fusiona en tu configuración el registro del hook y las reglas de denegación de `settings.example.json`. El hook necesita `jq` instalado. Sustituye las entradas de ejemplo de `skills/new-feature/skills-index.md` por tus propias skills.
3. **Prepara un proyecto.** Copia `project-example/CLAUDE.md` y `project-example/.claude/` en tu proyecto y rellena los placeholders. Crea los comandos `/commit` y `/update-docs` del proyecto a partir de `global/templates/`. Quédate solo con los perfiles que tengan sentido para tu stack.
4. **Abre una sesión en el proyecto** y activa el director: «activate the director profile» o «director mode» (son las frases que lista la descripción de la skill; si quieres pedirlo en español, añádelas allí).
5. **Dile lo que quieres**, como se lo dirías a un jefe de proyecto. Leerá el código, te preguntará lo que necesite para decidir y empezará a lanzar agentes.

Está previsto un comando de instalación interactivo que pregunte por las preferencias opcionales y genere los ficheros.

## Para seguir leyendo

- [Guía](docs/guia.md): los roles, el informe, la vida de una tarea, los permisos, varios directores en paralelo y las preferencias opcionales.
- [Registro de reglas](docs/registro-de-reglas.md): cada regla con el fallo que la originó y por qué se resuelve así.
