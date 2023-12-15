import sys
import toml
import streamlit as st

# adicionar o path para a poder usar a pasta do projeto
sys.path.append("./")

from utils.pdf_tools import download_and_extract_table, process_portaria_411a_2023


def main():
    # abrir o ficheiro de configuração com as variaveis
    with open("./variaveis.toml", "r", encoding="utf-8") as file:
        config = toml.load(file)

    # url
    url = config["url_portaria_411a_2023"]

    # paginas a extrair
    pagina_inicial, pagina_final = (
        config["pagina_inicial_portaria_411a_2023"],
        config["pagina_final_portaria_411a_2023"],
    )

    # paginas a extrair em formato string para o tabula
    paginas = f"{pagina_inicial}-{pagina_final}"

    # extrair as tabelas
    df = download_and_extract_table(url, paginas)

    df_processed = process_portaria_411a_2023(df)

    #save the dataframe as csv in datasets folder
    df_processed.to_csv("./datasets/portaria_411a_2023.csv", index=False)
    
    st.set_page_config(
        page_title="Portaria 411-A/2023", page_icon=":memo:", layout="wide"
    )
    
    st.title("Portaria 411-A/2023")
    
    col_1, col_2 = st.columns(2)
    with col_1:
        st.table(df)

    with col_2:
        st.table(df_processed)

if __name__ == "__main__":
    main()
