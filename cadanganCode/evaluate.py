#%%
import json
from pyserini.search.lucene import LuceneSearcher
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
import nltk

# Pastikan stopwords NLTK sudah diunduh
try:
    stopwords.words('indonesian')
except LookupError:
    print("Mengunduh stopwords untuk Bahasa Indonesia...")
    nltk.download('stopwords')
    print("Selesai.")


# Path index & data
INDEX_DIR = "my_index"
JSON_FILE = "json-file/docs.jsonl"  # ganti sesuai nama file

# Load searcher
searcher = LuceneSearcher(INDEX_DIR)

# ------------------------------------------------
# <--- TAMBAHAN: Blok kode untuk Preprocessing Query
# ------------------------------------------------
stop_words = set(stopwords.words('indonesian'))
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def stem_tokens(tokens):
    """Fungsi untuk melakukan stemming pada list token."""
    return [stemmer.stem(token) for token in tokens]

def preprocess_text(text):
    """Fungsi lengkap untuk preprocessing: lowercase, tokenisasi, stopword removal, stemming."""
    # 1. Lowercase
    text = text.lower()
    # 2. Tokenisasi + Hapus Stopwords
    tokens = [word for word in text.split() if word not in stop_words]
    # 3. Stemming
    stemmed_tokens = stem_tokens(tokens)
    return " ".join(stemmed_tokens)

# ------------------------------------------------
# Fungsi baca dokumen (support JSON array / NDJSON)
# ------------------------------------------------
def load_docs(path):
    docs = []
    with open(path, "r", encoding="utf-8") as f:
        first_char = f.read(1)
        f.seek(0)
        if first_char == "[":  # format array JSON
            docs = json.load(f)
        else:  # format NDJSON
            for line in f:
                if line.strip():
                    try:
                        docs.append(json.loads(line))
                    except Exception as e:
                        print(f"⚠️ Gagal parse baris: {line[:50]}... ({e})")
    return docs

# ------------------------------------------------
# Ground truth otomatis (pakai title + content)
# ------------------------------------------------
TECH_QUERIES = [
    "gemini ai",
    "laptop gaming",
    "hack",
    "teknologi",
    "komputer",
    "mobile legends"
]

# <--- MODIFIKASI: build_ground_truth disesuaikan dengan preprocessing
# Ganti fungsi build_ground_truth Anda dengan yang ini

# GANTI FUNGSI LAMA ANDA DENGAN YANG INI
# ==========================================

def build_ground_truth():
    """
    Membangun ground truth dengan metode hibrida:
    Mengecek jika SEMUA kata dari query ada di dalam dokumen (case-insensitive),
    tanpa memperdulikan urutan dan tanpa stemming.
    """
    docs = load_docs(JSON_FILE)
    ground_truth = {}

    print("--- Membangun Ground Truth (Metode Hibrida 'Semua Kata') ---")
    for query in TECH_QUERIES:
        relevant_docs = []
        
        # 1. Ubah query menjadi daftar kata-kata kunci (lowercased)
        query_words = query.lower().split()

        for doc in docs:
            doc_id = str(doc.get("id"))
            doc_text = (doc.get("title", "") + " " + doc.get("content", "")).lower()

            # 2. LOGIKA UTAMA: Cek jika SEMUA kata kunci dari query ada di dalam teks dokumen
            # all() akan mengembalikan True hanya jika semua kondisi di dalamnya True
            if all(word in doc_text for word in query_words):
                relevant_docs.append(doc_id)
        
        if relevant_docs:
            ground_truth[query] = relevant_docs
            print(f"Query '{query}' menemukan {len(relevant_docs)} dokumen relevan.")
        else:
            print(f"Query '{query}' tidak menemukan dokumen relevan.")
            
    print("-" * 30)
    return ground_truth, docs


# ------------------------------------------------
# Evaluasi IR (precision, recall, F1)
# ------------------------------------------------
def evaluate_ir(k=10):
    ground_truth, documents = build_ground_truth()
    all_precisions, all_recalls, all_f1s = [], [], []

    print("=== Hasil Evaluasi IR ===")

    for query, relevant_docs in ground_truth.items():
        # <--- MODIFIKASI: Query di-preprocess sebelum melakukan search
        processed_query = preprocess_text(query)
        hits = searcher.search(processed_query, k=k)
        retrieved = [h.docid for h in hits]

        retrieved_relevant = [d for d in retrieved if d in relevant_docs]

        precision = len(retrieved_relevant) / len(retrieved) if retrieved else 0
        recall = len(retrieved_relevant) / len(relevant_docs) if relevant_docs else 0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0

        all_precisions.append(precision)
        all_recalls.append(recall)
        all_f1s.append(f1)

        print(f"\nQuery Asli    : {query}")
        print(f"Query Proses  : {processed_query}")
        print(f"Retrieved ({len(retrieved)}): {retrieved}")
        print(f"Relevant ({len(relevant_docs)}) : {relevant_docs}")
        print(f"Precision: {precision:.2f}, Recall: {recall:.2f}, F1: {f1:.2f}")

    print("\n=== Rata-rata Evaluasi ===")
    if all_precisions:
        print(f"Precision : {sum(all_precisions)/len(all_precisions):.2f}")
        print(f"Recall    : {sum(all_recalls)/len(all_recalls):.2f}")
        print(f"F1-score  : {sum(all_f1s)/len(all_f1s):.2f}")
    else:
        print("Tidak ada hasil evaluasi (cek ground truth atau query).")


if __name__ == "__main__":
    evaluate_ir(k=10)
# %%
