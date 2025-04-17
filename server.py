from flask import Flask, request, send_file
from tortoise.api import TextToSpeech
import tempfile

app = Flask(__name__)
tts = TextToSpeech()

@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    text = data.get("text", "")
    voice = data.get("voice", "pat")  # Choose your preferred voice
    gen = tts.tts(text, voice=voice, use_deterministic_seed=False)
    
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    gen.save(tmp.name)
    
    return send_file(tmp.name, mimetype='audio/wav')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
