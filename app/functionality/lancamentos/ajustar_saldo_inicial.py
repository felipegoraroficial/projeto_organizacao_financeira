import streamlit as st
from datetime import datetime
from app.database import set_saldo_inicial


def render_ajustar_saldo_inicial():
    colA, colB, colC = st.columns(3)

    ano_saldo = colA.number_input(
        "Ano",
        min_value=2000,
        max_value=2100,
        value=datetime.now().year,
    )
    mes_saldo = colB.number_input(
        "Mês",
        min_value=1,
        max_value=12,
        value=datetime.now().month,
    )
    valor_saldo = colC.number_input("Saldo inicial", format="%.2f")

    if st.button("Salvar saldo inicial"):
        set_saldo_inicial(ano_saldo, mes_saldo, valor_saldo)
        st.success("Saldo inicial atualizado!")
        st.rerun()