"""
Master script to run the project.
"""


import click
from scripts.sdm_crawler_scrapper import sdm_crawler_and_scrapper
from scripts.csv_crawler import csv_crawler
from scripts.csv_merge import merge_sdm_ide_idg
from utils.utils import sdm_max

# from scripts.mgfhub_dataset import mgfhub_dataset


@click.command()
@click.option("--begin", default=1, help="Initial ID to start scraping")
@click.option("--end", default=sdm_max(), help="Final ID to stop scraping")
def main(begin=1, end=502):
    print("Starting...")

    # printing the begin and end values
    print(f"Begin: {begin}")
    print(f"End: {end}")

    # run the scrapper
    # goes through all the pages and save the data in a csv file (one csv file per page)
    sdm_crawler_and_scrapper(begin, end)

    # transform each scrapped csv file and join them in one dataframe, saved as csv
    # process it
    csv_crawler()

    # post processing
    merge_sdm_ide_idg()

    # mgfhub_dataset()

    print("Done.")


if __name__ == "__main__":
    main()
