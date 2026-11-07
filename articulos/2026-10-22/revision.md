# Revisión del boletín — 22 de octubre de 2026

Revisión aplicada sobre `articulo.md` (ES), `articulo-en.md` (EN), `wordpress-es.html` y `wordpress-en.html`
según `checklist-revision.md`. Cada versión revisada de forma independiente; el conteo de palabras excluye
la sección de Fuentes y las URLs.

## 1. Exactitud factual

- [x] Todo dato, cifra y cita tiene su referencia numerada [1]–[16] y enlace a fuente oficial.
- [x] 15 de 16 fuentes verificadas por fetch directo en esta sesión (Cloudflare ×3, OpenAI ×2, Microsoft ×2,
      AWS, NVIDIA, JD.com, Google ×2, DeepSeek, Hugging Face ×2).
- [~] **Fuente [2] (php.net)**: no se pudo fetch directo en la pasada final; la URL de anclaje sale enlazada
      desde la nota oficial de Cloudflare [1]. Pendiente: confirmar visualmente la página antes de publicar.
- [x] Números cotejados con la fuente: 70 % (w3techs vía Cloudflare), versiones PHP 8.5.12/8.4.27/8.3.36/8.2.35,
      WAF por defecto 03:02 UTC (~9 h antes de la divulgación), ~100.000 dominios de Commerce.com, ¥5/1.000,
      223 tareas, 2.651 rúbricas, 25 servicios por ALB, 90 %/85 % (Porsche), 40×/99,99 %/95 % (cuántica),
      $368 B/+17 %/$1 B en 2035, 243 M usuarios (58 %), 75 % compra agéntica.
- [~] **Tabla de resultados BlenderWorld** (GPT-6-Astra 79,9; tope 42,2 %; DeepSeek 66,0; Qwen3.8-Max 61,1):
      leída en la página del paper (`huggingface.co/papers/2610.23986`) durante la fase de investigación;
      no se re-verificó en el último lote de fetches. Fuente citada: [8].
- [~] **"GA en las próximas semanas"** (OpenAI en Google Cloud) registrado del anuncio oficial [6] durante la
      investigación; coherente con el texto del anuncio, no re-verificado en la pasada final.
- [x] Fechas dentro de la ventana 15–22 oct: 15 (Google cuántica, JD), 17 (DeepSeek), 19 (Microsoft seguridad),
      20 (AWS, Microsoft soberanía), 21 (Cloudflare ×2, OpenAI ×2, NVIDIA, Google e-Conomy).
      Corrección aplicada: **NVIDIA Cosmos es del 21 de octubre** (la planificación inicial decía 22).
- [x] Sin datos inventados, sin "se dice que", sin conjeturas como hecho; las interpretaciones viven
      en "Nuestra lectura".
- [x] Citas traducidas marcadas "(trad.)" en ES (Microsoft, AMD, título de la nota de DeepSeek).
- [x] ES y EN dicen lo mismo: mismas cifras, mismos hechos, mismas citas (EN 1.246 palabras = 90 % de ES).

## 2. Cobertura y equilibrio

- [x] 12 destacados en total; el primero es el más relevante de la semana (php2shell) y recibe 4 párrafos.
- [x] ≥ 3 destacados de empresas de Asia: DeepSeek (China), Qwen/Alibaba (China), JD.com (China)
      + el informe macro del Sudeste Asiático al cierre.
- [x] Mezcla de temas: seguridad (2), modelos/benchmarks (3), producto web/ingress (2), industria y
      mundo físico (2), cuántica/soberanía/economía digital (3).
- [x] Cada empresa como máximo 2 veces y solo por anuncios distintos: Cloudflare 2 (WAF php2shell / WebMCP),
      Microsoft 2 (agentic insider / soberanía), Google 2 (cuántica / e-Conomy SEA); el resto, 1.
- [x] Sin rumores ni filtraciones; solo anuncios oficiales.
- [x] El ítem central (php2shell) enlaza a 4 fuentes oficiales de la misma respuesta coordinada
      (Cloudflare, PHP, OpenAI, Cloudflare WAF).

## 3. Estructura y estilo

- [x] Secciones de plantilla: entradilla (3 párrafos), destacados en 5 bloques H2, "Nuestra lectura",
      Fuentes, cierre/CTA.
