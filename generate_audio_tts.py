#!/usr/bin/env python3
"""
Generador de Audio Podcast / Narración para Artículos de Blog
Soporta:
1. Gemini 3.8 Flash TTS (`gemini-3.8-flash-tts`) — Voz humana generativa de estudio (requiere GEMINI_API_KEY en entorno o ~/.env).
2. Microsoft Edge Neural TTS (`edge-tts`) — Voz neuronal natural humana sin necesidad de API key (por defecto `es-VE-SebastianNeural`).
3. Google Translate TTS — Respaldo de emergencia.
"""

import asyncio
import base64
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import wave
from typing import List, Optional

# Configurar salida UTF-8 para consola Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def load_api_key() -> str:
    """Carga GEMINI_API_KEY o GOOGLE_API_KEY desde variables de entorno, ./.env o ~/.env."""
    for var in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        val = os.environ.get(var, "").strip()
        if val:
            return val

    base_dir = pathlib.Path(__file__).resolve().parent
    for env_path in (base_dir / ".env", pathlib.Path.home() / ".env"):
        if env_path.is_file():
            try:
                for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("'").strip('"')
                    if k in ("GEMINI_API_KEY", "GOOGLE_API_KEY") and v:
                        return v
            except Exception:
                pass
    return ""


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
            "[*] GEMINI_API_KEY no detectada en entorno ni en ~/.env; usando guion limpio directo."
        )
        return cleaned_text

    models_to_try = ["gemini-3.8-flash", "gemini-2.5-flash"]
    lang_instruction = "español" if lang == "es" else "inglés"
    prompt = f"""Eres un locutor profesional de podcasts sobre tecnología e inteligencia artificial.
Convierte el siguiente artículo técnico en una narración fluida, cálida, amena y natural para ser leída en un podcast en {lang_instruction}.

Reglas:
- Conserva todos los datos, empresas, nombres y cifras clave de principio a fin sin omitir secciones.
- No uses listas con viñetas ni encabezados telegráficos; redacta frases completas con transiciones sonoras naturales ("Pasando al terreno de los semiconductores...", "Por su parte, desde Europa...").
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

    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
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
                    print(f"[✓] Guion adaptado con {model_name}.")
                    return candidates[0]["content"]["parts"][0]["text"].strip()
        except Exception as e:
            print(f"[!] Aviso con {model_name}: {e}")

    print("[!] Usando texto limpio directo como respaldo.")
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


def synthesize_audio_gemini_tts(
    text: str,
    output_path: str,
    api_key: str,
    lang: str = "es",
    voice_name: str = "Bodi",
) -> bool:
    """
    Sintetiza el guion completo con `gemini-3.8-flash-tts` (con fallback a `gemini-2.5-flash-preview-tts`).
    Gemini TTS devuelve audio PCM lineal a 24 kHz de calidad de estudio.
    """
    if not api_key:
        return False

    tts_models = ["gemini-3.8-flash-tts", "gemini-2.5-flash-preview-tts"]
    voices_to_try = [voice_name]
    if voice_name.lower() == "bodi":
        voices_to_try.append("Bodhi")
    voices_to_try.append("Puck")

    # Dividir en bloques amplios (~2500 caracteres por bloque) para no exceder límites de generación de audio por llamada
    blocks = split_into_tts_chunks(text, max_len=2500)
    style_prefix = (
        "Lee el siguiente boletín tecnológico con voz natural, cálida, profesional y ritmo de locutor de podcast:\n\n"
        if lang == "es"
        else "Read the following tech newsletter in a warm, natural, engaging podcast host voice:\n\n"
    )

    for model_name in tts_models:
        for candidate_voice in voices_to_try:
            print(
                f"[*] Sintetizando voz humana con {model_name} (voz: {candidate_voice}, {len(blocks)} bloque(s))..."
            )
            pcm_frames: List[bytes] = []
            sample_rate = 24000
            success = True
            voice_invalid = False

            for idx, block in enumerate(blocks, 1):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                payload = {
                    "contents": [{"parts": [{"text": style_prefix + block}]}],
                    "generationConfig": {
                        "responseModalities": ["AUDIO"],
                        "speechConfig": {
                            "voiceConfig": {
                                "prebuiltVoiceConfig": {"voiceName": candidate_voice}
                            }
                        },
                    },
                }
                try:
                    req = urllib.request.Request(
                        url,
                        data=json.dumps(payload).encode("utf-8"),
                        headers={"Content-Type": "application/json"},
                    )
                    with urllib.request.urlopen(req, timeout=120) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                        part = data["candidates"][0]["content"]["parts"][0]
                        inline = part.get("inlineData") or part.get("inline_data")
                        if not inline or "data" not in inline:
                            raise ValueError("Respuesta sin inlineData de audio")
                        mime = inline.get("mimeType", "")
                        m_rate = re.search(r"rate=(\d+)", mime)
                        if m_rate:
                            sample_rate = int(m_rate.group(1))
                        raw_bytes = base64.b64decode(inline["data"])
                        if raw_bytes[:4] == b"RIFF":
                            pcm_frames.append(raw_bytes[44:])
                        else:
                            pcm_frames.append(raw_bytes)
                except urllib.error.HTTPError as he:
                    err_body = he.read().decode("utf-8", errors="ignore")
                    print(
                        f"[!] Aviso en {model_name} con voz {candidate_voice} (bloque {idx}/{len(blocks)}): HTTP {he.code} - {err_body[:200]}"
                    )
                    success = False
                    if he.code == 400 and "voice" in err_body.lower():
                        voice_invalid = True
                    break
                except Exception as e:
                    print(
                        f"[!] Aviso en {model_name} con voz {candidate_voice} (bloque {idx}/{len(blocks)}): {e}"
                    )
                    success = False
                    break

            if success and pcm_frames:
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
                    wav_path = tmp_wav.name
                try:
                    with wave.open(wav_path, "wb") as wf:
                        wf.setnchannels(1)
                        wf.setsampwidth(2)  # 16-bit PCM
                        wf.setframerate(sample_rate)
                        wf.writeframes(b"".join(pcm_frames))

                    ffmpeg_bin = shutil.which("ffmpeg")
                    if ffmpeg_bin:
                        subprocess.run(
                            [
                                ffmpeg_bin,
                                "-y",
                                "-i",
                                wav_path,
                                "-codec:a",
                                "libmp3lame",
                                "-b:a",
                                "192k",
                                output_path,
                            ],
                            check=True,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
                    else:
                        shutil.move(wav_path, output_path)
                    print(
                        f"[✓] Audio generado con {model_name} (voz: {candidate_voice}): {output_path}"
                    )
                    return True
                finally:
                    if os.path.exists(wav_path):
                        os.remove(wav_path)

            if not voice_invalid:
                break

    return False


def synthesize_audio_edge_neural(
    text: str, output_path: str, lang: str = "es", voice: Optional[str] = None
) -> bool:
    """
    Sintetiza el texto usando las voces neuronales naturales de Microsoft Edge (`edge-tts`),
    que suenan humanas y fluidas sin requerir API key de pago.
    Voces por defecto:
      - Español (Venezuela): es-VE-SebastianNeural (alternativas: es-VE-PaolaNeural, es-CO-GonzaloNeural, es-ES-AlvaroNeural)
      - Inglés: en-US-AndrewMultilingualNeural
    """
    try:
        import edge_tts
    except ImportError:
        return False

    selected_voice = voice or (
        "es-VE-SebastianNeural" if lang == "es" else "en-US-AndrewMultilingualNeural"
    )
    print(
        f"[*] Sintetizando voz neuronal humana con Edge Neural TTS (voz: {selected_voice})..."
    )

    temp_path = output_path + ".part"

    async def _run():
        communicate = edge_tts.Communicate(text, selected_voice, rate="+4%")
        await communicate.save(temp_path)

    try:
        asyncio.run(_run())
        if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
            os.replace(temp_path, output_path)
            print(
                f"[✓] Audio neuronal generado con éxito ({selected_voice}): {output_path}"
            )
            return True
    except Exception as e:
        print(f"[!] Aviso en Edge Neural TTS: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return False


def synthesize_audio_google(text: str, output_path: str, lang: str = "es") -> bool:
    """Respaldo básico con Google Translate TTS."""
    chunks = split_into_tts_chunks(text, max_len=180)
    print(
        f"[*] Sintetizando {len(chunks)} fragmentos de voz ({lang}) con Google Translate TTS (respaldo)..."
    )

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
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
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
    api_key = load_api_key()

    print(f"[*] Preparando guion para locución (idioma: {lang})...")
    script = generate_podcast_script_with_gemini(cleaned, api_key, lang=lang)

    out_dir = os.path.dirname(article_path)
    suffix = "-en" if lang == "en" else ""
    audio_output = os.path.join(out_dir, f"podcast-episodio{suffix}.mp3")
    script_output = os.path.join(out_dir, f"guion-locucion{suffix}.txt")

    with open(script_output, "w", encoding="utf-8") as f:
        f.write(script + "\n")
    print(f"[✓] Guion guardado en: {script_output}")

    # 1. Intentar con gemini-3.8-flash-tts si hay GEMINI_API_KEY configurada
    if api_key and synthesize_audio_gemini_tts(script, audio_output, api_key, lang=lang):
        return

    # 2. Respaldo neuronal de alta calidad humana (Microsoft Edge Neural TTS, sin API key)
    if synthesize_audio_edge_neural(script, audio_output, lang=lang):
        return

    # 3. Respaldo de emergencia (Google Translate TTS)
    synthesize_audio_google(script, audio_output, lang=lang)


if __name__ == "__main__":
    main()
