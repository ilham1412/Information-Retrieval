import json
from pyserini.search.lucene import LuceneSearcher

# Path index & data
INDEX_DIR = "my_index"
JSON_FILE = "json-file/docs.jsonl"  # ganti sesuai nama file

# Load searcher
searcher = LuceneSearcher(INDEX_DIR)

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
# Bangun ground truth (judul dipakai sebagai "query")
# ------------------------------------------------
# 🔹 Daftar query yang kita anggap penting (domain teknologi)
TECH_QUERIES = [
    "transformasi digital"
]

def build_ground_truth():
    docs = load_docs(JSON_FILE)
    ground_truth = {}

    for query in TECH_QUERIES:
        relevant_docs = []
        for i, doc in enumerate(docs):
            title = doc.get("title", "").lower()
            if query in title:
                relevant_docs.append(str(i))
        if relevant_docs:  # hanya simpan kalau ada dokumen relevan
            ground_truth[query] = relevant_docs

    return ground_truth, docs


# ------------------------------------------------
# Evaluasi IR (precision, recall, F1)
# ------------------------------------------------
def evaluate_ir(k=10):
    ground_truth, documents = build_ground_truth()
    all_precisions, all_recalls, all_f1s = [], [], []

    print("=== Hasil Evaluasi IR ===")

    for query, relevant_docs in ground_truth.items():
        hits = searcher.search(query, k=k)
        retrieved = [h.docid for h in hits]

        # hitung metrik
        if not relevant_docs:
            continue

        retrieved_relevant = [d for d in retrieved if d in relevant_docs]

        precision = len(retrieved_relevant) / len(retrieved) if retrieved else 0
        recall = len(retrieved_relevant) / len(relevant_docs) if relevant_docs else 0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0

        all_precisions.append(precision)
        all_recalls.append(recall)
        all_f1s.append(f1)

        # Debug tiap query
        print(f"\nquery: {query}")
        print(f"Retrieved: {retrieved}")
        print(f"Relevant : {relevant_docs}")
        print(f"Precision: {precision:.2f}, Recall: {recall:.2f}, F1: {f1:.2f}")

    # Rata-rata
    print("\nRata-rata Evaluasi")
    if all_precisions:
        print(f"Precision : {sum(all_precisions)/len(all_precisions):.2f}")
        print(f"Recall    : {sum(all_recalls)/len(all_recalls):.2f}")
        print(f"F1-score  : {sum(all_f1s)/len(all_f1s):.2f}")
    else:
        print("⚠️ Tidak ada hasil evaluasi (cek ground truth atau query).")

# ------------------------------------------------
if __name__ == "__main__":
    evaluate_ir(k=10)