- [x] Jerarquía H2 → H3 sin saltos; H3 en formato "Empresa — anuncio".
- [x] Párrafos ≤ 4 líneas; frases ~20 palabras; voz activa; español neutro.
- [x] Vocabulario prohibido ausente (sin "revolución", "histórico", "cambia todo", sin clickbait).
- [x] Números clave en negrita; citas en formato `**[n]** Empresa — "Título", fecha. URL`.
- [x] CTA en una línea, sin enlace placeholder (texto plano).

## 4. Versión EN (adaptación)

- [x] Adaptación, no traducción literal: cadencia inglesa propia, idénticos números y hechos.
- [x] La cita de Spencer Pan no lleva "(trad.)" en EN (original en inglés); en ES sí.
- [x] EN 1.246 palabras frente a ES 1.384 → relación 90 % (dentro del equilibrio ±10 %, en el borde).

## 5. Metadatos y longitudes

- [x] Front matter completo y coherente en ambos idiomas (title, slug, date, excerpt, lang, categories,
      tags, status, translated apuntando recíprocamente).
- [x] Título ES 55 car. / EN 54 car. (≤ 60).
- [x] Excerpt ES 144 car. / EN 141 car. (120–160 ✓; también sirve como meta descripción en el rango 140–160).
- [x] ES 1.384 palabras (rango 900–1.400).

## 6. SEO y WordPress

- [x] Keyword principal "IA esta semana" en título; "php2shell" en H2 y primer párrafo.
      Slug cortos: `ia-semana-php2shell-modelos` / `ai-week-php2shell-modelos`.
- [x] Solo enlaces a fuentes oficiales; anchors descriptivos (nunca "aquí").
- [x] HTMLs válidos, solo con etiquetas permitidas (h2, h3, p, ul, li, strong, em, a, blockquote);
      sin `<code>`, sin `<div>`, sin placeholders; 18 enlaces externos en cada idioma,
      todos con `target="_blank" rel="noopener"`.
- [x] Meta título / meta descripción / categorías / tags en comentario de primera línea de ambos HTML.
- [x] Categorías y tags sugeridas (IA · Innovación · Estado del sector | IA, innovación, cloud, seguridad,
      agentes, cuántica).
- N/A alt text (sin imágenes en la edición).

## 7. Legal y reputación

- [x] Sin difamación, sin datos personales, sin leaks.
- [x] Terceras marcas (Calif.io, Wiz, Quarkslab, GPT-5.6 Sol, GPT-6-Astra, DeepSeek, Qwen3.8-Max, Porsche,
      Volkswagen, AMD) mencionadas solo en contexto de anuncios públicos (divulgación coordinada y
      benchmark publicados por sus emisores).
- [x] Opinión declarada como opinión ("Nuestra lectura").

## Cambios editoriales documentados (desviaciones de la lista aprobada)

1. **AWS: Lambda Web Functions → ECS Gateway (20/10).** El anuncio directo de Lambda Web Functions es del
   **12 de octubre** (fuera de la ventana 15–22); la lista aprobada lo fechaba por su mención en el roundup
   del 19/10. Para cumplir la regla de ventana con fuente oficial directa de la semana, el ítem AWS pasa a
   **Amazon ECS Gateway** (post de lanzamiento, 20/10, verificado).
2. **NAVER Papago → Google e-Conomy SEA 2026 (21/10).** La nota de prensa de NAVER
   (`pressReleasesDetail?seq=10171373`) devolvió **HTTP 500 en 3 intentos** a lo largo de la sesión; sin
   página accesible no cumple la regla "el enlace funciona". Se usó el ítem de reserva aprobado
   (e-Conomy SEA), que además refuerza el hilo de compra agéntica de la edición.
3. **NVIDIA Cosmos: fecha corregida de 22 a 21 de octubre** según el post oficial verificado.

Pendiente menor: los títulos de [2] (php.net) están parafraseados en la lista de fuentes (página no
verificada directamente); cotejar el título exacto antes de publicar.

## Veredicto

**APTO CON MATICES** — se guardan los entregables en `articulos/2026-10-22/`. Los matices son decisiones
editoriales documentadas (cambios 1–3) y tres datos no re-verificados en la pasada final (tabla de
BlenderWorld, "GA en semanas" de OpenAI y la página de php.net), todos citados a fuente oficial. Nada que
impida la publicación tras una ojeada visual a [2] y [8].
