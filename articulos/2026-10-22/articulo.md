---
title: "IA esta semana (N.º 1): php2shell y modelos a la carta"
slug: ia-semana-php2shell-modelos
date: 2026-10-22
excerpt: "El RCE php2shell fuerza una respuesta coordinada del sector; los modelos frontera entran en catálogos ajenos y el Sudeste Asiático crece 17 %."
lang: es
categories: ["IA", "Innovación", "Estado del sector"]
tags: [IA, innovación, cloud, seguridad, agentes, cuántica]
status: draft
translated: "2026-10-22/articulo-en.md"
---

# IA esta semana (N.º 1): php2shell y modelos a la carta

La semana arrancó con dos vulnerabilidades críticas en el runtime de PHP, conocidas como php2shell, capaces de convertir un servidor web en canal de ejecución remota [1]. La defensa se organizó en horas, con investigación asistida por modelos frontera [1][3].

OpenAI entra en el Model Garden de Google Cloud [6], DeepSeek abre su búsqueda web en la API [7] y Qwen publica su benchmark de agentes visuales [8].

Esta edición reúne 12 anuncios oficiales de los últimos 7 días. Tres son de empresas asiáticas; el cierre trae el dato macro del Sudeste Asiático.

## Seguridad: una respuesta coordinada en 24 horas

### Cloudflare — WAF por defecto

Calif.io, Wiz, OpenAI y Quarkslab divulgaron el 21 de octubre dos vulnerabilidades de PHP: CVE-2026-109618 y CVE-2026-109619, bautizadas php2shell [1]. Afectan a todo servidor con PHP 5.4 o posterior: denegación, ejecución remota de código y fuga de datos [1]. PHP respalda cerca del **70 %** de los sitios web [1].

PHP publicó el aviso oficial con las versiones correctoras: **8.5.12, 8.4.27, 8.3.36 y 8.2.35** [2]. Cloudflare activó reglas de WAF por defecto a las **03:02 UTC del 21 de octubre**, unas nueve horas antes de la divulgación [1].

El hallazgo por ruta nueva: Calif usó GPT-5.6 Sol en Patch the Planet de OpenAI, y Wiz lo reportó por su cuenta [3]. OpenAI habla de una "ventana del defensor" y publicó un verificador de versiones como skill de Codex [3].

La novedad de fondo es *full transaction detection*: el WAF correlaciona petición y respuesta y puede frenar la respuesta del servidor antes de que llegue al atacante [4]. Es el primer lanzamiento de detecciones gestionadas con esta capacidad [4]. Parchear PHP sigue obligatorio; el WAF es una segunda capa [1].

### Microsoft — Guardian Agents

Microsoft puso nombre al riesgo: los *agentic insiders*, agentes desplegados por la propia empresa [5]. Suelen venir sobre-privilegiados y nada confiables por defecto; optimizan resultados, no normas [5].

La receta: Guardian Agents supervisan cada acción 24/7 con identidad, permisos y riesgo dinámico por agente (Project Perception) [5]. "Necesitamos entender en tiempo real qué hacen los agentes y qué riesgos crean esas acciones" (trad.) [5].

## Modelos: la frontera entra en catálogos ajenos

### OpenAI — en el Model Garden

Los modelos frontera de OpenAI y los flujos agénticos de Codex llegarán al Model Garden de Google Cloud, con acceso nativo sobre la infraestructura y gobernanza de Google [6]. La disponibilidad general está a semanas [6].

Microsoft sigue siendo el socio principal [6]. El proveedor se elegirá por carga de trabajo, no por contrato anual [6].

### DeepSeek — búsqueda en la API

DeepSeek actualizó su V4.1 Flash a la versión 1017 y abrió dos endpoints, Search y Fetch, sobre motor de búsqueda propio [7]. El índice suma del orden de 100.000 millones de páginas, con filtro de SEO manipulado [7].

El precio apunta a volumen: **¥5 por 1.000 peticiones**, facturadas desde el 1 de noviembre [7]. El modelo salió con pesos abiertos, tras mejorar en proyectos completos [7].

