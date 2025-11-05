from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# load
pipeline = joblib.load("news_classifier_pipeline.joblib")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' in JSON body"}), 400
    text = data['text']
    # predict_proba returns probability for class 0 and 1; our mapping: 0->FAKE, 1->REAL
    proba = pipeline.predict_proba([text])[0]
    pred = pipeline.predict([text])[0]
    label = "REAL" if pred == 1 else "FAKE"
    confidence = float(proba[pred])  # probability of predicted class
    return jsonify({"label": label, "confidence": round(confidence, 4)})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
