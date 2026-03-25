import streamlit as st
from app.database_functions import (
    load_categories,
    insert_category,
    update_category,
    delete_category
)

def render_categorias():
    st.header("Gerenciar Categorias")

    categorias = load_categories()

    # Adicionar categoria
    st.subheader("Adicionar nova categoria")
    nova_cat = st.text_input("Nome da nova categoria")
    if st.button("Adicionar categoria"):
        if nova_cat.strip():
            insert_category(nova_cat.strip())
            st.success("Categoria adicionada!")
            st.rerun()

    # Editar categoria
    st.subheader("Editar categoria existente")
    cat_editar = st.selectbox("Categoria", categorias)
    novo_nome = st.text_input("Novo nome da categoria")
    if st.button("Salvar edição"):
        if novo_nome.strip():
            update_category(cat_editar, novo_nome.strip())
            st.success("Categoria atualizada!")
            st.rerun()

    # Excluir categoria
    st.subheader("Excluir categoria")
    cat_excluir = st.selectbox("Categoria para excluir", categorias, key="excluir_cat")
    if st.button("Excluir categoria"):
        delete_category(cat_excluir)
        st.warning("Categoria excluída!")
        st.rerun()