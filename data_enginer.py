import pandas as pd

# ================================
# 1. LOAD DATA
# ================================
df = pd.read_excel("Data_fiksr.xlsx")   # ganti dengan nama file kamu


# ================================
# 2. BERSIHKAN kolom total_amount
#  - handle format koma → titik
#  - ubah ke float
# ================================
df["total_amount"] = (
    df["total_amount"]
    .astype(str)
    .str.replace(".", "")      # hilangkan pemisah ribuan jika ada
    .str.replace(",", ".")     # ubah desimal ke format titik
    .astype(float)
)


# ================================
# 3. HAPUS BARIS DENGAN total_amount = 0
# ================================
df = df[df["total_amount"] != 0]


# ================================
# 4. HAPUS DUPLIKAT PADA customer_id
#    keep="first" → data pertama disimpan, sisanya dihapus
# ================================
df = df.drop_duplicates(subset="customer_id", keep="first")


# ================================
# 5. NORMALISASI order_date
#    otomatis mendeteksi format tanggal
# ================================
df["order_date"] = pd.to_datetime(df["order_date"], dayfirst=False)


# ================================
# 6. TAMBAHKAN KOLOM month
#    berisi nama bulan: January, February, dst.
# ================================
df["month"] = df["order_date"].dt.strftime("%B")


# ================================
# 7. SIMPAN HASIL
# ================================
df.to_excel("Data_Final.xlsx", index=False)

print("Proses selesai! File tersimpan sebagai Data_Final.xlsx")