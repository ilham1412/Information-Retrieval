# %%
from pyserini.index.lucene import LuceneIndexReader

# Buka index yang sudah dibuat
index_dir = "my_index"
reader = LuceneIndexReader(index_dir)

# Ambil daftar seluruh term unik (vocabulary)
unique_terms = reader.terms()

# Hitung jumlah total term unik
term_count = len(list(unique_terms))

print(f"Jumlah term unik dalam indeks: {term_count:,}")
# %%
