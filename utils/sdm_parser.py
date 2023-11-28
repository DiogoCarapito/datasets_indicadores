"""
Conjunto de funções para auxiliar o parseamento do HTML do site do SDM
"""

from bs4 import BeautifulSoup
import re
import toml
import pandas as pd


def header_text_mapper(dicionario):
    # remove key with None as value
    dicionario = {key: value for key, value in dicionario.items() if value is not None}

    # ACSS define o comprimento máximo da lista com o html parseado
    comprimento_maximo = dicionario["ACSS"]
    # comprimento_maximo = len(dicionario)

    # lista com o mapa dos cabeçalhos e textos referentes aos cabeçalhos
    mapa = []

    # etiqueta com o nome do cabeçalho inicial
    header = "ID"

    # iterate from 0 to comprimento_maximo
    for i in range(comprimento_maximo):
        # check if the value of the key is equal to i
        if i in dicionario.values():
            # header becomes the key of the value i
            header = list(dicionario.keys())[list(dicionario.values()).index(i)]

            # add the header to the list
            mapa.append(header)
        else:
            # add the header to the list
            mapa.append(header + "_TEXT")

    return mapa


# Função para parsear com o bs4 o html do site do SDM numa lista de conteúdos que estão em colunas e linhas
def soup_to_list(html):
    # Parse the html content
    soup = BeautifulSoup(html, "html.parser")

    # crair uma lista com os conteúdos do html
    info_in_list = [text for text in soup.stripped_strings]

    # remover os 3 primeiros elementos da lista que são sempre os mesmos
    # info_in_list = info_in_list[3:]

    return info_in_list


# função para extrair o ano do código_siars
def ano_codigo_siars(codigo_siars):
    # Função para extrair o ano do código_siars
    try:
        ano = re.findall(r"\d{4}", codigo_siars)[0]
    except IndexError:
        ano = None
    return ano


def extracao_texto_multilinha(lista, etiqueta_antes, etiqueta_depois):
    # localização do antes e depois
    local_antes = lista.index(etiqueta_antes)
    local_depois = lista.index(etiqueta_depois)

    # extrair texto entre as etiquetas
    texto_lista = lista[local_antes + 1 : local_depois]

    # contactonar lista em string
    texto = " ".join(texto_lista)

    return texto


def header_location_dictionary(parsed_list):
    # create a dictionary with the header location, so the text can be concatenated between the headers
    # not all headers exist in all pages, so the location of the headers is not always the same

    # ir buscar o url do pdf ao ficheiro de configuração com as variaveis
    with open("./variaveis.toml", "r", encoding="utf-8") as file:
        config = toml.load(file)

    # url
    list_of_headers = config["sdm_headers"]

    header_location = {}

    # function to find the location of the header in the list
    def find_header(header):
        try:
            return parsed_list.index(header)
        except ValueError:
            return None

    for each in list_of_headers:
        # id
        # header_location["id"] = parsed_list[0]

        # create a dict with the header and the location of the text in the list
        header_location[each] = find_header(each)

    return header_location

    # append header_location into a csv file for future reference
    # each header is a column's name and the value is the location of the text in the list
    # create a id columnm with the id of the indicator
    # with open("sdm/header_location.csv", "w", encoding="utf-8") as file:
    #    for key, value in header_location.items():
    #        file.write(f"{key},{value}\n")


# def dataframe_creation(header_location, parsed_content):
def dataframe_creation(parsed_content):
    # the text is after it's header and before the next header
    return parsed_content


def substitute_first(list_tupples, old, new, index_move):
    for i, each in enumerate(list_tupples):
        if each[0] == old:
            if index_move != 0:
                list_tupples.insert(i + index_move, (new, each[1]))
                list_tupples.remove(each)
            else:
                list_tupples[i] = (new, each[1])
            break

    return list_tupples


