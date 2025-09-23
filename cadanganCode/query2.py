# %%
import pandas as pd
import json
from pyserini.search.lucene import LuceneSearcher
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords

# -----------------------
# PREPROCESSING
# -----------------------
stop_words = set(stopwords.words('indonesian'))

factory = StemmerFactory()
stemmer = factory.create_stemmer()

def stem_tokens(tokens):
    return [stemmer.stem(token) for token in tokens]

def preprocess_query(text):
    # lowercase
    text = text.lower()
    # tokenisasi + hapus stopwords
    tokens = [word for word in text.split() if word not in stop_words]
    # stemming
    tokens = stem_tokens(tokens)
    return " ".join(tokens)

# -----------------------
# DISPLAY FUNCTION
# -----------------------
def display_results(query, hits, df):
    print(f"\nQuery: {query}")

    if not hits:
        print("Tidak ada dokumen yang sesuai.")
        return pd.DataFrame()

    results_with_scores = []
    for i, hit in enumerate(hits, start=1):
        # Parse JSON asli dari dokumen (karena pakai --storeRaw)
        try:
            raw = json.loads(hit.raw)
            docid = str(raw.get("id", hit.docid))  # fallback ke docid internal
        except Exception:
            docid = hit.docid

        # Cari di DataFrame
        matching_row = df[df["id"].astype(str) == docid].copy()

        if not matching_row.empty:
            matching_row["score"] = hit.score
            matching_row["rank"] = i
            matching_row["query"] = query
            results_with_scores.append(matching_row)

            # Print ringkas
            print(f"{i}. {matching_row.iloc[0]['title']} (Score: {hit.score:.4f})")
        else:
            print(f"{i}. [ID {docid}] tidak ditemukan di DataFrame (Score: {hit.score:.4f})")

    if results_with_scores:
        return pd.concat(results_with_scores, ignore_index=True)
    else:
        print("No matching documents found in DataFrame.")
        return pd.DataFrame()


# -----------------------
# MAIN SCRIPT
# -----------------------
# Load DataFrame (pastikan df punya kolom 'id', 'title', 'link', 'date')
df = pd.read_json("../json-file/docs.jsonl", lines=True)

# Gunakan index hasil pyserini.index
searcher = LuceneSearcher("../my_index")

# Daftar query
queries = [
    "gemini ai",
    "laptop gaming wajib dibeli",
    "cara agar tidak di hack",
    "teknologi canggih sekarang",
    "komputer terbaik",
    "mobile legend"
]

all_results = []

# Jalankan semua query dengan preprocessing
for q in queries:
    processed_q = preprocess_query(q)   # <<< preprocessing dulu
    hits = searcher.search(processed_q, k=10)
    result_df = display_results(q, hits, df)  # tetap tampilkan query asli
    if not result_df.empty:
        all_results.append(result_df)

# Gabungkan semua hasil
if all_results:
    combined = pd.concat(all_results, ignore_index=True)

    # Pilih hanya kolom sesuai permintaan + query
    output_df = combined[["id", "title", "date", "score", "rank", "query"]]

    print("\n=== Semua Hasil Gabungan ===")
    print(output_df.to_string(index=False))  # tampilkan semua, bukan head saja

    # Opsional: simpan ke Excel
    #output_df.to_excel("search_results.xlsx", engine="openpyxl")
    #print("\nSemua hasil pencarian disimpan ke search_results.xlsx")
else:
    print("Tidak ada hasil yang ditemukan untuk semua query.")
# %%
