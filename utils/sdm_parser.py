"""
Conjunto de funções para auxiliar o parseamento do HTML do site do SDM
"""

from bs4 import BeautifulSoup
import re
import toml
import pandas as pd


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


# função para indentificar na lista produzida no parse_html() os cabeçalhos e o conteúdo
def main_parse_old(lista):
    # dicionario cabecaço e conteúdo em key:value pairs
    dicionario = {
        # cabeçalhos e conteúdos em localização fixa
        "id": lista[3],  # id do indicador
        "codigo": lista[7],  # código do indicador. é pouco usado
        "codigo_siars": lista[8],  # código do indicador completo
        "ano": ano_codigo_siars(lista[8]),  # ano do indicador existente no código_siars
        "nome_abreviado": lista[9],  # nome abreviado do indicador
        "designacao": lista[11],  # nome completo do indicador
        # cabeçalhos e conteúdos em localização variável
        "objetivo": extracao_texto_multilinha(
            lista, "Objetivo", "Descrição do Indicador"
        ),  # extrair o objetivo do indicador
        "descrição_do_indicador": extracao_texto_multilinha(
            lista, "Descrição do Indicador", "Regras de cálculo"
        ),  # extrair o objetivo do indicador
    }

    return dicionario


def stop_at_bi(parsed_html):
    # check if there is a item called "BI" in the list
    # remove all the items in the list that comes after the first "BI" string
    if "BI" in parsed_html:
        # remove all the items in the list that comes after the first "BI" string
        parsed_html = parsed_html[: parsed_html.index("BI")]

        # remove the last 4 items in the list
        parsed_html = parsed_html[:-4]

    return parsed_html


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
        #header_location["id"] = parsed_list[0]

        # create a dict with the header and the location of the text in the list
        header_location[each] = find_header(each)


    """ # create a list with a map of the content, where the value is the location of the text in the list and the key is the tex in that list spot. the max lenght og the list is the position of ACSS value
    lista_mapa = [None] * header_location["ACSS"]

    # iterate over the dict and append the value to the list where the location is the key
    for key, value in header_location.items():
        if value == None:
            continue
        print(key, value)
        lista_mapa[int(value)] = key"""
    
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


def main_parse(html):
    # parse the html into a list of strings
    parsed_content = soup_to_list(html)

    # remove the first 3 items in the list
    parsed_content = parsed_content[3:]

    # create a dictionary with the header location, so the text can be concatenated between the headers
    parsed_content = header_location_dictionary(parsed_content)

    # create a dictonary with the content
    # where the key is the header and the value is the content
    # based on the location of the header in the dict
    # final_content = dataframe_creation(header_location, parsed_content)
    #final_content = dataframe_creation(parsed_content)

    #return final_content

    return parsed_content
