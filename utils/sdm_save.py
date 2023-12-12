import os
import pandas as pd

# import toml


def save_csv(indicador, df):
    # save as csv wiht utf-8 encoding
    df.to_csv(f"datasets/indicadores_em_csv/sdm_{indicador}.csv", index=False)
    print(f"{indicador} .csv saved!")


def save_json(indicador, df):
    # save as json wiht utf-8 encoding

    # set the index to the header column
    df.set_index("titulo", inplace=True)

    # rename the text column to the indicador
    df.rename(columns={"texto": indicador}, inplace=True)

    # save as json
    df.to_json(f"datasets/indicadores_em_json/sdm_{indicador}.json", force_ascii=False)
    print(f"{indicador} .json saved!")


def save_txt(indicador, df):
    # remove previous txt files
    if os.path.exists(f"datasets/indicadores_em_txt/sdm_{indicador}.txt"):
        os.remove(f"datasets/indicadores_em_txt/sdm_{indicador}.txt")

    # save as txt wiht utf-8 encoding
    for header, text in df.itertuples(index=True):
        with open(
            f"datasets/indicadores_em_txt/sdm_{indicador}.txt", "a", encoding="utf-8"
        ) as f:
            f.write(f"{header}\n{text}\n\n")
    print(f"{indicador} .txt saved!")


def big_csv():
    # save all small csv files into one big csv file
    # the csv files are saved in the datasets/indicadores_em_csv folder
    # the big csv file is saved in the datasets folder

    # create a list of all the csv files in the folder, it should end with .csv and exclude everything else
    csv_list = [
        each
        for each in os.listdir("datasets/indicadores_em_csv")
        if each.endswith(".csv")
    ]
    print(csv_list[30:40])

    # create an empty dataframe
    df = pd.DataFrame()

    # iterate over the list of csv files
    for each in csv_list[30:40]:
        # read the csv file
        csv = pd.read_csv(f"datasets/indicadores_em_csv/{each}")

        print(each)

        # transpose the csv file
        csv = csv.T

        # set the first row as the header
        csv.columns = csv.iloc[0]

        # remove the first row
        csv = csv.iloc[1:]

        # set the index to the ID column
        csv.set_index("ID", inplace=True)

        # print(csv)

        # Append the csv file to the dataframe
        df = pd.concat([df, csv], ignore_index=True)

    # sort df by the ID column
    # df.sort_values(by=['ID'], inplace=True)

    # save the dataframe as csv
    df.to_csv("datasets/sdm.csv", index=False)

    print("big csv saved!")


def big_json():
    # save all small json files into one big csv file
    # the json files are saved in the datasets/indicadores_em_csv folder
    # the big json file is saved in the datasets folder

    # create a list of all the json files in the folder
    json_list = os.listdir("datasets/indicadores_em_json")

    # create an empty dataframe
    df = pd.DataFrame()

    # iterate over the list of json files
    for each in json_list:
        # read the json file
        json = pd.read_json(f"datasets/indicadores_em_json/{each}")

        # append the json file to the dataframe
        df = df.append(json)

    # save the dataframe as json
    df.to_json("datasets/sdm.json", force_ascii=False)

    print("big json saved!")
