from flask import Flask, request, jsonify
from deepface import DeepFace
import os

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    print("---- REQUEST RECEIVED ----")
    print("Content-Type:", request.content_type)
    print("Files:", request.files)
    print("Form keys:", request.form)

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img_path = "temp.jpg"
    img.save(img_path)

    try:
        result = DeepFace.analyze(img_path, actions=["emotion"])
        print("Analysis result:", result)
        return jsonify(result)
    except Exception as e:
        print("DeepFace error:", str(e))
        return jsonify({"error": str(e)}), 500
