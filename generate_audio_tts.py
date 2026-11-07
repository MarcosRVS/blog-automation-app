#!/usr/bin/env python3
"""
Generador de Audio Podcast / Narración para Artículos de Blog
Usa la API de Google (Gemini 2.5 Flash + Google TTS) para convertir el artículo en un podcast de alta calidad.
"""

import os
import sys
import re
import json
import urllib.request
import urllib.error
import urllib.parse
from typing import List, Optional

# Configurar salida UTF-8 para consola Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def detect_language(md_text: str, article_path: str) -> str:
    """Detecta el idioma ('es' o 'en') a partir del frontmatter YAML o del nombre de archivo."""
    if md_text.startswith("---"):
        parts = md_text.split("---", 2)
        if len(parts) >= 3:
            match = re.search(r"^\s*lang:\s*([a-zA-Z-]+)", parts[1], flags=re.MULTILINE)
            if match:
                return match.group(1).strip().lower()[:2]
    if os.path.basename(article_path).endswith("-en.md"):
        return "en"
    return "es"


def clean_markdown_for_speech(md_text: str) -> str:
    """Limpia el Markdown para que sea natural al escucharse en audio sin romper palabras compuestas."""
    # 1. Eliminar frontmatter YAML
    if md_text.startswith("---"):
        parts = md_text.split("---", 2)
        if len(parts) >= 3:
            md_text = parts[2]

    # 2. Cortar la sección de Fuentes / Sources y el pie editorial para no leer URLs en voz alta
    md_text = re.split(
        r"\n##\s+(?:Fuentes|Sources)\b", md_text, maxsplit=1, flags=re.IGNORECASE
    )[0]
    md_text = re.split(r"\n---\s*\n", md_text, maxsplit=1)[0]

    # 3. Eliminar bloques de código y código inline
    text = re.sub(r"```.*?```", "", md_text, flags=re.DOTALL)
    text = re.sub(r"`([^`]+)`", r"\1", text)

    # 4. Eliminar citas numeradas tipo [1], [2] y notas de traducción "(trad.)"
    text = re.sub(r"\s*\[\d+\]", "", text)
    text = re.sub(r"\s*\(trad\.\)", "", text, flags=re.IGNORECASE)

    # 5. Convertir enlaces [texto](url) en solo texto
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)

    # 6. En encabezados H3 tipo "### Empresa — Acción", cambiar la raya por dos puntos
    text = re.sub(
        r"^#+\s*([^\n—–]+?)\s*[—–]\s*([^\n]+)$",
        r"\1: \2.",
        text,
        flags=re.MULTILINE,
    )
    # Quitar marcadores de encabezados restantes y asegurar pausa al final del título
    text = re.sub(r"^\s*#+\s*(.+?)\s*$", r"\1.", text, flags=re.MULTILINE)
    text = re.sub(r"\.\.+", ".", text)

    # 7. Reemplazar guiones bajos dentro de identificadores (ej. search_products -> search products)
    text = re.sub(r"(?<=\w)_(?=\w)", " ", text)

    # 8. Quitar negritas, cursivas y citas (> )
    text = re.sub(r"[*_]{1,3}", "", text)
    text = re.sub(r"^\s*>\s*", "", text, flags=re.MULTILINE)

    # 9. Quitar tablas y viñetas SOLO al inicio de línea (conservando guiones en CVE-2026, GPT-5.6, e-commerce)
    text = re.sub(r"^\s*\|[^\n]+\|\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)

    # 10. Reemplazar rayas parentéticas (— o –) por comas y espacios para no pegar palabras
    text = re.sub(r"\s*[—–]\s*", ", ", text)

    # 11. Normalizar abreviaturas comunes para mejor lectura TTS y evitar cortes de frase falsos
    text = re.sub(r"\bN\.º\s*", "número ", text)
    text = re.sub(r"\bEE\.\s*UU\.", "Estados Unidos", text)
    text = re.sub(r"(\d+)\s*×", r"\1 veces", text)

    # 12. Limpiar espacios antes de signos de puntuación y saltos de línea múltiples
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)
    text = re.sub(r",\s*,", ",", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def generate_podcast_script_with_gemini(
    cleaned_text: str, api_key: str, lang: str = "es"
) -> str:
    """Usa Gemini para adaptar el artículo a un guion hablado fluido y profesional."""
    if not api_key:
        print(
            "[!] Aviso: Variable GEMINI_API_KEY no definida; usando el texto limpio directo como guion."
        )
        return cleaned_text

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

    lang_instruction = "español" if lang == "es" else "inglés"
    prompt = f"""Eres un locutor profesional de podcasts sobre tecnología e inteligencia artificial.
Convierte el siguiente artículo técnico en una narración fluida, amena y natural para ser leída por un sistema Text-To-Speech en {lang_instruction}.

Reglas:
- Conserva todos los datos, empresas, nombres y cifras clave de principio a fin sin omitir secciones.
- No uses listas con viñetas ni encabezados; redacta frases completas con transiciones sonoras naturales.
- No agregues música ni efectos de sonido escritos (ej. NO pongas [Música de fondo]).
- No incluyas URLs ni números de referencia bibliográfica.
- Devuelve ÚNICAMENTE el texto que el locutor debe pronunciar.

Artículo:
{cleaned_text}
"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.4},
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            candidates = data.get("candidates", [])
            if candidates:
                return candidates[0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        print(
            f"[!] Aviso: No se pudo conectar a Gemini ({e}), usando texto limpio directo."
        )

    return cleaned_text


def split_into_tts_chunks(text: str, max_len: int = 180) -> List[str]:
    """Divide el texto en fragmentos seguros (<= max_len caracteres) respetando oraciones y pausas."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks: List[str] = []
    current_chunk = ""

    def flush_current():
        nonlocal current_chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        current_chunk = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        if len(sentence) <= max_len:
            if len(current_chunk) + len(sentence) + 1 <= max_len:
                current_chunk += (" " if current_chunk else "") + sentence
            else:
                flush_current()
                current_chunk = sentence
        else:
            # Si una sola oración supera max_len, subdividir por cláusulas (, ; :) o palabras
            flush_current()
            subparts = re.split(r"(?<=[,;:])\s+", sentence)
            for sub in subparts:
                sub = sub.strip()
                if not sub:
                    continue
                if len(sub) <= max_len:
                    if len(current_chunk) + len(sub) + 1 <= max_len:
                        current_chunk += (" " if current_chunk else "") + sub
                    else:
                        flush_current()
                        current_chunk = sub
                else:
                    flush_current()
                    words = sub.split()
                    for word in words:
                        if len(current_chunk) + len(word) + 1 <= max_len:
                            current_chunk += (" " if current_chunk else "") + word
                        else:
                            flush_current()
                            current_chunk = word
            flush_current()

    flush_current()
    return chunks


def synthesize_audio_google(text: str, output_path: str, lang: str = "es") -> bool:
    """
    Sintetiza el texto a audio MP3 utilizando Google Translate TTS API
    dividida en bloques seguros para máxima calidad y fluidez.
    """
    chunks = split_into_tts_chunks(text, max_len=180)
    print(f"[*] Sintetizando {len(chunks)} fragmentos de voz ({lang}) con Google TTS API...")

    temp_path = output_path + ".part"
    errors = 0

    with open(temp_path, "wb") as outfile:
        for idx, chunk in enumerate(chunks, 1):
            if not chunk:
                continue
            encoded_text = urllib.parse.quote(chunk)
            url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded_text}&tl={lang}&client=tw-ob"
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                },
            )
            try:
                with urllib.request.urlopen(req, timeout=20) as response:
                    outfile.write(response.read())
            except Exception as e:
                errors += 1
                print(f"[!] Error descargando fragmento {idx}/{len(chunks)}: {e}")

    if errors == len(chunks) and chunks:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        print("[X] Falló la síntesis de todos los fragmentos de audio.")
        return False

    os.replace(temp_path, output_path)
    if errors > 0:
        print(
            f"[!] Audio generado con {errors} fragmento(s) fallido(s): {output_path}"
        )
    else:
        print(f"[✓] Audio generado con éxito: {output_path}")
    return True


