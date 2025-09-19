from flask import Flask, request, send_file
from gtts import gTTS
from pydub import AudioSegment
import io

app = Flask(__name__)

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text", "")
    lang = data.get("lang", "en")

    if not text:
        return {"error": "Missing text"}, 400

    # Generate speech as MP3 (gTTS only outputs mp3)
    mp3_fp = io.BytesIO()
    tts = gTTS(text=text, lang=lang)
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    # Convert MP3 → OGG (Opus) using pydub
    mp3_audio = AudioSegment.from_file(mp3_fp, format="mp3")
    ogg_fp = io.BytesIO()
    mp3_audio.export(ogg_fp, format="ogg", codec="libopus", bitrate="32k")
    ogg_fp.seek(0)

    # Return OGG file (WhatsApp accepts audio/ogg with Opus codec)
    return send_file(ogg_fp, mimetype="audio/ogg", download_name="tts.ogg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

