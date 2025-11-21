# data_cleaning.py
import pandas as pd
import os

print("🧹 MEMULAI PEMBERSIHAN DATA...")
if "Data_fiksr.csv" not in os.listdir():
    raise FileNotFoundError("❌ Data_fiksr.csv tidak ditemukan!")

# 1. Load
df = pd.read_csv("Data_fiksr.csv")
print(f"✅ Baca {len(df)} baris")

# 2. Bersihkan total_amount & hapus 0
df["total_amount"] = (
    df["total_amount"].astype(str)
    .str.strip()
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
)
df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce")
df = df[df["total_amount"] != 0]
print(f"✅ Hapus nilai 0 → sisa {len(df)} baris")

# 3. Normalisasi tanggal (tanpa jam)
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df = df[df["order_date"].notna()]
df["order_date"] = df["order_date"].dt.date

# 4. Tambah kolom bulan
df["order_date"] = pd.to_datetime(df["order_date"])
df["month"] = df["order_date"].dt.strftime("%B")
df["year"] = df["order_date"].dt.year  # tambahkan year untuk visualisasi tahunan
df["order_date"] = df["order_date"].dt.date

# 5. Hapus duplikat customer_id
df = df.drop_duplicates(subset="customer_id", keep="first")
print(f"✅ Hapus duplikat → sisa {len(df)} baris")

# 6. Simpan
output = "Data_Bersih.xlsx"
df.to_excel(output, index=False)
print(f"🎉 Selesai! Data bersih tersimpan di '{output}'")