### Qwen — BlenderWorld

El equipo de Qwen —Alibaba— publicó BlenderWorld, primer benchmark integral de agentes visuales de creación 3D: **223 tareas** (texto, imagen o vídeo) [8][9]. Cada entrega se renderiza y se mide contra **2.651 rúbricas binarias** [8].

El techo queda lejos: GPT-6-Astra lidera con **79,9** y nadie completa a la perfección más del **42,2 %** de las tareas [8]. DeepSeek V4.1 Flash, 66,0; Qwen3.8-Max, 61,1 [8].

## Producto: web y despliegues listos para agentes

### Cloudflare — WebMCP en tiendas

Cloudflare activó su implementación edge de WebMCP con Commerce.com en casi **100.000 dominios** de e-commerce [10]. El estándar experimental de Google expone herramientas estructuradas (search_products, add_to_cart) para que el agente no adivine botones [10].

Todo ocurre en la sesión del navegador del comprador, sobre el dominio de la tienda; sin credenciales en terceros y con pago final humano [10]. Hay opt-out por tienda y fallback si el servidor MCP falla [10].

### AWS — ECS Gateway

Amazon ECS estrenó ECS Gateway, que automatiza el ingress de servicios contenerizados: certificados ACM, hostname DNS, reglas de listener y grupos de seguridad se crean solos en la cuenta propia [11].

Plataforma fija los estándares una vez; aplicación conecta sin trabajo de red [11]. Hasta **25 servicios** comparten un ALB sin coste extra, ya en todas las regiones comerciales [11].

## Fábrica y mundo físico: GTC Berlín y la planta conectada

### NVIDIA — Cosmos abierto

En la GTC de Berlín, NVIDIA abrió más Cosmos, sus *world models* físicos [12]. Cosmos Data Factory suma **cinco blueprints cloud-native** para curar datos, en GitHub y vía Azure, Nebius y CoreWeave [12].

Cosmos Framework expone entrenamiento, refuerzo y despliegue como *agent skills* para modelos abiertos (GR00T, Alpamayo, los Qwen o Pi0.5); Cosmos 3 NIM promete inferencia **2× más rápida** [12]. Porsche usa Data Factory en su *flywheel* de Volkswagen y espera un **90 %** menos de pruebas físicas y un **85 %** menos de ciclos [12].

### JD.com — IA en la fábrica

JINGDONG Industrials, el brazo industrial de JD.com, firmó el 13 de octubre en Shanghai un acuerdo con AMD para llevar IA a fábricas [13]. JoyIndustrial se adaptará a AMD Ryzen AI Max para correr en dispositivos de planta [13].

Anuncian mantenimiento predictivo, inspección visual, seguridad laboral y world models que anticipen colisiones leyendo trayectorias [13]. Spencer Pan, de AMD: "mover la IA más allá de ver y reconocer hacia entender, razonar y predecir" (trad.) [13].

## Y además: cuántica práctica, soberanía digital y $368B

### Google — estados mágicos

Google Quantum AI demostró en Willow el cultivo de estados mágicos, para producir los estados que exigirá la corrección de errores [14]. El protocolo redujo los errores **40×** y logró fidelidad lógica récord de **99,99 %**; el paper sale en Science [14]. Hasta el **95 %** de la capacidad de una máquina cuántica se estimaba destinado a fabricar esos estados: ese es el bloqueo eliminado [14].

### Microsoft — soberanía como continuo

Antes de Ignite, Microsoft convirtió la soberanía en un continuo de nube pública, privada y partners, con la carga de trabajo como criterio [15]. Llegan: Sovereign Control Panel (vista previa), Just-in-time Access y Customer Lockbox, Data Guardian y Production Touch Ledger en UE/EFTA y claves externas en GA [15]. Foundry Local y GitHub Enterprise Local pasan a GA en Azure Local [15].

### Google — Sudeste Asiático

