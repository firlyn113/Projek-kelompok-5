# visualisasi.py
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as mticker


def rupiah_formatter(x, pos):
    """Formatter untuk menampilkan angka dalam format Rupiah: Rp 1.234.560"""
    return f'Rp{int(x):,}'.replace(',', '.')

rupiah = mticker.FuncFormatter(rupiah_formatter)


# Pastikan folder output ada
os.makedirs("output_grafik", exist_ok=True)

print("🎨 MEMULAI VISUALISASI...")

# 1. Baca data bersih
df = pd.read_excel("Data_Analisis.xlsx")
print(f"Data: {len(df)} baris")

# 2. KONVERSI ke Rupiah (asumsi 1 USD = 16.000 IDR)
# Anda bisa ubah nilai kurs di sini jika perlu
KURS_USD_TO_IDR = 16000
df['total_rupiah'] = df['total_amount'] * KURS_USD_TO_IDR

# 3. GRAFIK 1: Pie Chart — Metode Pembayaran Terbanyak
if 'payment_method' in df.columns:
    plt.figure(figsize=(8, 6))
    payment_counts = df['payment_method'].value_counts()
    plt.pie(payment_counts, labels=payment_counts.index, autopct='%1.1f%%', startangle=90,
            colors=['#FFB3BA', '#BAFFC9', '#BAE1FF', '#FFFFBA'])
    plt.title("Distribusi Metode Pembayaran", fontsize=14)
    plt.tight_layout()
    plt.savefig("output_grafik/pie_payment.png", dpi=300)
    plt.show()
    print("Pie chart: metode pembayaran")
else:
    print("Kolom 'payment_method' tidak ditemukan — lewati pie chart")

# 4. GRAFIK 2: Mountain Plot (Area) — Transaksi per Negara
if 'shipping_country' in df.columns:
    top_negara = df['shipping_country'].value_counts().head(10).index
    df_top = df[df['shipping_country'].isin(top_negara)]
    negara_sum = df_top.groupby('shipping_country')['total_rupiah'].sum().sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    plt.fill_between(range(len(negara_sum)), negara_sum.values, alpha=0.7, color='skyblue')
    plt.plot(negara_sum.values, marker='o', color='navy')
    plt.xticks(range(len(negara_sum)), negara_sum.index, rotation=45)
    plt.ylabel("Total Transaksi")
    plt.gca().yaxis.set_major_formatter(rupiah)
    plt.title("Total Transaksi per Negara (Top 10)", fontsize=14)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("output_grafik/mountain_negara.png", dpi=300)
    plt.show()
    print("Mountain plot: transaksi per negara")
else:
    print("Kolom 'shipping_country' tidak ditemukan — lewati mountain plot")

# 5. GRAFIK 3: Bar Chart — Penjualan per Bulan
if 'month' in df.columns and 'year' in df.columns:
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    df['month_cat'] = pd.Categorical(df['month'], categories=month_order, ordered=True)
    monthly = df.groupby('month_cat')['total_rupiah'].sum().reindex(month_order).fillna(0)

    plt.figure(figsize=(10, 6))
    bars = plt.bar(monthly.index, monthly.values, color='lightcoral', edgecolor='black')
    plt.ylabel("Total Penjualan")
    plt.gca().yaxis.set_major_formatter(rupiah)
    plt.title("Penjualan per Bulan", fontsize=14)
    plt.xticks(rotation=45)

    # Tambahkan nilai di atas bar
    for bar, val in zip(bars, monthly.values):
        if val > 0:
            formatted_val = f'Rp{int(val):,}'.replace(',', '.')
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + val*0.01,
                     formatted_val, ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig("output_grafik/bar_bulan.png", dpi=300)
    plt.show()
    print("Bar chart: penjualan per bulan")
else:
    print("Kolom 'month' atau 'year' tidak lengkap — lewati bar chart")

# 6. GRAFIK 4: Line Chart — Penjualan per Tahun
if 'year' in df.columns:
    yearly = df.groupby('year')['total_rupiah'].sum()

    plt.figure(figsize=(10, 6))
    plt.plot(yearly.index, yearly.values, marker='o', linestyle='-', color='green', linewidth=2)
    plt.title("Tren Penjualan per Tahun", fontsize=14)
    plt.xlabel("Tahun")
    plt.ylabel("Total Penjualan")
    plt.gca().yaxis.set_major_formatter(rupiah)
    plt.grid(alpha=0.3)

    # Tambahkan nilai di titik
    for x, y in zip(yearly.index, yearly.values):
        formatted_val = f'Rp{int(y):,}'.replace(',', '.')
        plt.text(x, y, formatted_val, ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig("output_grafik/line_tahun.png", dpi=300)
    plt.show()
    print("Line chart: penjualan per tahun")
else:
    print("Kolom 'year' tidak ditemukan — lewati line chart")

print("\n✅ SEMUA GRAFIK TERSIMPAN DI FOLDER 'output_grafik/'")