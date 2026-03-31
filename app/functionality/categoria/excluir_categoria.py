import streamlit as st
from app.database import load_categories, delete_category

def render_excluir_categoria():
    categorias = load_categories()

    if not categorias:
        st.info("Nenhuma categoria cadastrada.")
        return

    # Extrair apenas os nomes
    nomes = [c[0] for c in categorias]

    cat_excluir = st.selectbox("Categoria para excluir", nomes, key="excluir_cat")

    if st.button("Excluir categoria"):
        delete_category(cat_excluir)
        st.warning("Categoria excluída!")
        st.rerun()