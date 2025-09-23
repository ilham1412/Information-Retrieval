# %%
import pandas as pd
import openpyxl

# ganti dengan path file CSV kamu
file_path = "kompas_tekno_terbaru.csv"
df = pd.read_csv(file_path)
df.head()
len(df)
# %%


# Misal, kolom 'judul' mengandung kata 'video' → hapus baris tsb
#df = df[~df['title'].str.contains("video", case=False, na=False)]

# Bisa juga filter berdasarkan URL, misalnya ada '/video/' di link
#df = df[~df['link'].str.contains("/video/", case=False, na=False)]

# Simpan hasil yang sudah difilter
df.to_excel("artikel-cleaning-final/kompas_scraping_bersih_terbaru.xlsx", index=False)

print("Selesai, data sudah difilter dan disimpan ke hasil_scraping_bersih.xlsx")

# %%
