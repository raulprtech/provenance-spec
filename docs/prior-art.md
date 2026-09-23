# Antecedentes primarios y frontera de novedad

Revisión localizada al 19 de septiembre de 2026. No es una revisión sistemática ni establece novedad.

## W3C PROV

La familia W3C PROV define un modelo interoperable centrado en entidades, actividades y agentes, con serializaciones, restricciones y extensiones. PROV-O permite especialización para dominios concretos. Por tanto, relacionar artefactos, actividades y participantes no puede presentarse como contribución nueva de PROVENANCE.

Fuentes primarias:

- W3C, [PROV Overview](https://www.w3.org/TR/prov-overview/), Working Group Note, 30 abril 2013.
- W3C, [PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/), Recommendation, 30 abril 2013.
- W3C, [PROV-DM: The PROV Data Model](https://www.w3.org/TR/prov-dm/), Recommendation, 30 abril 2013.

## Procedencia científica: RO-Crate

RO-Crate 1.3 define un paquete JSON-LD para agregar y describir datos y recursos de investigación, incluidas personas, organizaciones, software, equipo, workflows y acciones de procedencia. Ya cubre metadatos estructurados y una ruta de representación humana. PROVENANCE no debe afirmar haber inventado el empaquetado dual humano/máquina ni la vinculación de contribuyentes y artefactos.

Fuente primaria:

- Research Object community, [RO-Crate 1.3 specification](https://www.researchobject.org/ro-crate/specification/1.3/introduction.html), en especial la sección de procedencia de entidades.

## Procedencia de software: SLSA

SLSA define procedencia de build como una atestación sobre cómo se produjeron salidas, incluida la plataforma y parámetros externos. Su objetivo y modelo de amenaza son distintos del registro de decisiones colaborativas. Los hashes de v0.1 no equivalen a una atestación SLSA ni a una cadena de suministro segura.

Fuente primaria:

- SLSA, [Specification v1.1 — Terminology](https://slsa.dev/spec/v1.1/terminology).

## Procedencia de contenido: C2PA

C2PA liga afirmaciones y acciones a activos mediante manifiestos y firmas. Sus propios principios distinguen verificabilidad/ligadura de juicios de valor sobre si la procedencia es “buena” o “mala” y enfatizan privacidad y control. PROVENANCE v0.1 no implementa firmas ni Content Credentials.

Fuentes primarias:

- C2PA, [Content Credentials Technical Specification 2.3](https://spec.c2pa.org/specifications/specifications/2.3/specs/C2PA_Specification).
- C2PA, [Guiding Principles](https://c2pa.org/principles/).

## Hipótesis de contribución, aún no demostrada

La contribución candidata no es “provenance para IA” en general. Es un perfil mínimo y evaluable para registrar decisiones humano–IA sin capturar razonamiento privado, que:

1. obliga a separar `observed`, `user_declared`, `tool_verified` y `system_inferred`;
2. vincula decisiones, alternativas descartadas, evidencia y límites en una vista reconstruible;
3. evalúa representabilidad, reconstrucción documental y carga de documentación sin usar porcentajes de autoría ni aprendizaje supuesto.

Esta hipótesis necesita una búsqueda bibliográfica sistemática, comparación de perfiles y evaluación externa. El prototipo y el self-case sólo demuestran factibilidad técnica estrecha.

