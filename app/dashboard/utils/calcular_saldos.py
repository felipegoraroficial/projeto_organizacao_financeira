import pandas as pd


def calcular_saldos(df_lanc: pd.DataFrame, saldo_inicial: float):
    """
    Calcula:
    - Saldo Final (realizado)
    - Saldo Previsto (projetado)
    - Total de receitas e despesas (pagas e pendentes)

    df_lanc deve conter colunas:
    ["Tipo", "Valor", "Status"]
    """

    # Garantir consistência
    df_lanc["Status"] = df_lanc["Status"].str.lower()
    df_lanc["Tipo"] = df_lanc["Tipo"].str.lower()

    # Filtrar pagos e pendentes
    df_pagos = df_lanc[df_lanc["Status"] == "pago"]
    df_pendentes = df_lanc[df_lanc["Status"] == "pendente"]

    # Receitas e despesas pagas
    receitas_pagas = df_pagos[df_pagos["Tipo"] == "receita"]["Valor"].sum()
    despesas_pagas = df_pagos[df_pagos["Tipo"] == "despesa"]["Valor"].sum()

    # Receitas e despesas pendentes
    receitas_pendentes = df_pendentes[df_pendentes["Tipo"] == "receita"]["Valor"].sum()
    despesas_pendentes = df_pendentes[df_pendentes["Tipo"] == "despesa"]["Valor"].sum()

    # Saldo Final (somente efetivado)
    saldo_final = saldo_inicial + receitas_pagas - despesas_pagas

    # Saldo Previsto (efetivado + pendente)
    saldo_previsto = (
        saldo_inicial
        + (receitas_pagas + receitas_pendentes)
        - (despesas_pagas + despesas_pendentes)
    )

    return {
        "receitas_pagas": receitas_pagas,
        "despesas_pagas": despesas_pagas,
        "receitas_pendentes": receitas_pendentes,
        "despesas_pendentes": despesas_pendentes,
        "saldo_final": saldo_final,
        "saldo_previsto": saldo_previsto,
    }
