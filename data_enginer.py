# data_cleaning.py
import pandas as pd
import os

print(" MEMULAI PEMBERSIHAN DATA...")
if "Data_fiksr.csv" not in os.listdir():
    raise FileNotFoundError("Data_fiksr.csv tidak ditemukan!")

# 1. Load
data = pd.read_csv("Data_fiksr.csv")
print(f"Baca {len(data)} baris")

# 2. Bersihkan total_amount & hapus 0
data["total_amount"] = (
    data["total_amount"].astype(str)
    .str.strip()
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
)
data["total_amount"] = pd.to_numeric(data["total_amount"], errors="coerce")
data = data[data["total_amount"] != 0]
print(f"Hapus nilai 0 → sisa {len(data)} baris")

# 3. Normalisasi tanggal (tanpa jam)
data["order_date"] = pd.to_datetime(data["order_date"], errors="coerce")
data = data[data["order_date"].notna()]
data["order_date"] = data["order_date"].dt.date

# 4. Tambah kolom bulan
data["order_date"] = pd.to_datetime(data["order_date"])
data["month"] = data["order_date"].dt.strftime("%B")
data["year"] = data["order_date"].dt.year  # tambahkan year untuk visualisasi tahunan
data["order_date"] = data["order_date"].dt.date

# 5. Hapus duplikat customer_id
# data = data.drop_duplicates(subset="customer_id", keep="first")
# print(f"Hapus duplikat → sisa {len(data)} baris")

# 6. Output
print("==================")
print(data[['order_id', 'customer_id', 'total_amount', 'order_date', 'month', 'year']].head())
print("==================")

# 7. Simpan
output = "Data_Bersih.xlsx"
data.to_excel(output, index=False)
print(f"Selesai! Data bersih tersimpan di '{output}'")