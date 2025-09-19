from flask import Flask, request, send_file
from gtts import gTTS
import io

app = Flask(__name__)

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text", "")
    lang = data.get("lang", "en")

    if not text:
        return {"error": "Missing text"}, 400

    # Generate speech
    tts = gTTS(text=text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)

    return send_file(fp, mimetype="audio/mpeg", download_name="tts.mp3")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
