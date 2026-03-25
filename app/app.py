import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from dateutil.relativedelta import relativedelta

from app.database import (
    init_db,
    init_saldos,
    insert_transaction,
    load_transactions,
    delete_transaction,
    load_categories,
    insert_category,
    update_category,
    delete_category,
    set_saldo_inicial,
    get_saldo_inicial
)

st.set_page_config(page_title="Finanças Pessoais", layout="wide")

init_db()
init_saldos()

st.title("💰 Painel de Organização Financeira Pessoal")

# ============================================================
#   ABAS PRINCIPAIS
# ============================================================

aba_dashboard, aba_lancamentos, aba_categorias = st.tabs([
    "📊 Dashboard",
    "📝 Lançamentos",
    "🗂️ Categorias"
])

# ============================================================
#   ABA DE CATEGORIAS
# ============================================================

with aba_categorias:
    st.header("Gerenciar Categorias")

    categorias = load_categories()

    # Adicionar categoria
    st.subheader("Adicionar nova categoria")
    nova_cat = st.text_input("Nome da nova categoria")
    if st.button("Adicionar categoria"):
        if nova_cat.strip() != "":
            insert_category(nova_cat.strip())
            st.success("Categoria adicionada!")
            st.rerun()

    # Editar categoria
    st.subheader("Editar categoria existente")
    cat_editar = st.selectbox("Categoria", categorias)
    novo_nome = st.text_input("Novo nome da categoria")
    if st.button("Salvar edição"):
        if novo_nome.strip() != "":
            update_category(cat_editar, novo_nome.strip())
            st.success("Categoria atualizada!")
            st.rerun()

    # Excluir categoria
    st.subheader("Excluir categoria")
    cat_excluir = st.selectbox("Categoria para excluir", categorias, key="excluir_cat")
    if st.button("Excluir categoria"):
        delete_category(cat_excluir)
        st.warning("Categoria excluída!")
        st.rerun()


# ============================================================
#   ABA DE LANÇAMENTOS
# ============================================================

with aba_lancamentos:
    st.header("Adicionar novo lançamento")

    # Recorrência FORA do form (para funcionar corretamente)
    recorrente = st.checkbox("Lançamento recorrente?")
    parcelas = 1
    if recorrente:
        parcelas = st.slider("Repetir por quantos meses?", 1, 12, 1)

    with st.form("form_lancamento"):
        col1, col2 = st.columns(2)

        date = col1.date_input("Data")
        type = col2.selectbox("Tipo", ["Receita", "Despesa"])

        category = st.selectbox("Categoria", load_categories())
        description = st.text_input("Descrição")
        value = st.number_input("Valor", min_value=0.0, format="%.2f")

        status = st.selectbox("Status do lançamento", ["Pago", "Pendente"])

        submitted = st.form_submit_button("Adicionar")

        if submitted:
            insert_transaction(
                str(date),
                type,
                category,
                description,
                value,
                status.lower(),
                1 if recorrente else 0,
                parcelas
            )

            if recorrente:
                data_base = datetime.strptime(str(date), "%Y-%m-%d")

                for i in range(1, parcelas):
                    nova_data = data_base + relativedelta(months=i)
                    insert_transaction(
                        nova_data.strftime("%Y-%m-%d"),
                        type,
                        category,
                        f"{description} (Parcela {i+1}/{parcelas})",
                        value,
                        "pendente",
                        0,
                        1
                    )

            st.success("Lançamento(s) adicionado(s) com sucesso!")
            st.rerun()

    # ============================================================
    #   EXCLUSÃO DE LANÇAMENTOS
    # ============================================================

    st.subheader("📄 Excluir lançamentos")

    data = load_transactions()
    df_lanc = pd.DataFrame(data, columns=[
        "ID", "Data", "Tipo", "Categoria", "Descrição", "Valor",
        "Status", "Recorrente", "Parcelas"
    ])

    if df_lanc.empty:
        st.info("Nenhum lançamento cadastrado ainda.")
    else:
        df_lanc["Data"] = pd.to_datetime(df_lanc["Data"])

        st.markdown("### 🔎 Filtros")

        categorias_unicas = ["Todas"] + sorted(df_lanc["Categoria"].unique())
        filtro_categoria = st.selectbox("Filtrar por Categoria", categorias_unicas)

        descricoes_unicas = ["Todas"] + sorted(df_lanc["Descrição"].dropna().unique())
        filtro_descricao = st.selectbox("Filtrar por Descrição", descricoes_unicas)

        df_excluir = df_lanc.copy()

        if filtro_categoria != "Todas":
            df_excluir = df_excluir[df_excluir["Categoria"] == filtro_categoria]

        if filtro_descricao != "Todas":
            df_excluir = df_excluir[df_excluir["Descrição"] == filtro_descricao]

        st.markdown("### 🗑️ Lançamentos filtrados")

        if df_excluir.empty:
            st.info("Nenhum lançamento encontrado com os filtros selecionados.")
        else:
            for index, row in df_excluir.iterrows():
                colA, colB = st.columns([0.1, 0.9])

                if colA.button("🗑️", key=f"del_lanc_{row['ID']}"):
                    delete_transaction(row["ID"])
                    st.warning(f"Lançamento {row['ID']} apagado!")
                    st.rerun()

                colB.write(
                    f"**{row['Data'].date()}** — {row['Tipo']} — {row['Categoria']} — "
                    f"{row['Descrição']} — R$ {row['Valor']:,.2f} — "
                    f"Status: {row['Status'].capitalize()}"
                )


# ============================================================
#   ABA DO DASHBOARD
# ============================================================

