"""
Master script to run the project.
"""

#import toml
import streamlit as st
import pandas as pd
from scripts.sdm_scrapper import scrapper

#with open("variaveis.toml", "r", encoding="utf-8") as file:
    #config = toml.load(file)

# Accessing a value
#url_contratualizacao = config["url_pdf_contratualizacao"]


def main():
    st.title("SDM Scrapper")
    
    table = scrapper(begin=314, end=314)
    table = pd.DataFrame(table)
    st.table(table)

    #save as csv
    table.to_csv("datasets/indicadores_em_csv/sdm.csv", index=False)

if __name__ == "__main__":
    main()
