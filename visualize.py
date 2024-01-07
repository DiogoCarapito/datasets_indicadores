import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Visualização de dados", page_icon=":bar_chart:", layout="wide"
)

st.title("Visualização de dados")


tab_0, tab_1, tab_2, tab_3, tab_4, tab_5 = st.tabs(
    [
        "330 331 390 429",
        "Indicadores SDM",
        "Portaria IDE",
        "Indicadores Intervalos",
        "Indicadores Matrix",
        "Indicadores IDG",
    ]
)

with tab_0:
    st.subheader("330 331 390 429")

    sdm_330 = pd.read_csv("datasets/indicadores_em_csv/sdm_330.csv")
    sdm_331 = pd.read_csv("datasets/indicadores_em_csv/sdm_331.csv")
    sdm_390 = pd.read_csv("datasets/indicadores_em_csv/sdm_390.csv")
    sdm_429 = pd.read_csv("datasets/indicadores_em_csv/sdm_429.csv")

    # merge all the dataframes
    # sdm_330_331 = pd.merge(sdm_330, sdm_331, on="ID", how="outer")
    # sdm_330_331_390 = pd.merge(sdm_330_331, sdm_390, on="ID", how="outer")
    # sdm_330_331_390_429 = pd.merge(sdm_330_331_390, sdm_429, on="ID", how="outer")

    # st.dataframe(sdm_330_331_390_429.T)


with tab_1:
    st.subheader("Indicadores SDM")

    # read the csv file
    sdm = pd.read_csv("datasets/indicadores_sdm_complete.csv", index_col="id")

    # show the dataframe
    st.dataframe(sdm)


with tab_2:
    st.subheader("Portaria IDE")
    portaria = pd.read_csv("datasets/portaria_411a_2023.csv")
    st.metric("Número de indicadores", portaria.shape[0])
    st.dataframe(portaria)

    # create the intersection between the two dataframes by ID
    intersecion_df = pd.merge(portaria, sdm, on="id", how="inner")

    st.metric("Número de indicadores", intersecion_df.shape[0])
    st.dataframe(intersecion_df)


with tab_3:
    st.subheader("Indicadores Intervalos")

    indicadores_intervalos = pd.read_csv(
        "datasets/indicadores_intervalos_esperados_aceitaveis.csv"
    )
    st.dataframe(indicadores_intervalos)

with tab_4:
    st.subheader("Indicadores Matrix")
    indicadores_matrix = pd.read_csv("datasets/indicadores_matrix_multidimensional.csv")
    st.dataframe(indicadores_matrix)

with tab_5:
    st.subheader("Indicadores IDG")
    indicadores_idg = pd.read_csv("datasets/indicadores_impacto_idg.csv")
    st.dataframe(indicadores_idg)