with aba_dashboard:

    data = load_transactions()
    df = pd.DataFrame(data, columns=[
        "ID", "Data", "Tipo", "Categoria", "Descrição", "Valor",
        "Status", "Recorrente", "Parcelas"
    ])

    st.header("📊 Visão Geral")

    if df.empty:
        st.info("Nenhum dado cadastrado ainda.")
    else:
        df["Data"] = pd.to_datetime(df["Data"])

        # ============================================================
        #   FILTROS LATERAIS
        # ============================================================

        st.sidebar.header("Filtros de Visualização")

        anos = sorted(df["Data"].dt.year.unique())
        anos_opcoes = ["Todos"] + [str(a) for a in anos]
        ano_sel = st.sidebar.selectbox("Ano", anos_opcoes)

        meses = sorted(df["Data"].dt.month.unique())
        meses_opcoes = ["Todos"] + [f"{m:02d}" for m in meses]
        mes_sel = st.sidebar.selectbox("Mês", meses_opcoes)

        # FILTRAR POR ANO
        if ano_sel == "Todos":
            df_filtrado = df.copy()
        else:
            df_filtrado = df[df["Data"].dt.year == int(ano_sel)]

        # FILTRAR POR MÊS
        if mes_sel != "Todos":
            df_filtrado = df_filtrado[df_filtrado["Data"].dt.month == int(mes_sel)]

        df_mes = df_filtrado.copy()

        # ============================================================
        #   SALDO ANTERIOR (COM LÓGICA AUTOMÁTICA)
        # ============================================================

        if ano_sel != "Todos" and mes_sel != "Todos":
            mes_atual = int(mes_sel)
            ano_atual = int(ano_sel)

            saldo_manual = get_saldo_inicial(ano_atual, mes_atual)

            if saldo_manual != 0:
                saldo_anterior = saldo_manual
            else:
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

                saldo_anterior = saldo_final_mes_ant

                set_saldo_inicial(ano_atual, mes_atual, saldo_final_mes_ant)

        else:
            saldo_anterior = 0

        # ============================================================
        #   AJUSTAR SALDO INICIAL MANUALMENTE
        # ============================================================

        st.markdown("### Ajustar saldo inicial do mês")

        colA, colB, colC = st.columns(3)

        ano_saldo = colA.number_input("Ano", min_value=2000, max_value=2100, value=int(ano_sel) if ano_sel != "Todos" else datetime.now().year)
        mes_saldo = colB.number_input("Mês", min_value=1, max_value=12, value=int(mes_sel) if mes_sel != "Todos" else datetime.now().month)
        valor_saldo = colC.number_input("Saldo inicial", format="%.2f")

        if st.button("Salvar saldo inicial"):
            set_saldo_inicial(ano_saldo, mes_saldo, valor_saldo)
            st.success("Saldo inicial atualizado!")
            st.rerun()

        # ============================================================
        #   MÉTRICAS
        # ============================================================

        col1, col2, col3, col4 = st.columns(4)

        total_receitas = df_mes[df_mes["Tipo"] == "Receita"]["Valor"].sum()
        total_despesas = df_mes[df_mes["Tipo"] == "Despesa"]["Valor"].sum()
        saldo = total_receitas - total_despesas
        saldo_acumulado = saldo_anterior + saldo

        col1.metric("Saldo Inicial (período anterior)", f"R$ {saldo_anterior:,.2f}")
        col2.metric("Receitas", f"R$ {total_receitas:,.2f}")
        col3.metric("Despesas", f"R$ {total_despesas:,.2f}")
        col4.metric("Saldo Acumulado", f"R$ {saldo_acumulado:,.2f}")

        # ============================================================
        #   GRÁFICO DE CATEGORIAS (APENAS DESPESAS)
        # ============================================================

        st.markdown("### Distribuição de Gastos por Categoria")

        df_cat = df_mes[df_mes["Tipo"] == "Despesa"].copy()

        if df_cat.empty:
            st.info("Nenhuma despesa registrada neste período.")
        else:
            fig_cat = px.pie(
                df_cat,
                names="Categoria",
                values="Valor",
                title="Gastos por Categoria"
            )
            st.plotly_chart(fig_cat, use_container_width=True)

        # ============================================================
        #   EVOLUÇÃO AO LONGO DO TEMPO
        # ============================================================

        st.markdown("### Evolução ao longo do tempo")
        visao = st.selectbox("Visualizar por:", ["Dia", "Mês", "Ano"], key="visao_tempo")

        df_plot = df_mes.copy()

        if visao == "Dia":
            df_plot = df_plot.sort_values("Data", ascending=True)
            df_plot["Label"] = df_plot["Data"].dt.strftime("%d/%m")

        elif visao == "Mês":
            df_plot["Ano"] = df_plot["Data"].dt.year
            df_plot["Mes"] = df_plot["Data"].dt.month

            df_plot = (
                df_plot
                .groupby(["Ano", "Mes", "Tipo"], as_index=False)["Valor"]
                .sum()
                .sort_values(["Ano", "Mes"], ascending=True)
            )

            df_plot["Label"] = df_plot["Mes"].astype(str).str.zfill(2) + "/" + df_plot["Ano"].astype(str)

        elif visao == "Ano":
            df_plot["Ano"] = df_plot["Data"].dt.year

            df_plot = (
                df_plot
                .groupby(["Ano", "Tipo"], as_index=False)["Valor"]
                .sum()
                .sort_values("Ano", ascending=True)
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
            color_discrete_map={"Receita": "green", "Despesa": "red"}
        )

        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True)