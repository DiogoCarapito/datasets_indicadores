import pandas as pd
import os
import re


def num_denom_paragraph(text):
    # add a new line between the "." and "Numerador" or "Denominador" in the text provided
    return text.replace(". Numerador", ".\nNumerador").replace(
        ". Denominador", ".\nDenominador"
    )


def separar_ano_intervalos(df):
    # Nome das colunas que são fonte de informação dos intevalos
    colunas = ["Intervalo Aceitável", "Intervalo Esperado"]

    # Etiquetas para depois colocar nas tabelas
    etiquetas = ["aceitavel", "esperado"]

    # percorrer todas as linhas (indicadores)
    for row in df.to_dict("records"):
        # alternar entree aceitavel e esperdo
        for coluna, etiqueta in zip(colunas, etiquetas):
            # primeira descodificação: saber que anos existem com re
            anos = re.findall(r"Ano de (\d{4}):", row[coluna])

            # criar uma coluna com os anos extraidos
            df["anos_disponiveis"] = ", ".join(anos)

            # ir ano a ano
            for ano in anos:
                # segunda descodificação: tirar o intervalo com outra re
                intervalo = re.search(f"Ano de {ano}: \[([^\]]+)\]", row[coluna]).group(
                    1
                )

                # criar uma lista
                intervalo_lista = intervalo.split("; ")

                # crair uma expressão em texto e gravar numa coluna
                df[f"{etiqueta}_{ano}"] = f"[{intervalo}]"

                # criar uma coluna para min e outra para max
                df[f"min_{etiqueta}_{ano}"] = intervalo_lista[0]  # min
                df[f"max_{etiqueta}_{ano}"] = intervalo_lista[1]  # max

    return df


def csv_crawler():
    # get the list of files in the folder to create a loop that opnes and saves in a dataframe
    directory = "./datasets/indicadores_em_csv/"

    csv_files = [f for f in os.listdir(directory) if f.endswith(".csv")]

    csv_files.sort()

    # print(csv_files)

    # new dataframe to save all the data
    df = pd.DataFrame()

    # for loop to open each csv file and save it in the dataframe
    for file in csv_files:
        # construct full file path
        file_path = os.path.join(directory, file)

        # read the CSV file into a DataFrame
        temp_df = pd.read_csv(file_path)

        # make the first column the index
        temp_df.set_index(temp_df.columns[0], inplace=True)

        # transpose the DataFrame
        temp_df = temp_df.T

        try:
            # make ID the index
            temp_df.set_index("Código", inplace=True)

            # append the temp_df DataFrame to the main df DataFrame
            df = pd.concat([df, temp_df], ignore_index=False, join="outer")

        except pd.errors.InvalidIndexError as e:
            print(f"Erro. ID: {file} - {e}")

    # Change column ID to id
    df.rename(columns={"ID": "id"}, inplace=True)

    # make id as integer
    df["id"] = df["id"].astype(int)

    # sort the columns by id column
    df.set_index("id", inplace=True)

    # substituir o texto "Numerador" e "Denominador" por um novo parágrafo
    df["Descrição do Indicador"] = df["Descrição do Indicador"].apply(
        num_denom_paragraph
    )

    # adicionar novas colunas com os intervalos aceitaveis e esprados com os valores minimos e máximos por ano
    df = separar_ano_intervalos(df)

    # save the dataframe as csv in datasets folder
    df.to_csv("./datasets/indicadores_sdm.csv", index=True)


if __name__ == "__main__":
    csv_crawler()
