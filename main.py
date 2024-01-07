"""
Master script to run the project.
"""

import toml
import click
from scripts.sdm_scrapper import scrapper
from scripts.sdm_csv_crawler import csv_crawler


# get the max id to scrape from the config file
def sdm_max():
    with open("variaveis.toml", "r", encoding="utf-8") as file:
        config = toml.load(file)
    return config["sdm_indicador_final"]


# main function
@click.command()
@click.option("--begin", default=1, help="Initial ID to start scraping")
@click.option("--end", default=sdm_max(), help="Final ID to stop scraping")
def main(begin=1, end=481):
    print(f"Begin: {begin}")
    print(f"End: {end}")

    print("Starting...")

    # run the scrapper
    scrapper(begin, end)

    # run the csv crawler
    csv_crawler()

    print("Done.")


if __name__ == "__main__":
    main()
