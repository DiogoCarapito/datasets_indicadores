import streamlit as st
import pandas as pd

st.title("Visualização de dados")

tab_1, tab_2, tab_3 = st.tabs(
    ["Indicadores Intervalos", "Indicadores Matrix", "Indicadores IDG"]
)

# read a csv file
indicadores_intervalos = pd.read_csv(
    "datasets/indicadores_intervalos_esperados_aceitaveis.csv"
)
indicadores_matrix = pd.read_csv("datasets/indicadores_matrix_multidimensional.csv")
indicadores_idg = pd.read_csv("datasets/indicadores_impacto_idg.csv")

with tab_1:
    st.subheader("Indicadores Intervalos")

    st.table(indicadores_intervalos)

with tab_2:
    st.subheader("Indicadores Matrix")

    st.table(indicadores_matrix)

with tab_3:
    st.subheader("Indicadores IDG")

    st.table(indicadores_idg)
