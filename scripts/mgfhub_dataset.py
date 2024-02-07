import pandas as pd


def mgfhub_dataset():
    # load the csv file datasets/indicadores_sdm_complete.csv
    df = pd.read_csv("./datasets/indicadores_sdm_complete.csv")

    # drop columns

    # show columns
    print(df["Intervalo Aceitável"].unique())


if __name__ == "__main__":
    mgfhub_dataset()
