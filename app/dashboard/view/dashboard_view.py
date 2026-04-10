import pandas as pd
import streamlit as st

from app.dashboard.utils import (
    calcular_saldo_anterior,
    calcular_saldos,
    exportar_excel,
    filtrar_por_periodo,
    preparar_grafico_despesas,
    preparar_grafico_evolucao,
    preparar_grafico_receitas,
)
from app.database import load_transactions


def render_dashboard():

    # 🔐 Verificação de login
    if "usuario" not in st.session_state:
        st.switch_page("app/auth/login_view.py")

    # 🔄 Botão de refresh (agora no lugar certo)
    if st.button("🔄 Atualizar Dashboard"):
        st.rerun()

    st.header("📊 Visão Geral")

    usuario_id = st.session_state["usuario"]["id"]
    data = load_transactions(usuario_id)

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
    # CÓPIA PARA CÁLCULOS (NÃO AFETA GRÁFICOS)
    # -----------------------------
    df_calc = df_mes.copy()
    df_calc["Tipo"] = df_calc["Tipo"].str.lower()
    df_calc["Status"] = df_calc["Status"].str.lower()

    resultados = calcular_saldos(df_calc, saldo_anterior)

    # -----------------------------
    # MÉTRICAS ORGANIZADAS E ALINHADAS
    # -----------------------------

    st.subheader("Visão Geral")

    with st.container():
        col1, col2, col3 = st.columns([1, 1, 1])
        col1.metric("Saldo Inicial", f"R$ {saldo_anterior:,.2f}")
        col2.metric("Saldo Final (realizado)", f"R$ {resultados['saldo_final']:,.2f}")
        col3.metric(
            "Saldo Previsto (projetado)", f"R$ {resultados['saldo_previsto']:,.2f}"
        )

    st.markdown("---")

    # -----------------------------
    # GRÁFICO DE RECEITA
    # -----------------------------

    st.subheader("Receitas")

    with st.container():
        col4, col5 = st.columns([1, 1])
        col4.metric("Receitas Pagas", f"R$ {resultados['receitas_pagas']:,.2f}")
        col5.metric("Receitas Pendentes", f"R$ {resultados['receitas_pendentes']:,.2f}")

    preparar_grafico_receitas(df_mes)

    st.markdown("---")

    # -----------------------------
    # GRÁFICO DE DESPESA
    # -----------------------------

    st.subheader("Despesas")

    with st.container():
        col6, col7 = st.columns([1, 1])
        col6.metric("Despesas Pagas", f"R$ {resultados['despesas_pagas']:,.2f}")
        col7.metric("Despesas Pendentes", f"R$ {resultados['despesas_pendentes']:,.2f}")

    preparar_grafico_despesas(df_mes)

    st.markdown("---")

    # -----------------------------
    # EVOLUÇÃO AO LONGO DO TEMPO
    # -----------------------------
    preparar_grafico_evolucao(df_mes)

    # -----------------------------
    # TABELA PARA EXPORTAÇÃO
    # -----------------------------

    st.markdown("---")

    st.subheader("Tabela de Lançamentos do Período")

    excel_file = exportar_excel(df_mes)

    st.download_button(
        label="📥 Baixar tabela em Excel",
        data=excel_file,
        file_name="lancamentos_filtrados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    st.dataframe(df_mes, use_container_width=True)
