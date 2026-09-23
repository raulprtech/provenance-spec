# Protocolo de evaluación v0.1

Estado: propuesta previa a estudio. No se ha ejecutado y no contiene resultados.

## Preguntas

- RQ1, representabilidad: ¿qué proporción de hechos documentales relevantes de escenarios autorizados puede expresarse sin campos libres que contradigan el modelo?
- RQ2, reconstrucción: ¿con qué exactitud puede un evaluador ajeno reconstruir decisiones, alternativas, evidencia y límites?
- RQ3, carga: ¿qué tiempo, esfuerzo percibido y fricción introduce el perfil frente a baselines?

No se pregunta quién es “más autor” ni si alguien aprendió.

## Materiales y muestreo

1. Congelar entre 12 y 20 escenarios breves, estratificados por número de decisiones, participantes y artefactos.
2. Usar escenarios sintéticos o públicos/licenciados; un caso privado sólo con consentimiento y versión redactada aprobada.
3. Excluir datos clínicos, credenciales, chats privados no autorizados y materiales con IP incierta.
4. Separar autores de registros, revisores de privacidad y evaluadores de reconstrucción.

El self-case de desarrollo puede encontrar defectos del esquema, pero no entra como observación independiente de eficacia ni demuestra aprendizaje.

## Condiciones

- B0: nota narrativa libre.
- B1: plantilla tabular simple (decisión, responsable, evidencia, fecha).
- P: PROVENANCE v0.1 JSON + Markdown.

Asignar escenarios/condiciones con orden contrabalanceado. Congelar instrucciones, límite de tiempo y criterio de corrección antes de observar resultados. Si se añade una condición W3C PROV o RO-Crate, documentar el perfil exacto y tratarla como comparador distinto, no como implementación equivalente.

## Gold standard y unidad de análisis

Dos anotadores construyen independientemente un inventario de unidades atómicas: decisión, estado, alternativa, responsable declarado, evidencia, artefacto, fuente, clase epistemológica y límite. Resuelven desacuerdos sin consultar al evaluador de reconstrucción. La unidad primaria es el hecho documental, no el documento completo.

## Métricas preespecificadas

### Representabilidad

- cobertura = unidades correctamente codificadas / unidades aplicables;
- tasa de extensión no prevista;
- tasa de ambigüedad interanotador por campo;
- referencias rotas y violaciones del validador por registro;
- incidentes de privacidad o secretos detectados antes/después de revisión.

### Reconstrucción

- precisión, recall y F1 micro sobre unidades atómicas;
- exactitud de clase (`observed`, `user_declared`, `tool_verified`, `system_inferred`);
- tasa de atribuciones/inferencias no respaldadas;
- exactitud de alternativas y límites;
- calibración de confianza y tasa de abstención.

### Carga

- minutos activos para documentar y revisar;
- número de correcciones hasta validación;
- escala breve de esfuerzo percibido, fijada antes del estudio;
- tamaño del registro y tiempo de lectura/reconstrucción.

## Análisis

- Reportar intervalos compatibles con el diseño y distribuciones, no sólo promedios.
- Usar comparaciones pareadas por escenario/participante cuando corresponda.
- Mantener separados errores del esquema, del generador, del documentador y del evaluador.
- Analizar cualitativamente omisiones y redacciones; no convertir ausencia de registro en ausencia de contribución.
- Declarar cambios posteriores a la congelación y no ajustar hipótesis después de ver resultados.

## Criterios de factibilidad antes de una afirmación

Un piloto sólo habilita avanzar si no hay incidentes graves de privacidad, las referencias son validables, los evaluadores distinguen las cuatro clases y la carga puede medirse de forma reproducible. Los umbrales numéricos para superioridad o no inferioridad deben fijarse con asesoría metodológica antes del estudio; v0.1 no los inventa.

## Salidas previstas

Protocolo congelado, diccionario de anotación, escenarios permitidos, registros por condición, reporte de errores, análisis reproducible y declaración de exclusiones. Ninguna salida debe contener chats privados, credenciales, datos clínicos ni evaluaciones de autoría individual.

