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


def func():
    return None