El informe e-Conomy SEA 2026 (Google, Temasek y Bain) proyecta **368 mil millones de dólares** de economía digital en el Sudeste Asiático, un **17 %** más, camino a un billón en 2035 [16]. El motor es real: **243 millones** usan IA generativa a diario (58 % de la población trabajadora) y el **75 %** acepta comprar vía agentes [16].

## Nuestra lectura

La semana apunta a una tesis: los agentes ya viven dentro de la empresa y del escaparate. La divulgación coordinada asistida por IA ya es infraestructura disponible; el parcheo se planifica como proceso y no como incidente [1][3]. El modelo se elige por carga de trabajo, no por contrato anual [6][7]. Y entre e-Conomy (75 % de compradores agénticos [16]) y WebMCP en casi 100.000 tiendas [10], el carrito agéntico necesita responsable antes de la temporada alta.

## Fuentes

**[1]** Cloudflare — "Cloudflare deploys protections against php2shell vulnerability", 21 oct 2026. https://blog.cloudflare.com/php-vulnerabilities-waf-protection/
**[2]** Grupo PHP — "Aviso de seguridad del 21 de octubre de 2026 sobre la corrección de php2shell", 21 oct 2026. https://www.php.net/archive/2026.php#2026-10-21-5
**[3]** OpenAI — "Patch the Planet: global response coordination as agents uncover critical vulnerabilities", 21 oct 2026. https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/
**[4]** Cloudflare — "Introducing full transaction detection for Cloudflare WAF", 21 oct 2026. https://blog.cloudflare.com/full-transaction-waf/
**[5]** Microsoft — "Securing the agentic insider", 19 oct 2026. https://blogs.microsoft.com/blog/2026/10/19/securing-the-agentic-insider/
**[6]** OpenAI — "OpenAI models are coming to Google Cloud", 21 oct 2026. https://openai.com/index/openai-models-google-cloud/
**[7]** DeepSeek — "Nueva versión de DeepSeek V4.1 Flash (V4.1-Flash-1017)" (trad.), 17 oct 2026. https://api-docs.deepseek.com/zh-cn/news/news261017
**[8]** Qwen (Alibaba) — "Benchmarking Visual Agents for 3D Creation from Real-World References", 20 oct 2026. https://huggingface.co/papers/2610.23986
**[9]** Qwen — "BlenderWorld" (dataset oficial), oct 2026. https://huggingface.co/datasets/Qwen/BlenderWorld
**[10]** Cloudflare — "How Commerce.com and Cloudflare are getting storefronts ready for AI agents", 21 oct 2026. https://blog.cloudflare.com/webmcp-commerce/
**[11]** AWS — "Introducing Amazon ECS Gateway: A fully-managed ingress solution for ECS services", 20 oct 2026. https://aws.amazon.com/blogs/aws/introducing-amazon-ecs-gateway-a-fully-managed-ingress-solution-for-ecs-services/
**[12]** NVIDIA — "NVIDIA Cosmos Opens New Tools to Train, Evaluate and Deploy World Models", 21 oct 2026. https://blogs.nvidia.com/blog/cosmos-open-train-evaluate-deploy-world-models/
**[13]** JD.com — "JINGDONG Industrials and AMD Partner to Bring AI to Factory Operations", 15 oct 2026. https://jdcorporateblog.com/jingdong-industrials-and-amd-partner-to-bring-ai-to-factory-operations/
**[14]** Google — "Bringing the magic: Google breaks open a bottleneck in quantum computing", 15 oct 2026. https://blog.google/innovation-and-ai/models-and-research/quantum-computing/magic-state-cultivation-quantum-computing/
**[15]** Microsoft — "Advancing digital sovereignty with greater control and choice", 20 oct 2026. https://blogs.microsoft.com/blog/2026/10/20/advancing-digital-sovereignty-with-greater-control-and-choice/
**[16]** Google — "Southeast Asia's digital economy to hit $368 billion", 21 oct 2026. https://blog.google/company-news/inside-google/around-the-globe/google-asia/e-conomy-sea-report-2026/

---

Redactado y revisado por el equipo editorial del blog.

¿El resumen semanal en tu correo? Suscríbete al newsletter del blog.
