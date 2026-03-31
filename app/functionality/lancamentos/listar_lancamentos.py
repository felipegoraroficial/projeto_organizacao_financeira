from datetime import datetime

import pandas as pd
import streamlit as st

from app.database import (
    delete_transaction,
    load_transactions,
    marcar_como_pago,
)


def render_listar_lancamentos():
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
            "DataPagamento",
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

    df_filtrado = df_lanc.copy()

    if filtro_categoria != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Categoria"] == filtro_categoria]

    if filtro_descricao != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Descrição"] == filtro_descricao]

    st.markdown("### 🗑️ / ✔️ Lançamentos filtrados")

    if df_filtrado.empty:
        st.info("Nenhum lançamento encontrado com os filtros selecionados.")
        return

    for _, row in df_filtrado.iterrows():
        colA, colB, colC = st.columns([0.1, 0.1, 0.8])

        # Excluir
        if colA.button("🗑️", key=f"del_{row['ID']}"):
            delete_transaction(row["ID"])
            st.warning(f"Lançamento {row['ID']} apagado!")
            st.rerun()

        # Marcar como pago
        if row["Status"] == "pendente":
            if colB.button("✔️", key=f"pago_{row['ID']}"):
                data_pag = st.date_input(
                    "Data do pagamento",
                    key=f"data_pag_{row['ID']}",
                    value=datetime.today(),
                )
                marcar_como_pago(row["ID"], str(data_pag))
                st.success(f"Lançamento {row['ID']} marcado como pago!")
                st.rerun()
        else:
            colB.write("✅")

        texto = (
            f"**{row['Data'].date()}** — {row['Tipo']} — {row['Categoria']} — "
            f"{row['Descrição']} — R$ {row['Valor']:,.2f} — "
            f"Status: {row['Status'].capitalize()}"
        )

        if row["DataPagamento"]:
            texto += f" — Pago em: {row['DataPagamento']}"

        colC.write(texto)
