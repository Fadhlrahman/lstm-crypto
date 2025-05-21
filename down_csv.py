import yfinance as yf
import os
import pandas as pd

# Buat folder jika belum ada
os.makedirs("data", exist_ok=True)

# Mapping simbol Yahoo Finance → nama file CSV
coins = {
    "BTC-USD": "bitcoin.csv",
    "ETH-USD": "ethereum.csv",
    "DOGE-USD": "dogecoin.csv",
    "SOL-USD": "solana.csv",
    "XRP-USD": "xrp.csv"
}

# Rentang waktu
start_date = "2017-01-01"
end_date = "2025-12-31"  # Batas tinggi, ambil sampai tanggal terakhir tersedia

# Loop semua koin
for symbol, filename in coins.items():
    print(f" Mengunduh data {symbol}...")

    try:
        df = yf.download(symbol, start=start_date, end=end_date)

        if df.empty:
            print(f"  Data kosong untuk {symbol}, dilewati.")
            continue

        df = df[["Close"]].reset_index()  # Ambil tanggal & harga
        df.columns = ["date", "close"]    # Rename kolom
        df["type"] = "actual"             # Tambahkan kolom type

        df.to_csv(f"data/{filename}", index=False, encoding="utf-8-sig")
        print(f" {filename} berhasil disimpan. Data sampai: {df['date'].max().date()}")

    except Exception as e:
        print(f" Error saat unduh {symbol}: {e}")
