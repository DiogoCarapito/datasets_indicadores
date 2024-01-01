"""
Master script to run the project.
"""

# import toml
import click
from scripts.sdm_scrapper import scrapper

# with open("variaveis.toml", "r", encoding="utf-8") as file:
# config = toml.load(file)

# Accessing a value
# url_contratualizacao = config["url_pdf_contratualizacao"]


@click.command()
@click.option("--begin", default=1, help="Initial ID to start scraping")
@click.option("--end", default=481, help="Final ID to stop scraping")
def main(begin, end):
    scrapper(begin=begin, end=end)
    # scrapper(begin=1, end=476)


# if __name__ == "__main__":
#    cli()
