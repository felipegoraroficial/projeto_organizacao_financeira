import streamlit as st

from .adicionar_categoria import render_adicionar_categoria
from .editar_categoria import render_editar_categoria
from .excluir_categoria import render_excluir_categoria


def render_categorias():
    st.header("Gerenciar Categorias")

    st.subheader("Adicionar nova categoria")
    render_adicionar_categoria()

    st.subheader("Editar categoria existente")
    render_editar_categoria()

    st.subheader("Excluir categoria")
    render_excluir_categoria()
