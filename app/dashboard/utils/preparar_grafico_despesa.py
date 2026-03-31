import streamlit as st
import plotly.express as px

def preparar_grafico_despesas(df_mes):
    st.markdown("### Distribuição de Despesas por Categoria")

    df_cat = df_mes[df_mes["Tipo"] == "Despesa"].copy()

    if df_cat.empty:
        st.info("Nenhuma despesa registrada neste período.")
        return

    fig_cat = px.pie(
        df_cat,
        names="Categoria",
        values="Valor",
        title="Despesas por Categoria"
    )
    st.plotly_chart(fig_cat, use_container_width=True)