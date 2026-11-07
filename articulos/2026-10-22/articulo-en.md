---
title: "AI This Week (No. 1): php2shell and Models à la Carte"
slug: ai-week-php2shell-models
date: 2026-10-22
excerpt: "php2shell forces a coordinated industry response; frontier models land in other clouds; Southeast Asia's digital economy grows 17% this year."
lang: en
categories: ["AI", "Innovation", "Industry pulse"]
tags: [AI, innovation, cloud, security, agents, quantum]
status: draft
translated: "2026-10-22/articulo.md"
---

# AI This Week (No. 1): php2shell and Models à la Carte

The week opened with two critical vulnerabilities in PHP's runtime, known as php2shell, able to turn a web server into a remote execution channel [1]. The defense came together in hours, with AI-assisted research [1][3].

OpenAI enters Google Cloud's Model Garden [6], DeepSeek opens web search in its API [7], and Qwen publishes its visual-agent benchmark.

This edition gathers 12 official announcements from the past 7 days. Three come from Asian companies; the closer brings Southeast Asia's macro number.

## Security: a coordinated response within 24 hours

### Cloudflare — default-on WAF

Calif.io, Wiz, OpenAI and Quarkslab disclosed two PHP vulnerabilities on October 21: CVE-2026-109618 and CVE-2026-109619, known as php2shell [1]. They affect every server running PHP 5.4 or later: denial of service, remote code execution and data exposure [1]. PHP backs nearly **70%** of websites [1].

PHP published the official advisory with the patch versions: **8.5.12, 8.4.27, 8.3.36 and 8.2.35** [2]. Cloudflare turned default-on WAF rules for all its customers at **03:02 UTC on October 21**, about nine hours before disclosure [1].

The finding came through a new route: Calif used GPT-5.6 Sol in OpenAI's Patch the Planet program, and Wiz reported it independently [3]. OpenAI speaks of a "defender's window" and shipped a version checker as a Codex skill [3].

The deeper novelty is *full transaction detection*: the WAF correlates request and response and can stop the server's response before it reaches the attacker [4]. It is the first release of managed detections with this capability [4]. Patching PHP remains mandatory; the WAF is a second layer [1].

### Microsoft — Guardian Agents

Microsoft named the risk: the *agentic insider*, an agent deployed by the company itself [5]. Agents often ship over-privileged and untrustworthy by default; they optimize outcomes, not norms.

The playbook: Guardian Agents watch every single action 24/7 with per-agent identity, permissions and dynamic risk scoring (Project Perception) [5]. "We need to understand in real time what the agents are doing and what risks those actions create" [5].

## Models: the frontier lands in other clouds' catalogs

### OpenAI — in the Model Garden

OpenAI's frontier models and Codex agentic workflows will arrive on Google Cloud's Model Garden, with native access on Google's infrastructure and governance [6]. General availability is just weeks away [6].

Microsoft remains the primary partner [6]. The provider will be chosen per workload, not per annual contract [6].

### DeepSeek — search in the API

DeepSeek updated its V4.1 Flash to the 1017 version and opened two endpoints, Search and Fetch, on its own search engine [7]. The index totals on the order of 100 billion pages, with a filter for manipulative SEO [7].

Pricing targets volume: **¥5 per 1,000 requests**, billed from November 1 [7]. The model shipped open weights, after improving at complete projects [7].

### Qwen — BlenderWorld

Qwen's team at Alibaba published BlenderWorld, the first comprehensive benchmark for visual 3D-creation agents: **223 tasks** (text, image or video) [8][9]. Each submission is rendered and scored against **2,651 binary rubrics** [8].

The ceiling stays far: GPT-6-Astra leads with **79.9**, and no one completes more than **42.2%** of tasks "perfectly" [8]. DeepSeek V4.1 Flash, 66.0; Qwen3.8-Max, 61.1 [8].

## Product: web and deploys ready for agents

### Cloudflare — WebMCP in stores

Cloudflare activated its edge implementation of WebMCP with Commerce.com across almost **100,000 domains** of e-commerce [10]. Google's experimental standard exposes structured tools on the page (search_products, add_to_cart) so agents stop guessing buttons [10].

Everything happens in the shopper's browser session, on the store's own domain; no credentials to third parties and a human-final checkout [10]. There is per-store opt-out and a fallback when the MCP server fails [10].

### AWS — ECS Gateway

Amazon ECS shipped ECS Gateway, which automates ingress for containerized services: ACM certificates, DNS hostname, listener rules and security groups create themselves inside the customer's account [11].

Platform sets the standards once; applications connect with no networking work [11]. Up to **25 services** share one ALB at no extra charge, already available in all commercial Regions [11].

## Factory and physical world: GTC Berlin and the connected plant

### NVIDIA — Cosmos opened

At GTC Berlin, NVIDIA opened up more of Cosmos, its physical *world models* [12]. Cosmos Data Factory adds **five cloud-native blueprints** for curating data, on GitHub and via Azure, Nebius and CoreWeave [12].

Cosmos Framework exposes training, RL and deployment as *agent skills* for open models (GR00T, Alpamayo, the Qwen family or Pi0.5); Cosmos 3 NIM promises **2× faster** inference [12]. Porsche uses Data Factory in its Volkswagen flywheel and expects **90%** fewer repeated physical tests and **85%** shorter cycles [12].

