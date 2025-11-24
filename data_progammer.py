# analisis_programmer.py
import pandas as pd

print("MEMULAI ANALISIS DATA EXCEL...")

# 1. Baca data bersih
df = pd.read_excel("Data_Bersih.xlsx")
print(f"Data: {len(df)} baris")

# 2. Analisis negara: buyer & total transaksi (USD)
if 'shipping_country' in df.columns:
    negara = df.groupby('shipping_country').agg(
        buyer=('customer_id', 'count'),
        total_transaksi_usd=('total_amount', 'sum')
    ).reset_index()
    
    # Urutkan dari terbanyak
    negara = negara.sort_values(by='buyer', ascending=False).reset_index(drop=True)
    
    # Konversi ke Rupiah
    KURS = 16000
    negara['total_transaksi_idr'] = negara['total_transaksi_usd'] * KURS

    # konversi dollar rupiah perkolom 
    df['total_amount']=df['total_amount']/100
    df['total_amount'] = df['total_amount'].round(2)
    df['kon']=df['total_amount']*KURS
    df['rupiah']=df['kon'].apply(lambda rp : f"Rp  {(rp):,.0f}".replace(",","."))
    df=df[['order_id','customer_id','order_date','total_amount','payment_method','shipping_country','month','year','rupiah']]
    
    # Format Rupiah (string untuk tampilan)
    negara['total_transaksi_idr_str'] = negara['total_transaksi_idr'].apply(
        lambda x: f"Rp {int(x):,}".replace(",", ".")
    )
    
    print("Analisis negara selesai")
else:
    print("Kolom 'shipping_country' tidak ditemukan")
    negara = pd.DataFrame()

# 3. Simpan hasil analisis
if not negara.empty:
    output = "Data_Analisis.xlsx"
    with pd.ExcelWriter(output) as writer:
        df.to_excel(writer, sheet_name="Data_Bersih", index=False)
        negara.to_excel(writer, sheet_name="Negara_Analisis", index=False)
    print(f"Hasil analisis disimpan di '{output}'")
else:
    # Jika tidak ada analisis, cukup simpan data bersih
    df.to_excel("Data_Analisis.xlsx", index=False)
    print("Data bersih disimpan sebagai 'Data_Analisis.xlsx'")

print("\n+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+ OUTPUT DATA ANALISIS +_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+\n")
print(df)
print("\n+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+ OUTPUT DATA NEGARA +_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+\n")
print(negara)

