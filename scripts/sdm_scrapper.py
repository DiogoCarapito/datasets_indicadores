"""
Scrapes the SDM website for the latest data and saves it to a csv file.
It organizes the data in a table format
it uses click to create a command line interface
"""

import click
import sys

# adicionar o path para a poder usar a pasta do projeto
sys.path.append("./")
from utils.sdm_crawler import sdm_html_extraction
from utils.sdm_parser import main_parse


#@click.command()
#@click.option("--begin", default=1, help="Initial ID to start scraping")
#@click.option("--end", default=5, help="Final ID to stop scraping")
# @click.option("--end", default=448, help="Final ID to stop scraping")
def scrapper(begin=1, end=5):
    # create a list of ids to scrape
    # end + 1 because the range function doesn't include the last number
    id_list = [i for i in range(begin, end + 1)]

    # iterate over the list of ids
    for each in id_list:

        # scrape the url
        html = sdm_html_extraction(each)

        # transform the html into a list
        parsed_html = main_parse(html)

    return parsed_html

