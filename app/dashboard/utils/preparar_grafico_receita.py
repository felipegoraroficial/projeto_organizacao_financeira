import plotly.express as px
import streamlit as st


def preparar_grafico_receitas(df_mes):
    st.markdown("### Distribuição de Receitas por Categoria")

    df_rec = df_mes[df_mes["Tipo"] == "Receita"].copy()

    if df_rec.empty:
        st.info("Nenhuma receita registrada neste período.")
        return

    fig_rec = px.pie(
        df_rec, names="Categoria", values="Valor", title="Receitas por Categoria"
    )

    st.plotly_chart(fig_rec, use_container_width=True)
