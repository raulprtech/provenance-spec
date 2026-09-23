# PROVENANCE v0.1: especificación mínima

Estado: propuesta pública de especificación 0.1.0, en borrador. No es un estándar adoptado ni un formato estable.

## Alcance actual del proyecto

La aplicación inicial se reenfoca en artículos científicos: asistencia de IA capturada, decisiones humanas explícitas y delegaciones acotadas, bajo principios de transparencia no punitiva y confianza. Ver el [perfil propuesto](scientific-article-profile.md) y los [principios de confianza](trust-and-transparency.md).

Las reglas del formato 0.1.0 que siguen se conservan sin cambios. No implementan todavía captura automática, intervenciones estructuradas, cobertura, aprobación de divulgación ni el resumen por un modelo. Esas capacidades requieren un contrato versionado posterior. Exámenes y ARIA quedan fuera de la primera etapa.

## 1. Propósito y no objetivos

PROVENANCE v0.1 registra lo que una colaboración declara u observa acerca de decisiones, alternativas, evidencia, fuentes, participantes y artefactos. Mantiene una representación JSON y deriva de ella una vista Markdown legible.

No intenta:

- capturar cadena de pensamiento, razonamiento privado ni chats completos;
- estimar porcentaje de contribución de IA, puntuación de autoría o propiedad intelectual;
- inferir como hecho que una persona aprendió, comprendió o estuvo de acuerdo;
- autenticar identidades, firmar contenido o demostrar la verdad de una declaración;
- reemplazar W3C PROV, RO-Crate, C2PA o mecanismos de procedencia de compilación;
- depender de ARIA, aunque ARIA pueda ser un futuro productor/consumidor.

## 2. Clases epistemológicas

Cada elemento de evidencia declara exactamente una clase:

| Clase | Significado operativo | Lo que no implica |
|---|---|---|
| `observed` | El registrador declara haber observado el elemento o una fuente. | Verdad, exhaustividad o autenticidad. |
| `user_declared` | Una persona, o el autor del fixture en su nombre, declaró el contenido. | Verificación independiente. |
| `tool_verified` | Una operación determinista verificó una propiedad estrecha, como bytes y hash. | Veracidad semántica, identidad o autoría. |
| `system_inferred` | El sistema derivó una interpretación de bases citadas. | Hecho, intención privada ni conocimiento del usuario. |

Una `system_inferred` requiere `inference_basis` visible y al menos una limitación. Las otras clases no pueden llevar `inference_basis`, para evitar presentar una declaración o verificación como inferencia ambigua.

## 3. Modelo

El documento raíz contiene:

- identidad/versionado y fecha aportada por el registro;
- alcance, uso previsto y exclusiones;
- participantes declarados con tipo, rol y procedencia de la declaración;
- fuentes con localizador y clasificación;
- artefactos con ruta relativa, tipo, rol, tamaño y SHA-256 verificado;
- evidencia clasificada con referencias resolubles;
- decisiones con estado, responsables declarados, resumen de justificación, alternativas, evidencia y límites;
- límites globales y bitácora de redacciones.

Los identificadores son locales al documento. Todas las referencias deben resolver. Las rutas de artefacto deben permanecer dentro de `--base-dir`: no se aceptan rutas absolutas, `~` ni segmentos `..`.

## 4. Flujo determinista

`build` ejecuta, en orden:

1. copia profunda de la entrada;
2. redacción conservadora de claves sensibles y patrones conocidos;
3. lectura de cada ruta de artefacto aportada y cálculo de SHA-256/tamaño;
4. orden canónico de colecciones por `id`;
5. validación estructural y semántica;
6. serialización JSON con claves ordenadas y generación de Markdown.

Con los mismos bytes de entrada y artefactos, las salidas son idénticas. El programa no agrega hora actual, autores, decisiones ni explicaciones no aportadas.

## 5. Privacidad, secretos e IP

La redacción cubre claves comunes (`api_key`, `token`, `password`, `secret`, `private_key`, `authorization`) y patrones seleccionados de tokens/Bearer/llaves privadas. Es una defensa parcial, no un detector completo. La revisión humana antes de compartir sigue siendo obligatoria.

No deben incorporarse chats privados, prompts confidenciales, datos personales o clínicos, credenciales, materiales sin permiso ni rutas personales innecesarias. El caso abierto incluido es sintético. Los campos `chain_of_thought`, `private_reasoning`, `reasoning_trace`, `ai_percentage`, `authorship_score` y `learning_score` se rechazan.

## 6. Integridad y confianza

Un hash local permite detectar cambio de bytes frente al valor registrado. No prueba quién creó el archivo, cuándo ocurrió la decisión ni si la narración es completa. v0.1 no firma registros, no usa una bitácora inmutable y no valida URLs. Cualquier perfil posterior de confianza debe mantener separadas asociación criptográfica, identidad y verdad semántica.

## 7. Compatibilidad futura

El mapeo a W3C PROV es investigación futura: artefactos/fuentes podrían corresponder a `Entity`, acciones de registro a `Activity` y participantes a `Agent`. Esa analogía no se codifica todavía para no prometer interoperabilidad no probada. RO-Crate puede empaquetar resultados de investigación; C2PA puede ser relevante para credenciales ligadas a activos; SLSA cubre procedencia de builds. PROVENANCE v0.1 se limita a decisiones y evidencia documental observable.

