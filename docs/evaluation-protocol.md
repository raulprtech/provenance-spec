# Protocolo de evaluación: asistencia de IA en artículos científicos

Estado: diseño previo a estudio, sin resultados. Evalúa el perfil propuesto; requiere un prototipo de captura y resumen que aún no existe. No es una evaluación de exámenes ni de ARIA.

## Preguntas y alcance

- ¿Qué intervenciones capturables registra y resume correctamente el sistema?
- ¿Distingue asistencia, delegación, acción humana, declaración e inferencia sin inventar decisiones?
- ¿Cuánto trabajo humano exige revisar el registro y preparar una declaración publicable?
- ¿Las condiciones de captura y uso permiten compartir con confianza y sin presión?

No se mide autoría, aprendizaje, fraude ni si un investigador “usó demasiada IA”. La confianza no se deduce de cuántos eventos declara.

## Fase exploratoria

Preparar entre 12 y 20 escenarios sintéticos de elaboración de artículos. Incluir bibliografía, métodos, código, análisis, redacción y revisión; aceptación, modificación, rechazo, delegación, pendientes y correcciones. Esto es un piloto de factibilidad, no una muestra suficiente por definición para demostrar eficacia.

Incluir omisiones, trabajo externo, pérdida de eventos, tiempos desconocidos, versiones conflictivas, historia fabricada retrospectivamente, atribuciones no respaldadas, material sensible ficticio e instrucciones maliciosas dentro de las fuentes. No usar datos clínicos, credenciales reales, manuscritos confidenciales ni chats privados no autorizados.

## Referencia y condiciones comparables

Dos anotadores independientes del sistema construyen el inventario de referencia a partir de un guion o registro autorizado: intervenciones, elementos del artículo, delegaciones, decisiones explícitas, evidencia y cobertura. Resuelven desacuerdos antes de puntuar salidas. Separar autores de escenarios, revisores de privacidad y evaluadores.

Comparar B0 (declaración narrativa manual), B1 (tabla de tarea, asistencia, elemento afectado, decisión y evidencia) y P (captura más resumen asistido y revisión humana). Dar acceso a la misma evidencia y los mismos objetivos de divulgación; contrabalancear orden. Medir por separado captura, resumen y revisión: el formato no debe recibir crédito por disponer de más información que el comparador.

Un perfil PROV/RO-Crate documentado puede añadirse como comparación de representación. No asumir interoperabilidad por semejanza de campos.

## Métricas

- Resultado principal propuesto: recall de intervenciones correctamente representadas, por escenario, dentro de la cobertura capturable acordada.
- Salvaguarda principal: proporción de afirmaciones sobre decisiones humanas sin respaldo; informar también recuentos, denominadores y tipos de error.
- Precisión de intervenciones, atribución de actor, distinción entre delegación y aprobación, y clasificación de estados.
- Omisiones de límites, referencias inválidas y errores separados por captura, modelo, esquema y revisor.
- Minutos activos de revisión, correcciones necesarias y esfuerzo percibido con instrumento fijado previamente.
- Divulgaciones sensibles ficticias en el registro, los adjuntos y la declaración final.
- Seguridad percibida para compartir, comprensión de destinatarios y usos, disposición voluntaria a participar y motivos de exclusión o abandono.

No confundir exactitud con autenticidad: un paquete fabricado puede ser internamente coherente. Tampoco confundir satisfacción con eficacia o consentimiento con ausencia de presión.

## Análisis y criterios

La unidad independiente es el escenario y, cuando intervengan personas, se considera también el participante; los eventos dentro de ellos no cuentan como réplicas independientes. Reportar distribuciones e intervalos adecuados al agrupamiento y comparaciones pareadas cuando proceda.

Antes de un estudio confirmatorio, congelar endpoint, umbrales mínimos de cobertura y máximos de atribución falsa, plan de análisis y tamaño de muestra justificado. Registrar los cambios respecto del piloto; no elegir umbrales después de conocer resultados.

Un incidente grave de privacidad o publicación no autorizada detiene la fase afectada hasta corregir y volver a verificar. No avanzar a afirmaciones de eficacia sin comparación justa e independiente. Mantener separados los resultados técnicos y las hipótesis sobre confianza.

## Condiciones de confianza y salidas

Los participantes conocen acceso, retención, corrección y usos permitidos; pueden limitar captura sin que eso se convierta en señal adversa. El piloto no usa sus registros para puntuar uso de IA ni castigar la divulgación. Si las políticas reales contradicen este acuerdo, no presentar el piloto como no punitivo.

Publicar sólo materiales sintéticos o expresamente autorizados: protocolo, diccionario de anotación, errores, tiempos y resultados agregados. Ningún resultado se transfiere automáticamente a exámenes, aprendizaje o decisiones disciplinarias.
