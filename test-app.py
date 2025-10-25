import streamlit as st
import json
import pandas as pd
from pyserini.search.lucene import LuceneSearcher
import math

# --- KONFIGURASI ---
INDEX_DIR = "my_index"
ORIGINAL_DATA_PATH = "artikel-cleaning-final/data_gabungan_normalized.xlsx"
RESULTS_PER_PAGE = 10  # jumlah hasil per halaman

# --- CUSTOM CSS UNTUK TAMPILAN ---
st.markdown("""
    <style>
    body {
        background-color: #f8fafc;
        color: #1e293b;
    }
    .main-title {
        text-align: center;
        color: #1e3a8a;
        font-weight: 700;
        margin-top: -20px;
        margin-bottom: 30px;
    }
    .search-box {
        background-color: #f1f5f9;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    .result-card {
        background-color: white;
        padding: 20px 25px;
        border-radius: 15px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        border-left: 5px solid #3b82f6;
        transition: all 0.3s ease;
    }
    .result-card:hover {
        transform: scale(1.01);
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }
    .result-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1d4ed8;
        margin-bottom: 6px;
    }
    .result-meta {
        font-size: 0.9rem;
        color: #64748b;
        margin-bottom: 10px;
    }
    .result-content {
        font-size: 0.95rem;
        color: #334155;
        margin-bottom: 10px;
        text-align: justify;
    }
    .see-more {
        font-size: 0.9rem;
        color: #2563eb;
        text-decoration: none;
    }
    .pagination {
        display: flex;
        justify-content: center;
        gap: 8px;
        margin-top: 25px;
    }
    .page-button {
        background-color: #e0f2fe;
        color: #1e3a8a;
        border: none;
        padding: 6px 12px;
        border-radius: 8px;
        cursor: pointer;
        transition: 0.2s;
    }
    .page-button:hover {
        background-color: #93c5fd;
        color: white;
    }
    .page-button-active {
        background-color: #1d4ed8;
        color: white;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_original_data(filepath):
    try:
        df = pd.read_excel(filepath)
        return df
    except FileNotFoundError:
        st.error(f"File tidak ditemukan di path: {filepath}")
        return None

try:
    searcher = LuceneSearcher(INDEX_DIR)
    df_original = load_original_data(ORIGINAL_DATA_PATH)
except Exception as e:
    st.error(f"Gagal memuat Pyserini Index dari direktori '{INDEX_DIR}'. Pastikan path sudah benar. Error: {e}")
    st.stop()

# --- HEADER ---
st.markdown("<h1 class='main-title'>🔍 Search Engine GG Banget</h1>", unsafe_allow_html=True)

# --- INPUT QUERY ---
with st.container():
    st.markdown("<div class='search-box'>", unsafe_allow_html=True)
    query = st.text_input("Masukkan kata kunci:", placeholder="Contoh: vaksin covid, kesehatan mental, nutrisi anak...")
    st.markdown("</div>", unsafe_allow_html=True)

# --- HASIL PENCARIAN ---
if query and df_original is not None:
    # ambil banyak hasil (misalnya 100)
    hits = searcher.search(query, k=100)
    total_results = len(hits)
    
    if total_results == 0:
        st.info("Tidak ada hasil ditemukan.")
    else:
        total_pages = math.ceil(total_results / RESULTS_PER_PAGE)

        # Gunakan session_state untuk simpan halaman saat ini
        if "current_page" not in st.session_state:
            st.session_state.current_page = 1

        # Navigasi halaman
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.subheader(f"Hasil pencarian untuk: **'{query}'**")
            st.caption(f"Menampilkan {RESULTS_PER_PAGE} dari total {total_results} dokumen")

        # Tentukan range hasil
        start_idx = (st.session_state.current_page - 1) * RESULTS_PER_PAGE
        end_idx = start_idx + RESULTS_PER_PAGE
        page_hits = hits[start_idx:end_idx]

        # --- Tampilkan hasil sesuai halaman ---
        for i, h in enumerate(page_hits, start=start_idx + 1):
            try:
                doc_index = int(h.docid.replace('doc', ''))
                adjusted_index = doc_index - 1

                if adjusted_index < 0:
                    raise IndexError("Indeks tidak valid (negatif).")

                original_row = df_original.iloc[adjusted_index]
                original_title = original_row.get("title", "Tanpa Judul")
                original_content = original_row.get("content", "")

                raw_doc_from_index = searcher.doc(h.docid).raw()
                doc_from_index = json.loads(raw_doc_from_index)

                link = doc_from_index.get("link", "#")
                date = doc_from_index.get("date", "Tanggal tidak ada")

                # --- CARD HASIL ---
                st.markdown(f"""
                    <div class="result-card">
                        <div class="result-title">{i}. <a href="{link}" target="_blank">{original_title}</a></div>
                        <div class="result-meta">🗓️ {date}</div>
                        <div class="result-content">{" ".join(str(original_content).split()[:35])}...</div>
                        <a class="see-more" href="{link}" target="_blank">Lihat Selengkapnya →</a>
                    </div>
                """, unsafe_allow_html=True)

                with st.expander(f"🔎 Detail Dokumen {i}"):
                    st.write(f"**Judul:** {original_title}")
                    st.write(f"**Konten:** {original_content[:300]}...")
                    st.json(doc_from_index)

            except Exception as e:
                st.warning(f"❌ Gagal menampilkan dokumen {i}: {e}")

        # --- PAGINATION CONTROL ---
        st.markdown("<div class='pagination'>", unsafe_allow_html=True)
        cols = st.columns(total_pages if total_pages <= 5 else 7)

        # Tombol sebelumnya
        if st.session_state.current_page > 1:
            if cols[0].button("⬅️ Sebelumnya"):
                st.session_state.current_page -= 1
                st.rerun()

        # Tombol nomor halaman
        visible_pages = range(max(1, st.session_state.current_page - 2),
                              min(total_pages, st.session_state.current_page + 2) + 1)
        for page in visible_pages:
            if cols[page - visible_pages.start + 1].button(str(page),
                                                           key=f"page_{page}",
                                                           help=f"Halaman {page}"):
                st.session_state.current_page = page
                st.rerun()

        # Tombol berikutnya
        if st.session_state.current_page < total_pages:
            if cols[-1].button("Berikutnya ➡️"):
                st.session_state.current_page += 1
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
