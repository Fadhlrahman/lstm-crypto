###  FILE 2: app.py (Flask API dengan metode GET untuk prediksi harga kripto)

from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# Peta nama koin ke file data CSV
COIN_FILES = {
    "btc": "data/bitcoin.csv",
    "eth": "data/ethereum.csv",
    "doge": "data/dogecoin.csv",
    "sol": "data/solana.csv",
    "xrp": "data/xrp.csv"
}

# Fungsi normalisasi manual
def normalize(data):
    min_val = data.min()
    max_val = data.max()
    scaled = (data - min_val) / (max_val - min_val)
    return scaled, min_val, max_val

# Fungsi untuk mengembalikan nilai ke skala aslinya
def denormalize(normalized, min_val, max_val):
    return normalized * (max_val - min_val) + min_val

@app.route("/predict", methods=["GET"])
def predict():
    coin = request.args.get("coin", "").lower()
    range_str = request.args.get("range", "1")

    try:
        range_days = int(range_str)
        if range_days not in [1, 3, 7]:
            return jsonify({"error": "Range hanya boleh 1, 3, atau 7 hari"}), 400
    except ValueError:
        return jsonify({"error": "Parameter range harus berupa angka"}), 400

    if coin not in COIN_FILES:
        return jsonify({"error": "Koin tidak dikenali"}), 404

    data_path = COIN_FILES[coin]
    model_path = f"models/model_{coin}.h5"

    if not os.path.exists(data_path) or not os.path.exists(model_path):
        return jsonify({"error": "Data atau model tidak ditemukan"}), 404

    df = pd.read_csv(data_path)
    model = load_model(model_path)

    close_prices = df["close"].values.reshape(-1, 1)
    scaled_prices, min_val, max_val = normalize(close_prices)

    if len(scaled_prices) < 60:
        return jsonify({"error": "Data kurang dari 60 baris untuk prediksi"}), 400

    input_data = scaled_prices[-60:].reshape(1, 60, 1)
    predictions = model.predict(input_data)[0]  # Hasil prediksi [3 angka]

    # Denormalisasi semua prediksi
    predicted_prices = denormalize(predictions, min_val, max_val)

    return jsonify({
        "coin": coin.upper(),
        "day_1": f"${predicted_prices[0]:,.2f}" if len(predicted_prices) > 0 else "N/A",
        "day_3": f"${predicted_prices[1]:,.2f}" if len(predicted_prices) > 1 else "N/A",
        "day_7": f"${predicted_prices[2]:,.2f}" if len(predicted_prices) > 2 else "N/A"
    })



if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
