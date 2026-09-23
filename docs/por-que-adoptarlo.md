# ¿Por qué probar PROVENANCE en investigación o evaluación académica?

PROVENANCE es una **propuesta en borrador**, no un estándar adoptado. Plantea una hipótesis verificable: registrar decisiones, alternativas, evidencia y límites podría ayudar a una persona ajena al trabajo a reconstruir lo ocurrido sin leer una conversación privada con IA. Aún no existe un estudio independiente que demuestre ese beneficio. El [protocolo de evaluación](evaluation-protocol.md) propone cómo medirlo.

La [matriz bibliográfica](evidence-base.md) enlaza artículos originales con estas ideas y precisa qué no permiten concluir.

## Investigación

Un equipo puede documentar por qué cambió un método, aplazó un análisis o limitó una conclusión. El registro vincula la decisión con fuentes y artefactos, las alternativas consideradas, participantes declarados y dudas pendientes. Su JSON permite detectar referencias internas ausentes; el Markdown generado facilita la revisión por colaboradores, asesores o revisores.

Ejemplo: el equipo aplaza comparar dos modelos porque una variable no estaba disponible en el momento requerido. Puede enlazar el protocolo versionado y un artefacto verificable. La explicación del equipo se marca `user_declared`; la coincidencia de bytes de un archivo, `tool_verified`; y una interpretación posterior, `system_inferred`, con su base y límites. Así queda visible qué se declaró, qué se comprobó y qué sigue siendo una interpretación.

Puede probarse en handoffs de laboratorio, cambios a análisis preespecificados, paquetes de reproducibilidad y respuestas a revisión. Complementa protocolos, cuadernos, historial Git y formatos como W3C PROV o RO-Crate. No certifica la validez científica ni que el historial esté completo.

La motivación para metadatos explícitos y artefactos enlazados aparece en los [principios FAIR](https://doi.org/10.1038/sdata.2016.18) y en [RO-Crate](https://doi.org/10.3233/DS-210053). Ninguno evaluó PROVENANCE.

## Exámenes, proyectos y defensas

Cuando el reglamento permite ayuda de IA, un estudiante podría entregar un registro pequeño de las decisiones que acepta declarar: qué alternativa eligió, qué evidencia revisó, qué apoyo utilizó y qué no puede concluir. El examinador puede usarlo para formular preguntas concretas. El trabajo y las respuestas del estudiante siguen siendo la base para evaluar comprensión según las reglas publicadas de la institución.

Ejemplo: una IA sugiere dos rutas de solución; el estudiante declara cuál eligió y adjunta el resultado de una prueba que inspeccionó. El registro conserva esa distinción. No demuestra quién escribió cada línea, si el estudiante comprendió el método ni si hubo ayuda no declarada. Tampoco debe usarse como detector de fraude o calificador automático.

Una institución debería anunciar de antemano la política de uso, permitir herramientas diferentes o ausencia de IA, exigir sólo datos pertinentes al objetivo educativo y ofrecer una forma de corregir registros erróneos. No debe exigir chats privados, razonamiento oculto, credenciales ni datos de terceros. Si una evidencia no puede compartirse por privacidad o propiedad intelectual, debe poder registrarse ese límite.

La [AI Assessment Scale](https://doi.org/10.53761/q3azde36) propone explicitar el uso permitido de IA según el objetivo de evaluación y cuenta con un [piloto en un contexto universitario](https://doi.org/10.14742/ajet.9434). Un [experimento aleatorizado en matemáticas](https://doi.org/10.1073/pnas.2422633122) muestra por qué hay que separar desempeño con ayuda de resultados sin ayuda. Un [estudio de detectores de texto IA](https://doi.org/10.1016/j.patter.2023.100779) documenta problemas de equidad en evaluación. Ninguno valida PROVENANCE.

## Qué puede comprobarse hoy

- Presencia de campos requeridos y referencias locales resolubles.
- Base y limitación explícitas para una inferencia.
- Coincidencia de SHA-256 y tamaño con los bytes de un artefacto empaquetado.
- Generación idéntica de Markdown con las mismas entradas.

Estas comprobaciones se refieren al **registro**. No autentican identidades, prueban la verdad de una afirmación, atribuyen autoría ni miden aprendizaje. La implementación de referencia tiene [brechas de conformidad conocidas](conformance.md) y la redacción de secretos no es exhaustiva.

## Antes de exigirlo

1. Probar la versión fija del borrador en escenarios sintéticos o consentidos y de bajo impacto.
2. Compararla con una nota libre o plantilla que ya se utilice.
3. Pedir a lectores independientes que reconstruyan decisiones, evidencia y límites; medir errores y tiempo de documentación.
4. Revisar privacidad y accesibilidad antes de conservar o compartir registros.
5. Comunicar también fallos y carga de trabajo antes de afirmar una mejora.

Tiene sentido **pilotar** PROVENANCE porque convierte estas preguntas en algo medible. Hacerlo obligatorio requiere resultados favorables en el contexto específico.