def correccao_intervalos(lista_correspondencias):
    # transform list of tupples into a dataframe
    df = pd.DataFrame(lista_correspondencias, columns=["titulo", "texto"])

    # count how many times "Variação Aceitável_TEXT" in header column
    count = df["titulo"].value_counts()["Variação Aceitável_TEXT"]

    # calculate the trigger to change the header
    trigger = count / 2

    # loop over the df[df["header"]=="Variação Aceitável_TEXT"] and correct the header
    for i, index in enumerate(df[df["titulo"] == "Variação Aceitável_TEXT"].index):
        if i < trigger:
            df.loc[index, "titulo"] = "Intervalo Aceitável_TEXT"
        else:
            df.loc[index, "titulo"] = "Intervalo Esperado_TEXT"

    # transform back df into a list of tupples
    lista_correspondencias_corrigida = list(df.itertuples(index=False, name=None))

    return lista_correspondencias_corrigida


def correcoes_correspondencias(lista_correspondencias):
    # correções de correspondencias entre titulo e texto
    # correções de ordem com ajuste de posição
    substituicoes = [
        ("Nome abreviado_TEXT", "Código_TEXT", -2),
        ("Nome abreviado_TEXT", "Código SIARS_TEXT", -1),
        ("Estado do indicador_TEXT", "Fórmula_TEXT", -3),
        ("Estado do indicador_TEXT", "Unidade de medida_TEXT", -2),
        ("Estado do indicador_TEXT", "Output_TEXT", -1),
        ("Variação Aceitável_TEXT", "Área | Subárea | Dimensão_TEXT", -2),
        ("Prazo para Registos_TEXT", "Tipo de Indicador_TEXT", -3),
        ("Prazo para Registos_TEXT", "Área clínica_TEXT", -2),
        ("Prazo para Registos_TEXT", "Inclusão de utentes no indicador_TEXT", -1),
    ]

    for each in substituicoes:
        lista_correspondencias = substitute_first(
            lista_correspondencias, each[0], each[1], each[2]
        )

    # correção especial do intervalo aceitavel e esperado
    lista_correspondencias_corrigida = correccao_intervalos(lista_correspondencias)

    return lista_correspondencias_corrigida


def final_cleaning(lista_correspondencias):
    df = pd.DataFrame(lista_correspondencias, columns=["titulo", "texto"])
    # remove rows where header ends with _TEXT
    df["to_remove"] = [
        False if each.endswith("_TEXT") else True for each in df["titulo"]
    ]
    df.drop(df[df["to_remove"] == True].index, inplace=True)
    df.drop(columns=["to_remove"], inplace=True)
    # reset index
    df.reset_index(drop=True, inplace=True)

    # remove the text "_TEXT" from the headers
    df["titulo"] = [each.replace("_TEXT", "") for each in df["titulo"]]

    # remove all the rows after header "Prazo para Registos"
    index_after_prazo = df[df["titulo"] == "Prazo para Registos"].index[0]
    index_to_remove = index_after_prazo + 1
    df.drop(df.index[index_to_remove:], inplace=True)

    i = 0
    while i < len(df["titulo"]) - 1:
        if df.loc[i, "titulo"] == df.loc[i + 1, "titulo"]:
            df.loc[i, "texto"] += "\n" + df.loc[i + 1, "texto"]
            df.drop(i + 1, inplace=True)
            df.reset_index(drop=True, inplace=True)
        else:
            i += 1

    return df


def list_to_csv(parsed_content, header_map):
    lista_correspondencias = []
    for i in range(len(header_map)):
        lista_correspondencias.append((header_map[i], parsed_content[i]))

    lista_correspondencias = correcoes_correspondencias(lista_correspondencias)

    df = final_cleaning(lista_correspondencias)

    return df


def main_parse(html):
    # parse the html into a list of strings
    parsed_content = soup_to_list(html)

    # remove the first 3 items in the list
    parsed_content = parsed_content[3:]

    # if the first 5 letterins in the 0 index of the list are "Erro."
    if parsed_content[0][:5] != "Erro.":
        # create a dictionary with the header location, so the text can be concatenated between the headers
        header_dict = header_location_dictionary(parsed_content)

        # create a list o f tupples with the header and the text
        header_map = header_text_mapper(header_dict)

        final_csv = list_to_csv(parsed_content, header_map)

    else:
        print(parsed_content[0])
        final_csv = None

    return final_csv
