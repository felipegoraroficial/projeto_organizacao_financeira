import streamlit as st

from .adicionar_lancamento import render_adicionar_lancamento
from .ajustar_saldo_inicial import render_ajustar_saldo_inicial
from .listar_lancamentos import render_listar_lancamentos


def render_lancamentos():
    st.header("Lançamentos")

    st.subheader("Ajustar saldo inicial do mês")
    render_ajustar_saldo_inicial()

    st.header("Adicionar novo lançamento")
    render_adicionar_lancamento()

    st.subheader("📄 Excluir / Atualizar lançamentos")
    render_listar_lancamentos()
