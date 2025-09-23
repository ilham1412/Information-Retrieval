#%%
import pandas as pd
import re
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import nltk
from nltk.corpus import stopwords

# Download stopwords NLTK (sekali saja)
nltk.download('stopwords')

# Buat stopwords bahasa Indonesia
stop_words = set(stopwords.words('indonesian'))

# Buat stemmer Sastrawi
factory = StemmerFactory()
stemmer = factory.create_stemmer()

#%%
# 1. Baca file Excel hasil scraping
df = pd.read_excel("artikel-cleaning-final/data_gabungan.xlsx")   # ganti nama file sesuai hasil scraping

# 2. Hapus duplikat (berdasarkan judul)
df = df.drop_duplicates(subset="title")

# 3. Hapus baris yang tidak ada content-nya
df = df.dropna(subset=["content"])

# 4. Hapus kolom tag (karena kosong)
if "tag" in df.columns:
    df = df.drop(columns=["tag"])

# 5.hapus kolom description(karena kosong)
if "description" in df.columns:
    df = df.drop(columns=["description"])

#%%
import json
# 5. Preprocessing teks
def clean_text(text):
    # Case folding
    text = text.lower()

    # Hapus URL/link
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)

    # Hapus tanda baca
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Hapus karakter non-ascii (noise)
    text = re.sub(r"[^\x00-\x7f]", " ", text)

    return text

def remove_stopwords(text):
    tokens = text.split()
    filtered = [word for word in tokens if word not in stop_words]
    return " ".join(filtered)

def stemming(text):
    return stemmer.stem(text)


# Terapkan ke kolom title, description, dan content
for col in ["title", "content"]:
    df[col] = df[col].astype(str)  # pastikan string
    df[col] = df[col].apply(clean_text)
    df[col] = df[col].apply(remove_stopwords)
    df[col] = df[col].apply(stemming)

with open("json-file/docs.jsonl", "w", encoding="utf-8") as f:
    for i, row in df.iterrows():
        doc = {
            "id": str(i+1),  # bikin id unik (1,2,3,...)
            "contents": f"{row['title']} {row['content']}",  # isi utama yang diindex
            "title": row["title"],       # info tambahan
            "link": row["link"],         # info tambahan
            "date": str(row["date"])     # info tambahan
        }
        f.write(json.dumps(doc, ensure_ascii=False) + "\n")

#batas

#%%

import sys
import subprocess

cmd = [
    sys.executable, "-m", "pyserini.index",
    "--collection", "JsonCollection",
    "--input", "json-file",
    "--index", "my_index",
    "--generator", "DefaultLuceneDocumentGenerator",
    "--threads", "1",
    "--storePositions",
    "--storeDocvectors",
    "--storeRaw"
]

result = subprocess.run(cmd, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)


# %%
