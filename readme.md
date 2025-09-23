# 📘 Information Retrieval Project

Proyek ini adalah implementasi **Information Retrieval (IR)** menggunakan **Pyserini** untuk melakukan pencarian dokumen dari dataset artikel (berformat JSON).
Pengguna bisa melakukan pencarian query dan mendapatkan hasil peringkat dokumen sesuai relevansi.

---

## 📂 Struktur Folder

```
.
├── artikel-cleaning-final/   # folder untuk data artikel sebelum indexing
├── json-file/                # dataset artikel dalam format JSON
├── my_index/                 # hasil index pyserini
├── venv/                     # virtual environment 
├── app.py                    # script utama aplikasi pencarian
├── eksekusi.py               # script eksekusi indexing / pencarian batch
├── read.py                   # script tambahan
├── requirements.txt          # daftar dependencies
├── chromedriver.exe          # driver selenium (optional, diabaikan di GitHub)
└── .gitignore
```

---

## ⚙️ Instalasi

1. **Clone repository**

   ```bash
   git clone https://github.com/username/nama-repo.git
   cd nama-repo
   ```

2. **Buat virtual environment**

   ```bash
   python -m venv venv
   ```

3. **Aktifkan virtual environment**

   * Windows (Command Prompt):

     ```bash
     venvilham\Scripts\activate
     ```
   * Windows (PowerShell):

     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   * Linux/Mac:

     ```bash
     source venv/bin/activate
     ```

4. **Install requirements**

   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Menjalankan Program

1. **Indexing dataset**
   Pastikan folder `json-file/` berisi file JSON artikel dengan format kolom:

   ```json
   {
     "title": "Judul Artikel",
     "tag": "tag1, tag2",
     "link": "https://contoh.com/artikel",
     "date": "2023-09-23",
     "content": "Isi artikel ..."
   }
   ```

   Lalu jalankan:

   ```bash
   python eksekusi.py
   ```

2. **Menjalankan aplikasi pencarian**

   ```bash
   streamlit run app.py
   ```

   Setelah itu, masukkan query untuk melakukan pencarian dokumen.

---

## 🛠️ Troubleshooting (PATH Error Pyserini)

Jika muncul error seperti saat indexing **“ModuleNotFoundError: No module named pyserini”** walaupun sudah `pip install pyserini`, kemungkinan penyebabnya:

* Virtual environment tidak aktif.
* Python PATH salah saat menjalankan `subprocess`.

✅ Solusi:

1. Pastikan sudah aktifkan venv sebelum menjalankan program:

   ```bash
   venvilham\Scripts\activate
   ```
2. Gunakan python dari venv saat eksekusi subprocess:

   ```python
   import sys, subprocess
   subprocess.run([sys.executable, "script.py"])
   ```

Dengan begitu, script akan selalu memakai Python dari virtual environment.

---

## 📊 Evaluasi (Precision, Recall, F1)

Proyek ini juga menyediakan evaluasi IR menggunakan **precision, recall, dan F1-score**.

* Relevansi ditentukan berdasarkan pencocokan dokumen hasil pencarian dengan ground truth (label relevan).
* Script evaluasi akan menghitung:

  * **Precision** → seberapa relevan hasil pencarian.
  * **Recall** → seberapa banyak dokumen relevan berhasil ditemukan.
  * **F1-score** → harmonic mean dari precision & recall.

Contoh penggunaan:

```bash
python evaluate.py
```

---

## 📌 Catatan
  ```
* `chromedriver.exe` download sesuai chrome version, karena bisa berbeda untuk tiap device.

---

