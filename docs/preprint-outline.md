# Esqueleto de preprint (destino inicial: arXiv; sin envío autorizado)

Título provisional: **Observable Decision Provenance for Human–AI Collaboration: A Minimal, Privacy-Bounded Profile and Evaluation Protocol**

## Resumen

Problema, distinción entre procedencia observable y atribución/autenticidad, perfil v0.1, protocolo de evaluación y resultados pendientes. No incluir resultados hasta ejecutar el protocolo preregistrado o congelado.

## 1. Introducción

- Necesidad de reconstruir decisiones y evidencia en trabajo humano–IA.
- Riesgos de narrativas post hoc, captura excesiva y confusión entre registro, autoría, autenticidad y aprendizaje.
- Preguntas de investigación sobre representabilidad, reconstrucción y carga.
- Contribuciones formuladas como artefacto/protocolo hasta contar con resultados.

## 2. Trabajo relacionado

- W3C PROV: entidades, actividades, agentes, derivaciones y especialización.
- RO-Crate: empaquetado de objetos de investigación y procedencia de entidades.
- SLSA: atestaciones de procedencia de build.
- C2PA: procedencia vinculada criptográficamente a contenido y límites de interpretación.
- Literatura pendiente: explicaciones de sistemas de IA, documentación de decisiones, cuadernos electrónicos, reproducibilidad y autoría académica.

## 3. Requisitos y amenazas

- Modelo de información observable.
- Separación epistemológica de cuatro clases.
- Privacidad, secretos, IP, referencias rotas, historia fabricada y falsa certeza.
- No objetivos: cadena de pensamiento, puntuación de autoría, aprendizaje, identidad y verdad.

## 4. Perfil PROVENANCE v0.1

- Modelo JSON y reglas semánticas.
- Transformación determinista a Markdown.
- Cálculo de hashes y alcance exacto de `tool_verified`.
- Mapeo exploratorio, no normativo, a W3C PROV/RO-Crate.

## 5. Implementación de referencia

- Biblioteca estándar, operación offline, rutas confinadas.
- Validación de referencias e inferencias.
- Redacción defensiva y sus falsos negativos/positivos.
- Caso sintético reproducible.

## 6. Evaluación

- Corpus de escenarios autorizados, sintéticos y/o públicos.
- Tareas de codificación y reconstrucción por evaluadores que no participaron.
- Medidas de cobertura, exactitud con abstención, tiempo, carga subjetiva y desacuerdo.
- Baselines preregistrados: nota libre y plantilla simple; opcionalmente un perfil W3C PROV/RO-Crate adaptado si es viable.
- Análisis de errores y eventos de privacidad.

## 7. Resultados

Marcadores pendientes para resultados cuantitativos y cualitativos. El ejemplo del repositorio no se reporta como evidencia de eficacia, novedad o aprendizaje.

## 8. Discusión

- Qué puede reconstruirse y qué permanece desconocido.
- Coste de documentar frente a utilidad posterior.
- Interoperabilidad, autenticación y firmas como trabajo futuro.
- Riesgos de vigilancia y uso indebido en evaluación laboral/académica.

## 9. Limitaciones y ética

- Sesgo de selección de escenarios y participantes.
- Autodeclaraciones, omisiones y dependencia de la calidad de entrada.
- Redacción incompleta, reidentificación e IP.
- Prohibición de inferir autoría, desempeño individual o aprendizaje.

## 10. Disponibilidad y reproducibilidad

Versión congelada, esquema, generador, fixtures sintéticos, scripts de análisis y protocolo, sujetos a revisión de licencia/privacidad. No prometer apertura de materiales no autorizados.

