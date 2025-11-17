import pandas as pd

#Membaca data enginer
buka_file = "Data_Final.xlsx"
file = pd.read_excel(buka_file)

#Konversi dollar ke rupiah 
def usd_ke_idr(dollar):
    kurs = 16000
    return dollar*kurs

file['rupiah']=file['total_amount'].apply(usd_ke_idr)

#format rupiah
def format_rupiah(rp):
    rp = int(rp)
    rp = f"{rp : ,}"
    format = rp.replace(",",".")
    return format

file['rupiah_conversion']=file['rupiah'].apply(format_rupiah)

#mencetak setiap kolom excel
file = file[['order_id','customer_id','order_date','total_amount','payment_method','shipping_country','month','rupiah_conversion']]

#mengurutkan data negara dari banyaknya total pembelanjaan
negara= file.groupby('shipping_country')['customer_id'].count().reset_index(name='buyer')
urut_negara= negara.sort_values(by='buyer', ascending=False)

#menampilkan data file 
print("------------- DATA AMAZON -------------")
print(file)
print("------------- DATA NEGARA DAN BANYAKNYA PEMBELI -------------")
print(urut_negara)

#eksport file ke excel
eksport_file = 'Data_Baru.xlsx'
file.to_excel(eksport_file, index=False)

#menambahkan sheet baru untuk data negara dan banyaknya pembeli
with pd.ExcelWriter(eksport_file, mode='a', engine='openpyxl') as sheet:
    urut_negara.to_excel(sheet, sheet_name="negara dan pembeli", index=False)

print(f"File sudah tersimpan di {eksport_file}")


 