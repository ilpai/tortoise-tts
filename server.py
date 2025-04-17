from flask import Flask, request, send_file, jsonify
from tortoise.api import TextToSpeech
import tempfile
import os

app = Flask(__name__)
tts = TextToSpeech()

@app.route('/')
def index():
    return jsonify({
        "status": "ok",
        "message": "Tortoise-TTS API is running!",
        "endpoints": ["/speak (POST)"]
    })

@app.route('/speak', methods=['POST'])
def speak():
    try:
        data = request.get_json(force=True)
        text = data.get("text", "")
        voice = data.get("voice", "pat")

        if not text:
            return jsonify({"error": "Missing 'text' in request"}), 400

        print(f"Generating speech with voice: {voice}")
        gen = tts.tts(text, voice=voice, use_deterministic_seed=False)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            gen.save(tmp.name)
            return send_file(tmp.name, mimetype="audio/wav", as_attachment=True, download_name="speech.wav")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
