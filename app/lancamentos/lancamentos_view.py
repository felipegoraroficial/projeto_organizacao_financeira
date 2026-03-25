import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

from app.database_functions import (
    insert_transaction,
    load_transactions,
    delete_transaction,
    load_categories,
)


def render_lancamentos():
    st.header("Adicionar novo lançamento")

    # Recorrência fora do form
    recorrente = st.checkbox("Lançamento recorrente?")
    parcelas = st.slider("Repetir por quantos meses?", 1, 12, 1) if recorrente else 1

    with st.form("form_lancamento"):
        col1, col2 = st.columns(2)

        date = col1.date_input("Data")
        tipo = col2.selectbox("Tipo", ["Receita", "Despesa"])  # <-- corrigido

        category = st.selectbox("Categoria", load_categories())
        description = st.text_input("Descrição")
        value = st.number_input("Valor", min_value=0.0, format="%.2f")

        status = st.selectbox("Status do lançamento", ["Pago", "Pendente"])

        submitted = st.form_submit_button("Adicionar")

        if submitted:
            insert_transaction(
                str(date),
                tipo,  # <-- corrigido
                category,
                description,
                value,
                status.lower(),
                1 if recorrente else 0,
                parcelas,
            )

            if recorrente:
                data_base = datetime.strptime(str(date), "%Y-%m-%d")
                for i in range(1, parcelas):
                    nova_data = data_base + relativedelta(months=i)
                    insert_transaction(
                        nova_data.strftime("%Y-%m-%d"),
                        tipo,  # <-- corrigido
                        category,
                        f"{description} (Parcela {i+1}/{parcelas})",
                        value,
                        "pendente",
                        0,
                        1,
                    )

            st.success("Lançamento(s) adicionado(s) com sucesso!")
            st.rerun()

    # Exclusão de lançamentos
    st.subheader("📄 Excluir lançamentos")

    data = load_transactions()
    df_lanc = pd.DataFrame(
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
        ],
    )

    if df_lanc.empty:
        st.info("Nenhum lançamento cadastrado ainda.")
        return

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
        return

    for _, row in df_excluir.iterrows():  # <-- corrigido
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