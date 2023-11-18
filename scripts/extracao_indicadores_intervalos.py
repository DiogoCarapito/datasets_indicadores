"""
Script para extrair informação sobre indicadores do documento Operacionalização da Contratualização nos Cuidados de Saúde Primários para 2023
ANEXO XVI – INDICADORES: INTERVALOS ESPERADOS E VARIAÇÃO ACEITÁVEL (paginas 74-78)
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
        config["pagina_inicial_INTERVALOS_INDICADORES"],
        config["pagina_final_INTERVALOS_INDICADORES"],
    )

    # paginas a extrair em formato string para o tabula
    paginas = f"{pagina_inicial}-{pagina_final}"

    # extrair as tabelas do documento pdf atravez do url
    df = download_and_extract_table(url, paginas)

    # PROCESSAR O DATAFRAME
    # remover as linhas cuja coluna ID Indicador é <NA>
    df = df[df["ID Indicador"].notna()]

    # reset index
    df = df.reset_index(drop=True)

    # tornar ID Indicador em int
    df["ID Indicador"] = df["ID Indicador"].astype(int)

    # renomear colunas do dataframe
    df = df.rename(
        columns={
            "ID Indicador": "id_indicador",
            "Nome Indicador": "nome_indicador",
            "Int var.": "intervalo_aceitavel",
            "Int. Esperado": "intervalo_esperado",
        }
    )

    # criar 4 novas colunas com os valores dos intervalos esperados e aceitaveis
    # remover os parentises retos das colunas min_esperado, max_esperado, min_aceitavel e max_aceitavel
    # transformar os valores em float

    # Esperado
    df[["min_esperado", "max_esperado"]] = df["intervalo_esperado"].str.split(
        ";", expand=True
    )
    df["min_esperado"] = df["min_esperado"].str.replace("[", "").astype(float)
    df["max_esperado"] = df["max_esperado"].str.replace("]", "").astype(float)

    # Aceitável
    df[["min_aceitavel", "max_aceitavel"]] = df["intervalo_aceitavel"].str.split(
        ";", expand=True
    )
    df["min_aceitavel"] = df["min_aceitavel"].str.replace("[", "").astype(float)
    df["max_aceitavel"] = df["max_aceitavel"].str.replace("]", "").astype(float)

    # gravar o dataframe em csv
    df.to_csv("datasets/indicadores_intervalos_esperados_aceitaveis.csv", index=False)

    # success message
    print("Intervalos esperados e aceitaveis extraidos com sucesso!")

    return df


if __name__ == "__main__":
    main()
