from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

model, le_protocol, le_flags, le_label = pickle.load(open("model.pkl", "rb"))
history = []

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    input_df = pd.DataFrame([data])
    input_df['Protocol'] = le_protocol.transform(input_df['Protocol'])
    input_df['Flags'] = le_flags.transform(input_df['Flags'])
    input_df = input_df[['Protocol', 'Packet_Size', 'Flow_Duration', 'Flags']]

    prediction = model.predict(input_df)[0]
    label = le_label.inverse_transform([prediction])[0]

    result = {
        'prediction': label,
        'Src_IP': data.get('Src_IP', ''),
        'Dst_IP': data.get('Dst_IP', '')
    }

    history.append(result)
    return jsonify(result)

@app.route("/history", methods=["GET"])
def get_history():
    return jsonify(history[-60:])

if __name__ == "__main__":
    app.run(debug=True)
