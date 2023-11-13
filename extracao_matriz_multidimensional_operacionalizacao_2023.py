"""
Script para extrair informação sobre indicadores do documento Operacionalização da Contratualização nos Cuidados de Saúde Primários para 2023
MATRIZ MULTIDIMENSIONAL DAS USF E UCSP (paginas 13-15)
"""

# import pandas as pd
import streamlit as st
from utils.utils import download_and_extract_table

# URL do documento Operacionalização da Contratualização nos Cuidados de Saúde Primários para 2023
url = "https://www.acss.min-saude.pt/wp-content/uploads/2016/10/Operacionalizacao_CSP_2023_VF.pdf"

# MATRIZ MULTIDIMENSIONAL DAS USF E UCSP (paginas 13-15)
# paginas do documento pdf a extrair as tabelas
paginas = "13-15"

# extrair as tabelas do documento pdf atravez do url
df = download_and_extract_table(url, paginas)

# Processar o dataframe

# show dataframe using streamlit
st.dataframe(df)

# gravar o dataframe em csv
df.to_csv("datasets/matriz_multidimensional_usf_e_ucsp.csv", index=False)
