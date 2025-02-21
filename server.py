from flask import Flask, request, jsonify
import whisper
import os

app = Flask(__name__)
model = whisper.load_model("base")  # Using a small model for faster response

WAKE_WORD = "hello bank"  # Define the wake word

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/detect_wake_word", methods=["POST"])
def detect_wake_word():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    file = request.files["audio"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    result = model.transcribe(filepath)
    transcript = result["text"].lower()

    if WAKE_WORD in transcript:
        return jsonify({"wake_word_detected": True, "transcription": transcript})
    else:
        return jsonify({"wake_word_detected": False, "transcription": transcript})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
