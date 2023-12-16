import streamlit as st
import pandas as pd

st.set_page_config(page_title="Visualização de dados", page_icon=":bar_chart:", layout="wide")

st.title("Visualização de dados")


tab_1, tab_2, tab_3, tab_4, tab_5 = st.tabs([
    "Indicadores SDM",
    "Portaria IDE",
    "Indicadores Intervalos",
    "Indicadores Matrix",
    "Indicadores IDG"
    ]
)

with tab_1:
    st.subheader("Indicadores SDM")
    
    st.dataframe(pd.read_csv("datasets/indicadores_em_csv/sdm_331.csv").T)
    
    # read the csv file
    sdm = pd.read_csv("datasets/indicadores_sdm.csv", index_col="ID")
    
    # show the dataframe
    st.dataframe(sdm)


with tab_2:
    st.subheader("Portaria IDE")
    portaria = pd.read_csv("datasets/portaria_411a_2023.csv")
    st.table(portaria)


with tab_3:
    st.subheader("Indicadores Intervalos")
    
    indicadores_intervalos = pd.read_csv(
    "datasets/indicadores_intervalos_esperados_aceitaveis.csv"
)
    st.table(indicadores_intervalos)

with tab_4:
    st.subheader("Indicadores Matrix")
    indicadores_matrix = pd.read_csv("datasets/indicadores_matrix_multidimensional.csv")
    st.table(indicadores_matrix)

with tab_5:
    st.subheader("Indicadores IDG")
    indicadores_idg = pd.read_csv("datasets/indicadores_impacto_idg.csv")
    st.table(indicadores_idg)
