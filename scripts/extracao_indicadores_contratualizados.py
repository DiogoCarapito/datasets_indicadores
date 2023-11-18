"""
Script para extrair informação sobre indicadores do documento Operacionalização da Contratualização nos Cuidados de Saúde Primários para 2023
CONTRATUALIZAÇÃO DAS USF E UCSP - INDICADORES ASSOCIADOS ÀS DIMENSÕES DA MATRIZ MULTIDIMENSIONAL COM IMPACTO NO CÁLCULO DO IDG (2023)
"""


import sys

# adicionar o path para a poder usar a pasta utils
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
        config["pagina_inicial_MATRIZ_MULTIDIMENSIONAL"],
        config["pagina_final_MATRIZ_MULTIDIMENSIONAL"],
    )

    # paginas a extrair em formato string para o tabula
    paginas = f"{pagina_inicial}-{pagina_final}"

    # extrair as tabelas do documento pdf atravez do url
    df = download_and_extract_table(url, paginas)

    # Processar o dataframe

    # gravar o dataframe em csv
    df.to_csv("./datasets/matriz_multidimensional_usf_e_ucsp.csv", index=False)

    # success message
    print("Matriz Multidimensional USF e UCSP extraida com sucesso!")

    return df


if __name__ == "__main__":
    main()
