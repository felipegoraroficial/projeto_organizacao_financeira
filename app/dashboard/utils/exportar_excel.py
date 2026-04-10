from io import BytesIO

import pandas as pd


def exportar_excel(df: pd.DataFrame, sheet_name="Lançamentos"):
    """
    Converte um DataFrame em um arquivo Excel (bytes) para download no Streamlit.
    """
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, index=False, sheet_name=sheet_name)
    writer.close()
    return output.getvalue()
