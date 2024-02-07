import toml
import tabula
import requests
import tempfile
import pandas as pd


# get the max id to scrape from the config file
def sdm_max():
    with open("variaveis.toml", "r", encoding="utf-8") as file:
        config = toml.load(file)
    return config["sdm_indicador_final"]


# table extraction from pdf in a url
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


def func():
    return None
