import streamlit as st
import plotly.express as px


from app.database_functions import get_saldo_inicial, set_saldo_inicial


def filtrar_por_periodo(df, ano_sel, mes_sel):
    df_filtrado = df.copy()

    if ano_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Data"].dt.year == int(ano_sel)]

    if mes_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Data"].dt.month == int(mes_sel)]

    return df_filtrado


def calcular_saldo_anterior(df, ano_sel, mes_sel):
    if ano_sel == "Todos" or mes_sel == "Todos":
        return 0

    ano_atual = int(ano_sel)
    mes_atual = int(mes_sel)

    saldo_manual = get_saldo_inicial(ano_atual, mes_atual)
    if saldo_manual != 0:
        return saldo_manual

    # mês anterior
    if mes_atual == 1:
        mes_ant = 12
        ano_ant = ano_atual - 1
    else:
        mes_ant = mes_atual - 1
        ano_ant = ano_atual

    saldo_inicial_mes_ant = get_saldo_inicial(ano_ant, mes_ant)

    df_mes_ant = df[
        (df["Data"].dt.year == ano_ant) &
        (df["Data"].dt.month == mes_ant)
    ]

    total_rec_ant = df_mes_ant[df_mes_ant["Tipo"] == "Receita"]["Valor"].sum()
    total_desp_ant = df_mes_ant[df_mes_ant["Tipo"] == "Despesa"]["Valor"].sum()

    saldo_final_mes_ant = saldo_inicial_mes_ant + (total_rec_ant - total_desp_ant)

    set_saldo_inicial(ano_atual, mes_atual, saldo_final_mes_ant)

    return saldo_final_mes_ant


def preparar_grafico_categorias(df_mes):
    st.markdown("### Distribuição de Gastos por Categoria")

    df_cat = df_mes[df_mes["Tipo"] == "Despesa"].copy()

    if df_cat.empty:
        st.info("Nenhuma despesa registrada neste período.")
        return

    fig_cat = px.pie(
        df_cat,
        names="Categoria",
        values="Valor",
        title="Gastos por Categoria"
    )
    st.plotly_chart(fig_cat, use_container_width=True)


def preparar_grafico_evolucao(df_mes):
    st.markdown("### Evolução ao longo do tempo")

    visao = st.selectbox("Visualizar por:", ["Dia", "Mês", "Ano"], key="visao_tempo")

    df_plot = df_mes.copy()

    if visao == "Dia":
        df_plot = df_plot.sort_values("Data")
        df_plot["Label"] = df_plot["Data"].dt.strftime("%d/%m")

    elif visao == "Mês":
        df_plot["Ano"] = df_plot["Data"].dt.year
        df_plot["Mes"] = df_plot["Data"].dt.month

        df_plot = (
            df_plot.groupby(["Ano", "Mes", "Tipo"], as_index=False)["Valor"]
            .sum()
            .sort_values(["Ano", "Mes"])
        )

        df_plot["Label"] = df_plot["Mes"].astype(str).str.zfill(2) + "/" + df_plot["Ano"].astype(str)

    elif visao == "Ano":
        df_plot["Ano"] = df_plot["Data"].dt.year

        df_plot = (
            df_plot.groupby(["Ano", "Tipo"], as_index=False)["Valor"]
            .sum()
            .sort_values("Ano")
        )

        df_plot["Label"] = df_plot["Ano"].astype(str)

    fig_bar = px.bar(
        df_plot,
        x="Label",
        y="Valor",
        color="Tipo",
        barmode="group",
        title=f"Receitas e Despesas por {visao}",
        text_auto=True,
        color_discrete_map={"Receita": "green", "Despesa": "red"},
    )

    fig_bar.update_traces(textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)