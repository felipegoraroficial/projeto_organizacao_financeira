import streamlit as st
import pandas as pd
from datetime import datetime


from app.database_functions import (
    load_transactions,
    set_saldo_inicial
)

from .dashboard_utils import (
    filtrar_por_periodo,
    calcular_saldo_anterior,
    preparar_grafico_categorias,
    preparar_grafico_evolucao
)


def render_dashboard():
    st.header("📊 Visão Geral")

    data = load_transactions()
    df = pd.DataFrame(data, columns=[
        "ID", "Data", "Tipo", "Categoria", "Descrição", "Valor",
        "Status", "Recorrente", "Parcelas"
    ])

    if df.empty:
        st.info("Nenhum dado cadastrado ainda.")
        return

    df["Data"] = pd.to_datetime(df["Data"])

    # -----------------------------
    # FILTROS LATERAIS
    # -----------------------------
    st.sidebar.header("Filtros de Visualização")

    anos = sorted(df["Data"].dt.year.unique())
    ano_sel = st.sidebar.selectbox("Ano", ["Todos"] + [str(a) for a in anos])

    meses = sorted(df["Data"].dt.month.unique())
    mes_sel = st.sidebar.selectbox("Mês", ["Todos"] + [f"{m:02d}" for m in meses])

    df_mes = filtrar_por_periodo(df, ano_sel, mes_sel)

    # -----------------------------
    # SALDO ANTERIOR
    # -----------------------------
    saldo_anterior = calcular_saldo_anterior(df, ano_sel, mes_sel)

    # -----------------------------
    # AJUSTE MANUAL DO SALDO
    # -----------------------------
    st.markdown("### Ajustar saldo inicial do mês")

    colA, colB, colC = st.columns(3)

    ano_saldo = colA.number_input(
        "Ano",
        min_value=2000,
        max_value=2100,
        value=int(ano_sel) if ano_sel != "Todos" else datetime.now().year,
    )
    mes_saldo = colB.number_input(
        "Mês",
        min_value=1,
        max_value=12,
        value=int(mes_sel) if mes_sel != "Todos" else datetime.now().month,
    )
    valor_saldo = colC.number_input("Saldo inicial", format="%.2f")

    if st.button("Salvar saldo inicial"):
        set_saldo_inicial(ano_saldo, mes_saldo, valor_saldo)
        st.success("Saldo inicial atualizado!")
        st.rerun()

    # -----------------------------
    # MÉTRICAS
    # -----------------------------
    col1, col2, col3, col4 = st.columns(4)

    total_receitas = df_mes[df_mes["Tipo"] == "Receita"]["Valor"].sum()
    total_despesas = df_mes[df_mes["Tipo"] == "Despesa"]["Valor"].sum()
    saldo = total_receitas - total_despesas
    saldo_acumulado = saldo_anterior + saldo

    col1.metric("Saldo Inicial (período anterior)", f"R$ {saldo_anterior:,.2f}")
    col2.metric("Receitas", f"R$ {total_receitas:,.2f}")
    col3.metric("Despesas", f"R$ {total_despesas:,.2f}")
    col4.metric("Saldo Acumulado", f"R$ {saldo_acumulado:,.2f}")

    # -----------------------------
    # GRÁFICO DE CATEGORIAS
    # -----------------------------
    preparar_grafico_categorias(df_mes)

    # -----------------------------
    # EVOLUÇÃO AO LONGO DO TEMPO
    # -----------------------------
    preparar_grafico_evolucao(df_mes)