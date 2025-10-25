import streamlit as st
import json
from pyserini.search.lucene import LuceneSearcher

INDEX_DIR = "my_index"

searcher = LuceneSearcher(INDEX_DIR)

st.title("Search Engine gg banget")

query = st.text_input("Masukkan kata kunci:")

if query:
    hits = searcher.search(query, k=10)  #

    st.subheader(f"Hasil pencarian untuk: '{query}'")

    if not hits:
        st.write("Tidak ada hasil ditemukan.")
    else:
        for i, h in enumerate(hits):
            raw_doc = searcher.doc(h.docid).raw()
            if raw_doc:
                doc = json.loads(raw_doc)

                title = doc.get("title", "Tanpa Judul")
                link = doc.get("link", "#")
                content = doc.get("content", "")
                date = doc.get("date", "Tanggal tidak ada")

                st.markdown(f"### {i+1}. [{title}]({link})")
                st.caption(date)
                st.write(" ".join(content.split()[:30]) + "...")

                # tombol debug untuk cek isi raw
                with st.expander(f"metadata dokumen {i+1}"):
                    st.json(doc)

            else:
                st.write(f"{i+1}. (Dokumen tidak memiliki raw field)")

                