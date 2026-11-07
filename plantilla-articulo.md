# Plantilla del artículo semanal

Boletín de resumen: una entrada que recopile lo mejor de la semana en IA e
innovación de las grandes empresas (EE. UU. + Europa + Asia), con enlaces y análisis breve.

## Front matter (YAML) — rellénalo en ambos idiomas

```yaml
---
title: "Título del boletín (≤ 60 caracteres)"
slug: slug-seo-corto
date: AAAA-MM-DD
excerpt: "Frase gancho de 120–160 caracteres."
lang: es           # en en la versión inglesa
categories: ["IA", "Innovación", "Estado del sector"]
tags: [IA, innovación, semiconductores, robótica, cloud]
status: draft
translated: "XXXX-MM-DD/articulo-en.md"   # en la versión ES; recíproco en la EN
---
```

## Esqueleto (secciones fijas)

### 1. Título
Patrones que funcionan: `IA esta semana (N.º X): [tema estrella] y [segundo tema]` o
`[Empresa] [acción] mientras [contexto]: lo que importa en IA esta semana`.
Honesto y sin snake-oil; nunca prometer lo que no contiene.

### 2. Entradilla (2–3 párrafos)
- Qué movió la semana (2–3 nombres y sus anuncios).
- Por qué este resumen existe: sincrónico y sin relleno.
- Qué encontrará el lector ("tres de las diez novedades salen de Asia"…).

### 3. Lo destacado de la semana (8–12 puntos, agrupados en 3–5 bloques H2)

Bloques sugeridos (adaptar según lo que haya):
*Modelos y research* · *Producto y beta* · *Chips e infraestructura* ·
*Robótica y automoción* · *China/Asia spotlight* · *Regulación e inequidad táctica*

Formato por item (H3 + cuerpo):
```markdown
### [Empresa] — [acción concreta en ≤ 8 palabras]

2–4 párrafos: qué anunció oficialmente, dato/tabla/resultado clave, por qué
importa (1 párrafo). Cita numerada al final del dato clave [n].
```
Reglas del bloque:
- Cada item aparece **una sola vez** (la empresa más citada puede tener 2 items
  solo si son anuncios distintos).
- 3 de los ≥ 8 items como mínimo de empresas de Asia (China, Japón, Corea, Taiwán).
- El item central de la semana (el más importante) va primero y recibe 4 párrafos.

### 4. Nuestra lectura (3–5 frases)
Qué implica para las empresas que leen el blog: decisiones de compra (chips,
serverless, cloud china…), riesgos, tendencias a observar. Opinión marcada
como tal. Nada que no se pueda sostener con dos de las fuentes del artículo.

### 5. Fuentes
Lista numerada completa (ver formato en `guia-estilo.md`), una entrada por cita
usada en el texto, en orden de aparición.

### 6. Cierre y CTA
Firma del equipo + llamada a la acción (contacto, demo, newsletter) en una línea.

## Versión en inglés

Misma estructura y las mismas fuentes; títulos y entrdilla reescritos para el
ritmo nativo, no literalmente traducidos (ver `guia-estilo.md`).

## Entregable WordPress

El `.html` listo para pegar usa solo: `h2/h3/p/ul/li/strong/em/a/figure/blockquote`,
incluye sugerencia de meta título, meta descripción, categorías y tags como
comentario HTML en la primera línea, y deja los enlaces externos con
`target="_blank" rel="noopener"`.