def find_latest_article(base_dir: str) -> Optional[str]:
    """Busca automáticamente el artículo más reciente en articulos/AAAA-MM-DD/articulo.md."""
    articulos_dir = os.path.join(base_dir, "articulos")
    if not os.path.isdir(articulos_dir):
        return None
    dated_dirs = sorted(
        [
            d
            for d in os.listdir(articulos_dir)
            if os.path.isdir(os.path.join(articulos_dir, d))
            and re.match(r"^\d{4}-\d{2}-\d{2}$", d)
        ],
        reverse=True,
    )
    for d in dated_dirs:
        candidate = os.path.join(articulos_dir, d, "articulo.md")
        if os.path.isfile(candidate):
            return candidate
    return None


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    article_path = sys.argv[1] if len(sys.argv) > 1 else find_latest_article(base_dir)

    if not article_path or not os.path.exists(article_path):
        print(f"[X] No se encontró ningún artículo válido en: {article_path}")
        sys.exit(1)

    print(f"[*] Leyendo artículo: {article_path}")
    with open(article_path, "r", encoding="utf-8") as f:
        content = f.read()

    lang = detect_language(content, article_path)
    cleaned = clean_markdown_for_speech(content)
    api_key = os.environ.get("GEMINI_API_KEY", "")

    print(f"[*] Adaptando guion para locución (idioma: {lang})...")
    script = generate_podcast_script_with_gemini(cleaned, api_key, lang=lang)

    out_dir = os.path.dirname(article_path)
    suffix = "-en" if lang == "en" else ""
    audio_output = os.path.join(out_dir, f"podcast-episodio{suffix}.mp3")
    script_output = os.path.join(out_dir, f"guion-locucion{suffix}.txt")

    with open(script_output, "w", encoding="utf-8") as f:
        f.write(script + "\n")
    print(f"[✓] Guion guardado en: {script_output}")

    synthesize_audio_google(script, audio_output, lang=lang)


if __name__ == "__main__":
    main()
