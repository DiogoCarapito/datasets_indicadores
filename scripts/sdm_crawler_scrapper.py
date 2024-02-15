"""
Scrapes the SDM website for the latest data and saves it to a csv file.
It organizes the data in a table format
it uses click to create a command line interface
"""

# import click
import sys
import pandas as pd

# adicionar o path para a poder usar a pasta do projeto
sys.path.append("./")
from utils.sdm_crawler import sdm_crawler
from utils.sdm_parser import main_scrape
from utils.sdm_save import save_csv  # , save_json, save_txt#, big_csv, big_json
from utils.utils import sdm_max


# @click.command()
# @click.option("--begin", default=1, help="Initial ID to start scraping")
# @click.option("--end", default=482, help="Final ID to stop scraping")
def sdm_crawler_and_scrapper(begin=1, end=sdm_max()):
    # create a list of ids to scrape
    # end + 1 because the range function doesn't include the last number
    id_list = [i for i in range(begin, end + 1)]

    # reset sdm_erro.txt
    with open("datasets/indicadores_em_csv/sdm_erro.txt", "w", encoding="utf-8") as f:
        f.write("")

    # iterate over the list of ids
    for each in id_list:
        # scrape the url
        html = sdm_crawler(each)

        # transform the html into a list
        scraped_html = main_scrape(html)

        # if the html is None, save the id in a txt file
        if scraped_html is None:
            print(f"Erro. ID: {each}")
            # save the id that failed in a txt file
            with open(
                "datasets/indicadores_em_csv/sdm_erro.txt", "a", encoding="utf-8"
            ) as f:
                f.write(f"{each}\n")
            continue

        else:
            # save dataframe as csv
            df = pd.DataFrame(scraped_html)
            save_csv(indicador=each, df=df)


if __name__ == "__main__":
    sdm_crawler_and_scrapper()
