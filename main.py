"""
Master script to run the project.
"""

# import toml
from scripts.sdm_scrapper import scrapper

# with open("variaveis.toml", "r", encoding="utf-8") as file:
# config = toml.load(file)

# Accessing a value
# url_contratualizacao = config["url_pdf_contratualizacao"]


def main():
    scrapper(begin=1, end=476)


if __name__ == "__main__":
    main()
