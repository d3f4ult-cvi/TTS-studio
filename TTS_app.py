# ============================================================
# 0. PACKAGING SAFETY (must come before importing gradio)
# ============================================================
import os
import sys

# A windowed .exe has no console, so stdout/stderr are None and Gradio would crash.
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

# Don't send usage analytics
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"


# ============================================================
# 1. SETUP / IMPORTS
# ============================================================
import tempfile            # lets us save audio to a temporary file

import gradio as gr        # builds the web UI
from gtts import gTTS      # Google Text-to-Speech: turns text into an MP3

# Map friendly names (shown in the dropdown) to (language code, accent domain).
VOICES = {
    "English (US)":        ("en", "com"),
    "English (UK)":        ("en", "co.uk"),
    "English (Australia)": ("en", "com.au"),
    "Spanish":             ("es", "es"),
    "French":              ("fr", "fr"),
    "German":              ("de", "de"),
    "Japanese":            ("ja", "co.jp"),
}

MAX_CHARS = 1000  # protects against huge requests


# ============================================================
# 2. CORE PROCESSING FUNCTION
# ============================================================
def text_to_speech(text, voice_name, slow):
    """Convert text to speech and return the path of the generated MP3."""

    if not text or not text.strip():
        raise gr.Error("Please type some text first!")
    if len(text) > MAX_CHARS:
        raise gr.Error(f"Text is too long ({len(text)} characters). Maximum is {MAX_CHARS}.")

    lang, tld = VOICES[voice_name]

    try:
        tts = gTTS(text=text, lang=lang, tld=tld, slow=slow)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.save(tmp.name)
        return tmp.name
    except Exception:
        raise gr.Error("Speech service unavailable. Check your internet connection and try again.")


# ============================================================
# 3. GRADIO UI LAYOUT
# ============================================================
with gr.Blocks(theme=gr.themes.Soft(), title="Text-to-Speech Studio") as demo:

    gr.Markdown(
        """
        # 🎙️ Text-to-Speech Studio
        Type something, pick a voice, and hear it spoken aloud.
        """
    )

    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="Your text",
                placeholder="Hello, class! This voice was generated with Python.",
                lines=6,
                max_length=MAX_CHARS,
            )
            voice_input = gr.Dropdown(
                choices=list(VOICES.keys()),
                value="English (US)",
                label="Voice / Language",
            )
            slow_input = gr.Checkbox(label="Speak slowly", value=False)
            generate_btn = gr.Button("🔊 Generate Speech", variant="primary")

        with gr.Column():
            audio_output = gr.Audio(label="Generated speech", type="filepath")

    generate_btn.click(
        fn=text_to_speech,
        inputs=[text_input, voice_input, slow_input],
        outputs=audio_output,
    )

    gr.Examples(
        examples=[
            ["Welcome to computer science class!", "English (UK)", False],
            ["Hola, ¿cómo estás hoy?", "Spanish", False],
            ["Bonjour tout le monde, bienvenue en cours d'informatique.", "French", True],
        ],
        inputs=[text_input, voice_input, slow_input],
    )


# ============================================================
# 4. LAUNCH
# ============================================================
if __name__ == "__main__":
    # Render provides PORT. Locally it falls back to 7860.
    port = int(os.environ.get("PORT", 7860))
    is_server = "PORT" in os.environ

    demo.queue(max_size=20).launch(
        server_name="0.0.0.0" if is_server else "127.0.0.1",
        server_port=port,
        inbrowser=not is_server,   # only auto-open a browser on your own PC
    )