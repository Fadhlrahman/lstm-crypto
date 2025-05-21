import subprocess

print("Update data dari CoinGecko...")
subprocess.run(["python", "update_data.py"])

print("Retraining model semua koin...")
subprocess.run(["python", "train/train_lstm.py"])

print("Selesai.")
