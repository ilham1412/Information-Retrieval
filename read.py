# %%
#cek data saja
import pandas as pd
import openpyxl

# ganti dengan path file CSV kamu
file_path = "kompas_tekno_terbaru.csv"
df = pd.read_csv(file_path)
df.head()
len(df)
# %%
#mengubah dari csv ke xlsx.

#untuk web kompas yang sulit banyak iklan video
# Misal, kolom 'judul' mengandung kata 'video' → hapus baris tsb
#df = df[~df['title'].str.contains("video", case=False, na=False)]

# Bisa juga filter berdasarkan URL, misalnya ada '/video/' di link
#df = df[~df['link'].str.contains("/video/", case=False, na=False)]

# Simpan hasil yang sudah difilter
df.to_excel("artikel-cleaning-final/kompas_scraping_bersih_terbaru.xlsx", index=False)

print("Selesai, data sudah difilter dan disimpan ke hasil_scraping_bersih.xlsx")

# %%
#mengubah format tanggal menjadi sama
import pandas as pd
from datetime import datetime

# mapping hari ke bahasa Indonesia
hari_mapping = {
    "Monday": "Senin",
    "Tuesday": "Selasa",
    "Wednesday": "Rabu",
    "Thursday": "Kamis",
    "Friday": "Jumat",
    "Saturday": "Sabtu",
    "Sunday": "Minggu"
}

# mapping bulan ke bahasa Indonesia
bulan_mapping = {
    "Jan": "Januari",
    "Feb": "Februari",
    "Mar": "Maret",
    "Apr": "April",
    "May": "Mei",
    "Jun": "Juni",
    "Jul": "Juli",
    "Aug": "Agustus",
    "Sep": "September",
    "Oct": "Oktober",
    "Nov": "November",
    "Dec": "Desember"
}

def normalize_date(date_str):
    if pd.isna(date_str):  # jika kosong
        return None
    date_str = str(date_str).strip()

    # coba format 1: dd/mm/yyyy
    try:
        dt = datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        try:
            # coba format 2: Hari, 17 Sep 2025 06:45 WIB
            dt = datetime.strptime(date_str, "%A, %d %b %Y %H:%M WIB")
        except ValueError:
            return date_str  # kalau tetap error, kembalikan aslinya

    # konversi hari & bulan
    hari = hari_mapping[dt.strftime("%A")]
    bulan = bulan_mapping[dt.strftime("%b")]

    return f"{hari}, {dt.day} {bulan} {dt.year}"

# === BACA FILE EXCEL ===
df = pd.read_excel("artikel-cleaning-final/data_gabungan.xlsx")  # ganti dengan nama file excel kamu

# asumsikan nama kolom lama adalah "date"
df["date"] = df["date"].apply(normalize_date)

# simpan ke file baru
df.to_excel("artikel-cleaning-final/data_gabungan_normalized.xlsx", index=False)

print("✅ Normalisasi selesai! Kolom 'date' sudah diperbarui dan disimpan ke data_normalized.xlsx")


# %%
