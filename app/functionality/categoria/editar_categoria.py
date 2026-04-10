import streamlit as st

from app.database import load_categories, update_category


def render_editar_categoria():
    categorias = load_categories()

    if not categorias:
        st.info("Nenhuma categoria cadastrada.")
        return

    nomes = [c[0] for c in categorias]
    cat_sel = st.selectbox("Categoria", nomes)

    # pegar tipo atual
    tipo_atual = [c[1] for c in categorias if c[0] == cat_sel][0]

    novo_nome = st.text_input("Novo nome da categoria", value=cat_sel)
    novo_tipo = st.selectbox(
        "Novo tipo", ["Receita", "Despesa"], index=0 if tipo_atual == "Receita" else 1
    )

    if st.button("Salvar edição"):
        update_category(cat_sel, novo_nome.strip(), novo_tipo)
        st.success("Categoria atualizada!")
        st.rerun()