### JD.com — AI in the factory

JINGDONG Industrials, JD.com's industrial arm, signed an agreement with AMD on October 13 in Shanghai to bring AI into factories [13]. JoyIndustrial will be adapted to AMD Ryzen AI Max to run on shop-floor devices [13].

The announced uses span predictive maintenance, visual inspection, workplace safety and world models that anticipate collisions by reading trajectories [13]. AMD's Spencer Pan: "moving AI beyond seeing and recognizing to understanding, reasoning, and predicting" [13].

## Also this week: practical quantum, digital sovereignty and $368B

### Google — magic states

Google Quantum AI demonstrated magic state cultivation on Willow, to produce the states error correction will demand [14]. The protocol cut errors **40×** and reached a record logical fidelity of **99.99%**; the paper appears in Science [14]. Up to **95%** of a quantum machine's capacity was estimated to go into producing those states: that is the bottleneck removed [14].

### Microsoft — sovereignty as a continuum

Ahead of Ignite, Microsoft turned sovereignty into a continuum of public cloud, private cloud and partners, with the workload as the criterion [15]. Arriving: Sovereign Control Panel (public preview), Just-in-time Access and Customer Lockbox, Data Guardian and Production Touch Ledger in the EU/EFTA, and external keys now GA [15]. Foundry Local and GitHub Enterprise Local go GA on Azure Local [15].

### Google — Southeast Asia

The e-Conomy SEA 2026 report (Google, Temasek and Bain) projects **$368 billion** of digital economy in Southeast Asia, up **17%**, on track to pass $1 trillion in 2035 [16]. The engine is real: **243 million** people use generative AI daily (58% of the working population) and **75%** accept buying through agents [16].

## Our take

The week points to one thesis: agents now live inside the company and the shop window. AI-assisted coordinated disclosure is available infrastructure; patching gets planned as a process, not an incident [1][3]. The model is chosen per workload, not per annual contract [6][7]. And between e-Conomy (75% agentic buyers [16]) and WebMCP live on nearly 100,000 stores [10], agentic checkout needs an owner before peak season.

## Sources

**[1]** Cloudflare — "Cloudflare deploys protections against php2shell vulnerability", Oct 21, 2026. https://blog.cloudflare.com/php-vulnerabilities-waf-protection/
**[2]** PHP Group — "PHP security release announcement for php2shell fixes", Oct 21, 2026. https://www.php.net/archive/2026.php#2026-10-21-5
**[3]** OpenAI — "Patch the Planet: global response coordination as agents uncover critical vulnerabilities", Oct 21, 2026. https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/
**[4]** Cloudflare — "Introducing full transaction detection for Cloudflare WAF", Oct 21, 2026. https://blog.cloudflare.com/full-transaction-waf/
**[5]** Microsoft — "Securing the agentic insider", Oct 19, 2026. https://blogs.microsoft.com/blog/2026/10/19/securing-the-agentic-insider/
**[6]** OpenAI — "OpenAI models are coming to Google Cloud", Oct 21, 2026. https://openai.com/index/openai-models-google-cloud/
**[7]** DeepSeek — "New DeepSeek V4.1 Flash version (V4.1-Flash-1017)" (translated title), Oct 17, 2026. https://api-docs.deepseek.com/zh-cn/news/news261017
**[8]** Qwen (Alibaba) — "Benchmarking Visual Agents for 3D Creation from Real-World References", Oct 20, 2026. https://huggingface.co/papers/2610.23986
**[9]** Qwen — "BlenderWorld" (official dataset), Oct 2026. https://huggingface.co/datasets/Qwen/BlenderWorld
**[10]** Cloudflare — "How Commerce.com and Cloudflare are getting storefronts ready for AI agents", Oct 21, 2026. https://blog.cloudflare.com/webmcp-commerce/
**[11]** AWS — "Introducing Amazon ECS Gateway: A fully-managed ingress solution for ECS services", Oct 20, 2026. https://aws.amazon.com/blogs/aws/introducing-amazon-ecs-gateway-a-fully-managed-ingress-solution-for-ecs-services/
**[12]** NVIDIA — "NVIDIA Cosmos Opens New Tools to Train, Evaluate and Deploy World Models", Oct 21, 2026. https://blogs.nvidia.com/blog/cosmos-open-train-evaluate-deploy-world-models/
**[13]** JD.com — "JINGDONG Industrials and AMD Partner to Bring AI to Factory Operations", Oct 15, 2026. https://jdcorporateblog.com/jingdong-industrials-and-amd-partner-to-bring-ai-to-factory-operations/
**[14]** Google — "Bringing the magic: Google breaks open a bottleneck in quantum computing", Oct 15, 2026. https://blog.google/innovation-and-ai/models-and-research/quantum-computing/magic-state-cultivation-quantum-computing/
**[15]** Microsoft — "Advancing digital sovereignty with greater control and choice", Oct 20, 2026. https://blogs.microsoft.com/blog/2026/10/20/advancing-digital-sovereignty-with-greater-control-and-choice/
**[16]** Google — "Southeast Asia's digital economy to hit $368 billion", Oct 21, 2026. https://blog.google/company-news/inside-google/around-the-globe/google-asia/e-conomy-sea-report-2026/

---

Written and reviewed by the editorial team.

Want the weekly roundup in your inbox? Subscribe to the blog newsletter.
