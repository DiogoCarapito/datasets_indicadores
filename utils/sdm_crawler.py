"""
sdm crawlers
"""

import requests
import toml


# function to scrape a single url
def sdm_html_extraction(id_indicador):
    # ir buscar o url do pdf ao ficheiro de configuração com as variaveis
    with open("./variaveis.toml", "r", encoding="utf-8") as file:
        config = toml.load(file)

    # url
    url = config["url_sdm"] + str(id_indicador)

    try:
        # request the url
        rqst = requests.get(url, timeout=30)

        # success message
        print(f"{id_indicador} Scraped!")

        # return the html
        return rqst.content

    # exception if the request times out
    except requests.exceptions.Timeout:
        message = f"Request for {id} timed out"
        print(message)
        return message

    except requests.exceptions.ConnectionError:
        message = f"Request for {id} failed"
        print(message)
        return message


# function to scrape a batch of urls and returns as a dictionary
def sdm_batch_crawler(begin, end):
    # create a list from 1 to 448
    id_list = [i for i in range(begin, end)]

    # dictionary to store the content
    dict_content = {}

    # iterate over the list of ids
    for url_code in id_list:
        # append the html to a dictionary of ids
        dict_content[url_code] = sdm_html_extraction(url_code)

    # return the dictionary
    return dict_content
