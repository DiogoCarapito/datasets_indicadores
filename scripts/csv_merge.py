import pandas as pd


def merge_sdm_ide_idg():
    # Read in the data
    df_sdm = pd.read_csv("datasets/indicadores_sdm.csv")

    df_ide = pd.read_csv("datasets/indicadores_ide.csv", header=None)
    df_ide = df_ide[0].to_list()

    # df_portaria = pd.read_csv("datasets/portaria_411a_2023.csv")

    df_idg = pd.read_csv("datasets/indicadores_idg.csv", header=None)
    df_idg = df_idg[0].to_list()
    # sdm is the main dataframe i want to overwrite at the end
    # i want to create a column where if the same id is found in the df_ide, the value is 1
    # if not, the value is 0

    # create a new column in df_sdm

    # print(df_ide)

    # iterate over the rows of df_sdm
    for index, row in df_sdm.iterrows():
        # check if the id is in df_ide
        if row["id"] in df_ide:
            # if it is, change the value of the ide column to 1
            print(row["id"])
            df_sdm.loc[index, "ide"] = 1

    print(df_sdm[df_sdm["ide"] == 1].shape[0])

    # do the same for the idg column
    # df_sdm["idg"] = 0

    for index, row in df_sdm.iterrows():
        if row["id"] in df_idg:
            df_sdm.loc[index, "idg"] = 1

    print(df_sdm[df_sdm["idg"] == 1].shape[0])

    # save the dataframe
    df_sdm.to_csv("datasets/indicadores_sdm_complete.csv", index=False)


if __name__ == "__main__":
    merge_sdm_ide_idg()
