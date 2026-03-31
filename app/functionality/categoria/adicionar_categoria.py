import streamlit as st
from app.database import insert_category

def render_adicionar_categoria():
    nova_cat = st.text_input("Nome da nova categoria")
    tipo = st.selectbox("Tipo da categoria", ["Receita", "Despesa"])

    if st.button("Adicionar categoria"):
        if nova_cat.strip():
            insert_category(nova_cat.strip(), tipo)
            st.success("Categoria adicionada!")
            st.rerun()