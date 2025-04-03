from flask import Flask, request, jsonify

from model_api.model import SentimentModel

app = Flask(__name__)

model = SentimentModel()


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    review = data.get('review', '')

    if not review:
        return jsonify({"error": "No review provided"}), 400

    result = model.predict(review)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
