import pandas as pd
import os

# ================================
# Cek file dalam folder (opsional)
# ================================
print("File dalam folder:", os.listdir())

# ================================
# 1. LOAD DATA (CSV)
# ================================
df = pd.read_csv("Data_fiksr.csv")
print("✓ File CSV berhasil dibaca")


# ================================
# 2. BERSIHKAN kolom total_amount
#    - hilangkan ribuan (.)
#    - ubah koma → titik
#    - ubah ke float
# ================================
df["total_amount"] = (
    df["total_amount"]
    .astype(str)
    .str.replace(".", "", regex=False)     # hilangkan pemisah ribuan
    .str.replace(",", ".", regex=False)    # ubah koma → titik
)

df["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce")
print("✓ Kolom total_amount dibersihkan")


# ================================
# 3. HAPUS BARIS total_amount = 0 atau NaN
# ================================
df = df[df["total_amount"].notna()]
df = df[df["total_amount"] != 0]
print("✓ Baris total_amount 0/NaN dibuang")


# ================================
# 4. HAPUS DUPLIKAT berdasarkan customer_id
# ================================
df = df.drop_duplicates(subset="customer_id", keep="first")
print("✓ Duplikat customer_id dibuang")


# ================================
# 5. NORMALISASI order_date
# ================================
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

# hapus baris tanggal rusak
df = df[df["order_date"].notna()]
print("✓ order_date berhasil dinormalisasi")


# ================================
# 6. TAMBAH KOLOM month
# ================================
df["month"] = df["order_date"].dt.strftime("%B")
print("✓ Kolom month ditambahkan")


# ================================
# 7. SIMPAN HASIL
# ================================
df.to_excel("Data_Final.xlsx", index=False)
print("🎉 Proses selesai! File tersimpan sebagai Data_Final.xlsx")
