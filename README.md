# Automatización del blog — flujo semanal

Pipeline de **investigación → curación → redacción → revisión** para el artículo de
resumen semanal del blog de la empresa (WordPress, español + inglés).

## Cómo lanzar cada semana

Elige un día fijo (ej. lunes 9:00) y pega esto en la sesión:

```text
Genera el boletín semanal del blog. Sigue README.md:
1. Lee fuentes.md, guia-estilo.md, plantilla-articulo.md y checklist-revision.md.
2. Investiga en las fuentes oficiales lo publicado en los últimos 7 días sobre innovación e IA (EE. UU., Europa y Asia).
3. Dame una lista curada de 8–12 destacados (empresa — qué — enlace oficial — fecha) y espera mi aprobación.
4. Con mi OK, redacta el artículo en español con la plantilla y luego la versión en inglés.
5. Revisa ambos contra checklist-revision.md y guarda el entregable en articulos/AAAA-MM-DD/.
6. Ejecuta python generate_audio_tts.py para generar el guion de locución y el audio del podcast.
```

## Fases del flujo

| Fase | Qué ocurre | Control humano |
|---|---|---|
| 1. Investigación | Se rastrea la lista de fuentes oficiales (`fuentes.md`) buscando publicaciones de los últimos 7 días sobre IA e innovación. | — |
| 2. Curación | Se filtran 8–12 destacados: solo lanzamientos, papers, resultados y anuncios con enlace oficial verificable. | **Aprobación**: tú validas la selección antes de escribir. |
| 3. Redacción ES | Se escribe texto 100 % original siguiendo `plantilla-articulo.md` y `guia-estilo.md`, citando las fuentes. | — |
| 4. Versión EN | Adaptación al inglés (no traducción literal), misma estructura y fuentes. | — |
| 5. Revisión | Auto-revisión contra `checklist-revision.md`: exactitud, cobertura, estilo, SEO, formato WordPress. | Informe de revisión incluido en el entregable. |
| 6. Entrega y Audio | Archivos guardados en `articulos/AAAA-MM-DD/` (Markdown, HTML para WordPress y podcast MP3 generado con `generate_audio_tts.py`). | Tú publicas (o me lo pides vía API). |

## Reglas de la casa

1. **Solo fuentes oficiales**: newsroom, blog corporativo, laboratorio de la empresa,
   página de producto propia o repositorio GitHub oficial. No agencias, no blogs de
   terceros, no rumorology (salvo que la propia empresa lo confirme).
2. **Todo dato enlazado**: cada afirmación factual lleva su cita. Las citas de
   textos en chino/japonés se traducen y se enlaza el original.
3. **Texto nuevo, nunca plagiado**: se resumes y se interpreta; la fuente conlleva
   el crédito. Citas literales solo entre comillas y limitadas.
4. **Portafolio equilibrado**: mínimo 3 destacados de empresas de Asia en cada
   número; cubrir AI + innovación (chips, robótica, cloud, productos).
5. **Ventana temporal**: solo contenido de los últimos 7 días; lo más antiguo solo
   como contexto marcado como tal.

## WordPress

- Entregable por defecto: Markdown + HTML compatible con el editor de
  WordPress (etiquetas simples `h2/h3/p/ul/figure/blockquote`, incluidos
  meta título, meta descripción, tags y categorías sugeridas).
- Opcional: si me das la URL del sitio y un *Application Password* de un usuario
  con rol autor, puedo crear el borrador directamente vía REST API de WordPress
  (`/wp-json/wp/v2/posts`, `status: draft`) sin publicarlo.

## Estructura de carpetas

```text
blog-automation-app/
  README.md                 ← este archivo (flujo + comando semanal)
  fuentes.md                ← lista maestra de fuentes oficiales (EE. UU., Europa, Asia)
  guia-estilo.md            ← voz, estilo, reglas de citación, SEO
  plantilla-articulo.md     ← esqueleto del artículo y front matter
  checklist-revision.md     ← rúbrica de revisión antes de entrega
  generate_audio_tts.py     ← generador de guion de locución y audio MP3 (podcast)
  articulos/
    AAAA-MM-DD/             ← un boletín por fecha
      articulo.md           ← versión en español
      articulo-en.md        ← versión en inglés
      wordpress-es.html     ← HTML listo para pegar (ES)
      wordpress-en.html     ← HTML listo para pegar (EN)
      revision.md           ← resultado de la revisión contra el checklist
      guion-locucion.txt    ← guion limpio/adaptado para narración por voz
      podcast-episodio.mp3  ← episodio de audio sintetizado
```
