import pandas as pd
import streamlit as st

from app.dashboard.utils import (
    calcular_saldo_anterior,
    filtrar_por_periodo,
    preparar_grafico_despesas,
    preparar_grafico_evolucao,
    preparar_grafico_receitas,
)
from app.database import load_transactions


def render_dashboard():
    st.header("📊 Visão Geral")

    data = load_transactions()
    df = pd.DataFrame(
        data,
        columns=[
            "ID",
            "Data",
            "Tipo",
            "Categoria",
            "Descrição",
            "Valor",
            "Status",
            "Recorrente",
            "Parcelas",
            "DataPagamento",
        ],
    )

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
    # GRÁFICO DE RECEITA
    # -----------------------------
    preparar_grafico_receitas(df_mes)

    # -----------------------------
    # GRÁFICO DE DESPESA
    # -----------------------------
    preparar_grafico_despesas(df_mes)

    # -----------------------------
    # EVOLUÇÃO AO LONGO DO TEMPO
    # -----------------------------
    preparar_grafico_evolucao(df_mes)
