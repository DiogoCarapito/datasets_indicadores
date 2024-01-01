import tabula
import requests
import tempfile
import pandas as pd


def intervalo_esperado_portaria_parse(df):
    # intervalo minimois between a [ and a ;
    df["min_esperado"] = df["Intervalo esperado"].str.extract(r"\[(.*?);")

    # intervalo maximo is between a ; and a ]
    df["max_esperado"] = df["Intervalo esperado"].str.extract(r";(.*?)\]")

    return df


def intervalo_aceitavel_portaria_parse(df):
    # intervalo minimois between a [ and a ;
    df["min_aceitavel"] = df["Intervalo aceitável"].str.extract(r"\[(.*?);")

    # ge the sencond part of the string after the U
    df["max_aceitavel"] = df["Intervalo aceitável"].str.split("U").str[1]
    df["max_aceitavel"] = df["max_aceitavel"].str.extract(r"\;(.*?)]")

    return df


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


def process_portaria_411a_2023(df):
    df = pd.DataFrame(df)

    # rename columns
    df.rename(
        columns={
            "Unnamed: 0": "Dimensão",
            "N.o": "id",
            "Unnamed: 1": "Nome",
            "Unnamed: 2": "Ponderação",
            "Valores": "Intervalo esperado",
            "Variações": "Intervalo aceitável",
        },
        inplace=True,
    )

    # remover as linhas que não interessam
    df.drop([0, 1], axis=0, inplace=True)

    # reset index
    df.reset_index(drop=True, inplace=True)

    # remove " . . . " from "Dimensão" column and "Nome" column
    df["Dimensão"] = df["Dimensão"].str.replace(" .", "")
    df["Nome"] = df["Nome"].str.replace(" .", "")

    # remove all lines that have <NA>
    df.dropna(axis=0, inplace=True)

    # adicionar uma linha que não foi lida automaticamente
    df.loc[41] = [
        "Gestão da Doença",
        "261",
        "Utentes com avaliação do risco de úlcera de pé",
        "1,5",
        "[87;100]",
        "[70;87[U]100;100]",
    ]

    # remove " caracter from "Ponderação" column
    df["Ponderação"] = df["Ponderação"].str.replace('"', "")

    # extract the min and max values from "intervalos" into 4 new columns
    df = intervalo_esperado_portaria_parse(df)
    df = intervalo_aceitavel_portaria_parse(df)

    # substitute , to . so it can be converted to float in ponderacao and intervalo_esperado_minimo, intervalo_esperado_maximo, intervalo_aceitavel_minimo, intervalo_aceitavel_maximo
    df["Ponderação"] = df["Ponderação"].str.replace(",", ".")
    df["min_esperado"] = df["min_esperado"].str.replace(",", ".")
    df["max_esperado"] = df["max_esperado"].str.replace(",", ".")
    df["min_aceitavel"] = df["min_aceitavel"].str.replace(",", ".")
    df["max_aceitavel"] = df["max_aceitavel"].str.replace(",", ".")

    return df
