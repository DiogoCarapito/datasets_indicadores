"""
Script para extrair informação sobre indicadores do documento Operacionalização da Contratualização nos Cuidados de Saúde Primários para 2023
MATRIZ MULTIDIMENSIONAL DAS USF E UCSP (paginas 13-15)
"""

import sys

# adicionar o path para a poder usar a pasta do projeto
sys.path.append("./")

from utils.pdf_tools import download_and_extract_table
import toml


def main():
    # ir buscar o url do pdf ao ficheiro de configuração com as variaveis
    with open("./variaveis.toml", "r", encoding="utf-8") as file:
        config = toml.load(file)

    # url
    url = config["url_pdf_contratualizacao"]

    # paginas a extrair
    pagina_inicial, pagina_final = (
        config["pagina_inicial_INDICADORES_IDG"],
        config["pagina_final_INDICADORES_IDG"],
    )

    # paginas a extrair em formato string para o tabula
    paginas = f"{pagina_inicial}-{pagina_final}"

    # extrair as tabelas do documento pdf atravez do url
    df = download_and_extract_table(url, paginas)

    # Processar o dataframe

    # gravar o dataframe em csv
    df.to_csv("./datasets/indicadores_impacto_idg.csv", index=False)

    # success message
    print("Indicadores com impacto no IDG extraidos com sucesso!")

    return df


if __name__ == "__main__":
    main()
