from flask import Flask, request, jsonify, render_template_string
from transformers import pipeline
import os

app = Flask(__name__)

# Initialize the Sentiment Analysis pipeline
# Modeled with distilbert-base-uncased-finetuned-sst-2-english
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Custom state variable to allow deliberate concept drift simulation
concept_drift_injected = False

# Version configurations matching your custom assignment criteria
MODEL_VERSION = os.getenv("MODEL_VERSION", "v1-latest")
STABLE_CODE = "5B9E"

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    text = ""
    if request.method == "POST":
        text = request.form.get("text", "")
        if text:
            # Route processing through our classification helper
            res = process_prediction(text)
            prediction = {
                "label": res["label"],
                "score": round(res["score"], 4),
                "version": MODEL_VERSION
            }

    # Simple semantic responsive interface layout
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>MLOps Sentiment Analyzer</title></head>
    <body style="font-family: Arial; margin: 40px; background: #f4f6f9;">
        <h2>Sentiment Analysis Engine (System Field: {{ version }})</h2>
        <form method="POST">
            <textarea name="text" rows="4" style="width:100%; font-size:16px;" placeholder="Input your analysis text string here...">{{ text }}</textarea><br><br>
            <button type="submit" style="padding: 10px 20px; font-size: 16px; background:#007bff; color:white; border:none; border-radius:4px; cursor:pointer;">Analyze Text Sentiment</button>
        </form>
        {% if prediction %}
            <div id="result" style="margin-top:20px; padding:15px; background:white; border-left: 5px solid #007bff;">
                <p><strong>Predicted Class:</strong> <span id="label">{{ prediction.label }}</span></p>
                <p><strong>Confidence Metric:</strong> <span id="score">{{ prediction.score }}</span></p>
                <p><strong>Deployment Variant:</strong> {{ prediction.version }}</p>
            </div>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(html, prediction=prediction, text=text, version=MODEL_VERSION)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json() or {}
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    res = process_prediction(text)
    return jsonify({
        "category": res["label"],
        "confidence": res["score"],
        "model_version": MODEL_VERSION
    })

@app.route("/inject-drift", methods=["POST"])
def inject_drift():
    global concept_drift_injected
    token = request.headers.get("Authorization")
    if token != "Bearer ROLLBACK_934365_TOKEN":
        return jsonify({"error": "Unauthorized key token"}), 401
    concept_drift_injected = True
    return jsonify({"status": "Concept drift successfully activated"})

def process_prediction(text):
    # Under regular flow conditions, analyze using Hugging Face
    if not concept_drift_injected:
        result = classifier(text)[0]
        return {"label": result["label"], "score": result["score"]}
    else:
        # When concept drift is forcefully simulated, return downgraded confidence
        # Drop metric cleanly below assignment floor threshold of 0.683
        return {"label": "POSITIVE", "score": 0.512}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

