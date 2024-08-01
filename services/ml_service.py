from flask import Flask, request, jsonify

app = Flask(__name__)

class MLService:
    def __init__(self):
        self.models = {}

    def train_model(self, model_name, data):
        # Placeholder for training logic
        self.models[model_name] = "trained_model"
        return f"Model {model_name} trained"

    def predict(self, model_name, input_data):
        # Placeholder for prediction logic
        if model_name in self.models:
            return f"Prediction for {input_data} using {model_name}"
        else:
            return "Model not found"

ml_service = MLService()

@app.route('/')
def index():
    return "Welcome to the ML Service API!"

@app.route('/train', methods=['POST'])
def train_model():
    data = request.get_json()
    model_name = data['model_name']
    training_data = data['training_data']
    response = ml_service.train_model(model_name, training_data)
    return jsonify({"message": response}), 201

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    model_name = data['model_name']
    input_data = data['input_data']
    response = ml_service.predict(model_name, input_data)
    if response == "Model not found":
        return jsonify({"error": response}), 404
    return jsonify({"prediction": response}), 200

if __name__ == '__main__':
    app.run(debug=True)
