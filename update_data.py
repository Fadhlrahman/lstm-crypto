import pandas as pd
from datetime import datetime
from pycoingecko import CoinGeckoAPI
import os

# Inisialisasi CoinGecko
cg = CoinGeckoAPI()

# Mapping CoinGecko ID ke nama file CSV
coins = {
    "bitcoin": "bitcoin.csv",
    "ethereum": "ethereum.csv",
    "dogecoin": "dogecoin.csv",
    "solana": "solana.csv",
    "ripple": "xrp.csv"
}

# Ambil harga semua koin sekaligus
ids = ','.join(coins.keys())
prices = cg.get_price(ids=ids, vs_currencies='usd')

# Tanggal hari ini
today = datetime.today().strftime('%Y-%m-%d')

# Buat folder data kalau belum ada
os.makedirs("data", exist_ok=True)

# Update masing-masing CSV
for coin_id, filename in coins.items():
    harga = prices.get(coin_id, {}).get('usd')
    if harga is None:
        print(f" Gagal ambil harga untuk {coin_id}")
        continue

    file_path = os.path.join("data", filename)
    df = pd.read_csv(file_path, encoding="utf-8-sig")

    # Cek apakah tanggal hari ini sudah ada
    if today in df["date"].astype(str).values:
        print(f"⏭ Data {coin_id.upper()} untuk {today} sudah ada, dilewati.")
        continue

    # Tambahkan baris baru
    new_row = pd.DataFrame({
        "date": [today],
        "close": [harga],
        "type": ["actual"]
    })

    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(file_path, index=False, encoding="utf-8-sig")
    print(f" Harga {coin_id.upper()} {today} = ${harga} ditambahkan ke {filename}")
