import streamlit as st
import plotly.express as px

def preparar_grafico_evolucao(df_mes):
    st.markdown("### Evolução ao longo do tempo (Visão Mensal)")

    df_plot = df_mes.copy()

    df_plot["Ano"] = df_plot["Data"].dt.year
    df_plot["Mes"] = df_plot["Data"].dt.month

    df_plot = (
        df_plot.groupby(["Ano", "Mes", "Tipo"], as_index=False)["Valor"]
        .sum()
        .sort_values(["Ano", "Mes"])
    )

    df_plot["Label"] = (
        df_plot["Mes"].astype(str).str.zfill(2)
        + "/"
        + df_plot["Ano"].astype(str)
    )

    fig_bar = px.bar(
        df_plot,
        x="Label",
        y="Valor",
        color="Tipo",
        barmode="group",
        title="Receitas e Despesas por Mês",
        text_auto=True,
        color_discrete_map={"Receita": "green", "Despesa": "red"},
    )

    fig_bar.update_traces(textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)