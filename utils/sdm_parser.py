"""
Conjunto de funções para auxiliar o parseamento do HTML do site do SDM
"""

from bs4 import BeautifulSoup
import re


# Função para parsear com o bs4 o html do site do SDM numa lista de conteúdos que estão em colunas e linhas
def initial_parse(content):
    # Parse the html content
    soup = BeautifulSoup(content, "html.parser")

    # crair uma lista com os conteúdos do html
    info_in_list = [text for text in soup.stripped_strings]

    return info_in_list


# função para extrair o ano do código_siars
def ano_codigo_siars(codigo_siars):
    #Função para extrair o ano do código_siars
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
    texto_lista= lista[local_antes + 1 : local_depois]

    #contactonar lista em string
    texto = " ".join(texto_lista)
    
    return texto


# função para indentificar na lista produzida no parse_html() os cabeçalhos e o conteúdo
def main_parse(lista):
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
        "objetivo": extracao_texto_multilinha(lista,"Objetivo","Descrição do Indicador"), # extrair o objetivo do indicador
        "descrição_do_indicador": extracao_texto_multilinha(lista,"Descrição do Indicador", "Regras de cálculo"), # extrair o objetivo do indicador
    }

    return dicionario
