"""
Script para extrair informação sobre indicadores do documento Operacionalização da Contratualização nos Cuidados de Saúde Primários para 2023
ANEXO XVI – INDICADORES: INTERVALOS ESPERADOS E VARIAÇÃO ACEITÁVEL (paginas 74-78)
"""

# import pandas as pd
import streamlit as st
from utils.utils import download_and_extract_table

# URL do documento Operacionalização da Contratualização nos Cuidados de Saúde Primários para 2023
url = "https://www.acss.min-saude.pt/wp-content/uploads/2016/10/Operacionalizacao_CSP_2023_VF.pdf"

# paginas do documento pdf a extrair as tabelas
paginas = "74-78"

# extrair as tabelas do documento pdf atravez do url
df = download_and_extract_table(url, paginas)

# Processar o dataframe
# remover as linhas cuja coluna ID Indicador é <NA>
df = df[df["ID Indicador"].notna()]

# reset index
df = df.reset_index(drop=True)

# tornar ID Indicador em int
df["ID Indicador"] = df["ID Indicador"].astype(int)

# renomear colunas do dataframe
df = df.rename(
    columns={
        "ID Indicador": "id_indicador",
        "Nome Indicador": "nome_indicador",
        "Int var.": "intervalo_aceitavel",
        "Int. Esperado": "intervalo_esperado",
    }
)

# criar 4 novas colunas com os valores dos intervalos esperados e aceitaveis
# remover os parentises retos das colunas min_esperado, max_esperado, min_aceitavel e max_aceitavel
# transformar os valores em float

# Esperado
df[["min_esperado", "max_esperado"]] = df["intervalo_esperado"].str.split(
    ";", expand=True
)
df["min_esperado"] = df["min_esperado"].str.replace("[", "").astype(float)
df["max_esperado"] = df["max_esperado"].str.replace("]", "").astype(float)

# Aceitável
df[["min_aceitavel", "max_aceitavel"]] = df["intervalo_aceitavel"].str.split(
    ";", expand=True
)
df["min_aceitavel"] = df["min_aceitavel"].str.replace("[", "").astype(float)
df["max_aceitavel"] = df["max_aceitavel"].str.replace("]", "").astype(float)

# visualizar o dataframe com streamlit
st.table(df)

# gravar o dataframe em csv
df.to_csv("datasets/indicadores_intervalos_esperados_aceitaveis.csv", index=False)
