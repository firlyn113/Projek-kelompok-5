# visualisasi.py
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.ticker as mticker


def rupiah_formatter(x, pos):
    return f'Rp{int(x):,}'.replace(',', '.')

rupiah_func = mticker.FuncFormatter(rupiah_formatter)


# Pastikan folder output ada
os.makedirs("output_grafik", exist_ok=True)

print("🎨 MEMULAI VISUALISASI...")

# 1. Baca data bersih
df = pd.read_excel("Data_Bersih.xlsx")
print(f"Data: {len(df)} baris")

# 2. GRAFIK 1: Pie Chart — Metode Pembayaran Terbanyak
if 'payment_method' in df.columns:
    plt.figure(figsize=(8, 6))
    payment_counts = df['payment_method'].value_counts()
    plt.pie(payment_counts, labels=payment_counts.index, autopct='%1.1f%%', startangle=90, 
            colors=['#FFB3BA', '#BAFFC9', '#BAE1FF','#FFFFBA',])
    plt.title("Distribusi Metode Pembayaran", fontsize=14)
    plt.tight_layout()
    plt.savefig("output_grafik/pie_payment.png", dpi=300)
    plt.show()
    print("Pie chart: metode pembayaran")
else:
    print("Kolom 'payment_method' tidak ditemukan — lewati pie chart")

# 3. GRAFIK 2: Mountain Plot (Area) — Transaksi per Negara
if 'shipping_country' in df.columns:
    # Ambil top 10 negara (untuk readability)
    top_negara = df['shipping_country'].value_counts().head(10).index
    df_top = df[df['shipping_country'].isin(top_negara)]
    
    # Agregat total per negara
    negara_sum = df_top.groupby('shipping_country')['total_amount'].sum().sort_values(ascending=False)
    
    plt.figure(figsize=(10, 6))
    plt.fill_between(range(len(negara_sum)), negara_sum.values, alpha=0.7, color='skyblue')
    plt.plot(negara_sum.values, marker='o', color='navy')
    plt.xticks(range(len(negara_sum)), negara_sum.index, rotation=45)
    plt.ylabel("Total Transaksi (Per Juta/USD)")
    plt.title("Total Transaksi per Negara (Top 10)", fontsize=14)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("output_grafik/mountain_negara.png", dpi=300)
    plt.show()
    print("Mountain plot: transaksi per negara")
else:
    print("Kolom 'shipping_country' tidak ditemukan — lewati mountain plot")

# 4. GRAFIK 3: Bar Chart — Penjualan per Bulan
if 'month' in df.columns and 'year' in df.columns:
    # Untuk urutan bulan benar, buat mapping
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    df['month_cat'] = pd.Categorical(df['month'], categories=month_order, ordered=True)
    monthly = df.groupby('month_cat')['total_amount'].sum().reindex(month_order).fillna(0)
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(monthly.index, monthly.values, color='lightcoral', edgecolor='black')
    plt.ylabel("Total Penjualan (USD)")
    plt.title("Penjualan per Bulan", fontsize=14)
    plt.xticks(rotation=45)
    
    # Tambahkan nilai di atas bar
    for bar, val in zip(bars, monthly.values):
        if val > 0:
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + val*0.01,
                     f'${val:,.0f}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig("output_grafik/bar_bulan.png", dpi=300)
    plt.show()
    print("Bar chart: penjualan per bulan")
else:
    print("Kolom 'month' atau 'year' tidak lengkap — lewati bar chart")

# 5. GRAFIK 4: Line Chart — Penjualan per Tahun
if 'year' in df.columns:
    yearly = df.groupby('year')['total_amount'].sum()
    
    plt.figure(figsize=(10, 6))
    plt.plot(yearly.index, yearly.values, marker='o', linestyle='-', color='green', linewidth=2)
    plt.title("Tren Penjualan per Tahun", fontsize=14)
    plt.xlabel("Tahun")
    plt.ylabel("Total Penjualan (USD)")
    plt.grid(alpha=0.3)
    
    # Tambahkan nilai di titik
    for x, y in zip(yearly.index, yearly.values):
        plt.text(x, y, f'${y:,.0f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig("output_grafik/line_tahun.png", dpi=300)
    plt.show()
    print("Line chart: penjualan per tahun")
else:
    print("Kolom 'year' tidak ditemukan — lewati line chart")

print("\nSEMUA GRAFIK TERSIMPAN DI FOLDER 'output_grafik/'")