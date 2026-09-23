# Transparencia y confianza en artículos científicos

El enfoque inicial de PROVENANCE es documentar automáticamente la asistencia de IA capturada durante la preparación de un artículo científico, junto con las decisiones humanas y delegaciones explícitamente registradas. La captura automática y la organización por un modelo son **objetivos por implementar**, no capacidades actuales del prototipo.

## Transparencia no punitiva

Buscamos que usar IA sea transparente, pero que su mera utilización no se convierta en motivo para juzgar o castigar a quien la declara. Preferimos construir confianza en los procesos para compartir decisiones y delegaciones antes que buscar detectar su uso para sancionarlo.

Esto no significa que la ciencia sea inmune a la crítica: métodos, resultados y afirmaciones deben poder examinarse. Tampoco promete protección frente a terceros ni anula políticas editoriales. Es un compromiso de diseño, no un efecto demostrado.

La confianza es una condición de uso: explicar qué se captura, pedir consentimiento, minimizar datos, permitir pausas y correcciones, definir quién accede y cuánto tiempo conserva el registro, y revisar antes de compartir. Si el contexto no ofrece esas condiciones, no debemos presentarlo como un espacio seguro para declarar el uso de IA.

Un registro ausente o incompleto indica cobertura desconocida, no culpabilidad. No habrá puntuaciones de uso sospechoso, porcentajes de autoría ni clasificaciones morales del investigador. Ver [principios de confianza](trust-and-transparency.md).

## Qué queremos documentar

- Asistencia en bibliografía, ideas, métodos, código, análisis, interpretación, escritura, traducción, edición, figuras y respuestas a revisores.
- Parte y versión del artículo afectadas y evidencia disponible.
- Tarea delegada y límites de esa delegación.
- Aceptación, modificación, rechazo o decisión pendiente, distinguiendo acción capturada, declaración humana e interpretación del modelo.
- Lo que no se pudo observar, lo que se corrigió y lo que no puede compartirse.

“No registrado” no significa “no ocurrió”. Buscamos cubrir todas las intervenciones capturadas dentro del alcance declarado, no conocer todo el trabajo externo ni inventar intenciones.

## Ejemplo y salidas

Si una IA propone reformular un párrafo y el autor aplica una versión modificada, el registro puede describir esa acción y enlazar el cambio autorizado. No puede concluir que el autor verificó todas las afirmaciones ni atribuirle razones que no expresó.

Proponemos un registro de trabajo detallado y una declaración breve de uso de IA para el artículo, aprobada por los autores. Capturar automáticamente no significa publicar automáticamente. No se requieren chats completos ni razonamiento privado.

## Estado y siguiente etapa

El formato 0.1.0 y su generador JSON/Markdown existen; la integración con un editor, la captura automática, el resumen por un modelo y la aprobación de publicación todavía no. El [perfil propuesto](scientific-article-profile.md) define esa hoja de ruta. El validador tiene brechas y los adjuntos copiados no se saneaban automáticamente; no deben tratarse como seguros por pasar una comprobación del registro.

La [bibliografía](evidence-base.md) motiva problemas y antecedentes; no demuestra que PROVENANCE los resuelva. El [protocolo](evaluation-protocol.md) medirá cobertura, atribuciones falsas, esfuerzo de revisión y condiciones de confianza. ARIA y los exámenes quedan para un perfil posterior con evaluación propia; documentar asistencia no demuestra aprendizaje.
