# Importador EGO Round 2 → PROVENANCE v0.1

Estado: perfil offline acotado para el fixture sintético Round 2. No es un contrato estable con EGO.

## Entrada aceptada

El directorio fuente debe contener `producer-manifest.json` con protocolo `ego.offline-experiment-export/v1` y exactamente estas salidas:

- `plan-receipt.json`
- `status-receipt.json`
- `receipt.json`
- `learning-package.json`

El importador rechaza nombres no seguros, symlinks, archivos ausentes, tamaños o SHA-256 discordantes, protocolos no admitidos, cadenas de recibos inconsistentes y referencias internas de evidencia inexistentes. Otros archivos presentes no se copian por estar fuera del manifiesto.

También requiere un `import-request.json` explícito. Sus declaraciones se conservan como `user_declared`; no se fabrica una decisión humana a partir de recibos de herramientas.

## Mapeo epistemológico

| Entrada o transformación | Clase PROVENANCE | Límite |
|---|---|---|
| Valores leídos de recibos/learning package | `observed` | Se observó la declaración, no la ejecución. |
| Declaración explícita del operador | `user_declared` | No autentica identidad ni verdad. |
| Coincidencia con hash y tamaño del manifiesto | `tool_verified` | Integridad respecto al manifiesto suministrado, no autenticidad. |
| Interpretación upstream y secuencia reconstruida | `system_inferred` | Requieren base y límites visibles. |

Los tres recibos comparten timestamp. Por ello `plan→status→report` se documenta como reconstrucción semántica basada en `capability` y campos comunes, no como cronología verificada.

Los objetos `artifact_steps` y `artifact_digest` aparecen catalogados por URI/hash dentro del learning package, pero sus bytes no están en el export. Se conservan como fuentes referenciadas no verificadas. Una referencia a un identificador inexistente en el catálogo provoca rechazo.

## Privacidad y publicación

La salida sólo usa rutas relativas `artifacts/...`; no serializa la ruta fuente. Copia únicamente archivos declarados por el manifiesto y el propio manifiesto. No incluye otros archivos vecinos, chats, pacientes, test bloqueado ni credenciales.

El paquete educativo describe sesiones y ejercicios; no permite afirmar que alguien completó, comprendió, dominó o aprendió el contenido. Tampoco permite atribuir autoría. No se sube a arXiv ni a otro servicio.

## Uso

```bash
PYTHONPATH=src python3 src/ego_round2_importer.py   /ruta/al/export-round2   examples/ego_round2_import/public-package   --declaration-file examples/ego_round2_import/import-request.json
```

El destino debe no existir. La construcción ocurre en staging y sólo se materializa localmente mediante rename al completar toda la validación.
