from flask import Flask, request, jsonify
from deepface import DeepFace
from flask_cors import CORS
import tempfile

app = Flask(__name__)
CORS(app)

@app.route("/detect-mood", methods=["POST"])
def detect_mood():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files['image']

    with tempfile.NamedTemporaryFile(delete=False) as temp:
        image.save(temp.name)

        try:
            analysis = DeepFace.analyze(img_path=temp.name, actions=["emotion"])
            dominant_emotion = analysis[0]["dominant_emotion"]
            return jsonify({"mood": dominant_emotion})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "DeepFace Mood Detection API is running."

if __name__ == "__main__":
    app.run(debug=True)
