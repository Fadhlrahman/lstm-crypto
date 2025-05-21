### FILE 1: train_lstm.py (Versi Multi-Koin)

import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import os

# Multi-koin mapping
COIN_MAP = {
    "btc": "data/bitcoin.csv",
    "eth": "data/ethereum.csv",
    "doge": "data/dogecoin.csv",
    "sol": "data/solana.csv",
    "xrp": "data/xrp.csv",
}

def normalize(data):
    min_val = data.min()
    max_val = data.max()
    return (data - min_val) / (max_val - min_val), min_val, max_val

def train_lstm_model(csv_path, model_path, pred_steps=[1, 3, 7]):
    df = pd.read_csv(csv_path)
    df = df["close"].dropna().values.reshape(-1, 1)
    normalized, min_val, max_val = normalize(df)

    SEQ_LEN = 60
    X, y = [], []
    for i in range(SEQ_LEN, len(normalized) - max(pred_steps)):
        X.append(normalized[i-SEQ_LEN:i])
        y.append([normalized[i + offset] for offset in pred_steps])

    X, y = np.array(X), np.array(y)

    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=(SEQ_LEN, 1)),
        LSTM(64),
        Dense(len(pred_steps))
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')  # tanpa metrics
    model.fit(X, y, epochs=20, batch_size=32)
    model.save(model_path)
    print(f" Model disimpan ke {model_path}")

if __name__ == "__main__":
    os.makedirs("models", exist_ok=True)
    for coin, path in COIN_MAP.items():
        model_path = f"models/model_{coin}.h5"
        print(f" Training model untuk {coin.upper()}...")
        train_lstm_model(path, model_path)
