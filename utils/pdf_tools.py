import tabula
import requests
import tempfile
import pandas as pd


def download_and_extract_table(url, pages):
    """
    Função para extrair tabelas de um documento pdf e juntar num dataframe
    :param pages: paginas do documento pdf a extrair as tabelas
    :return: dataframe com as tabelas extraidas
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        response = requests.get(url, timeout=10)  # Add timeout argument here
        pdf_path = f"{tmpdirname}/file.pdf"
        with open(pdf_path, "wb") as f:
            f.write(response.content)
        list_df = tabula.read_pdf(pdf_path, pages=pages)
        df = pd.concat(list_df)
        df.reset_index(drop=True, inplace=True)
    return df


def preprocess_idg(df):
    """
    Função para pré-processar o dataframe que tem infomração sobre os indicadores com impacto no IDG
    """
    # colect all the cells in the dataframe that has only numbers and no text
    # these cells are the id of the indicators

    # create a list with the id of the indicators

    # print(df["Unnamed: 3"].loc[7])

    return df
