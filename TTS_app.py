# ============================================================
# 1. SETUP / IMPORTS
# ============================================================
import tempfile            # lets us save audio to a temporary file

import gradio as gr        # builds the web UI
from gtts import gTTS      # Google Text-to-Speech: turns text into an MP3

# Map friendly names (shown in the dropdown) to (language code, accent domain).
# The "tld" is the Google domain, which changes the accent of the voice.
VOICES = {
    "English (US)":        ("en", "com"),
    "English (UK)":        ("en", "co.uk"),
    "English (Australia)": ("en", "com.au"),
    "Spanish":             ("es", "es"),
    "French":              ("fr", "fr"),
    "German":              ("de", "de"),
    "Japanese":            ("ja", "co.jp"),
}


# ============================================================
# 2. CORE PROCESSING FUNCTION
# ============================================================
def text_to_speech(text, voice_name, slow):
    """Convert text to speech and return the path of the generated MP3."""

    # Basic input validation: show a friendly error popup in the UI
    if not text or not text.strip():
        raise gr.Error("Please type some text first!")

    # Look up the language code and accent for the chosen voice
    lang, tld = VOICES[voice_name]

    # Ask gTTS to build the speech
    tts = gTTS(text=text, lang=lang, tld=tld, slow=slow)

    # Save to a temporary .mp3 file and return its path.
    # Gradio's Audio component can play any file path it receives.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts.save(tmp.name)

    return tmp.name


# ============================================================
# 3. GRADIO UI LAYOUT
# ============================================================
with gr.Blocks(theme=gr.themes.Soft(), title="Text-to-Speech Studio") as demo:

    # Title and description (Markdown is supported)
    gr.Markdown(
        """
        # 🎙️ Text-to-Speech Studio
        Type something, pick a voice, and hear it spoken aloud.
        """
    )

    with gr.Row():
        # Left column: inputs
        with gr.Column():
            text_input = gr.Textbox(
                label="Your text",
                placeholder="Hello, class! This voice was generated with Python.",
                lines=6,
            )
            voice_input = gr.Dropdown(
                choices=list(VOICES.keys()),
                value="English (US)",
                label="Voice / Language",
            )
            slow_input = gr.Checkbox(label="Speak slowly", value=False)
            generate_btn = gr.Button("🔊 Generate Speech", variant="primary")

        # Right column: output
        with gr.Column():
            audio_output = gr.Audio(label="Generated speech", type="filepath")

    # Wire it up: when the button is clicked, run our function.
    # inputs  -> arguments passed to text_to_speech (in order)
    # outputs -> where the returned value is displayed
    generate_btn.click(
        fn=text_to_speech,
        inputs=[text_input, voice_input, slow_input],
        outputs=audio_output,
    )

    # Clickable examples so you can demo instantly
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
    demo.launch(inbrowser=True)