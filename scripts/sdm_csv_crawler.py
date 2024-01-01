import pandas as pd
import os


# get the list of files in the folder to create a loop that opnes and saves in a dataframe
directory = "./datasets/indicadores_em_csv/"

csv_files = [f for f in os.listdir(directory) if f.endswith(".csv")]

csv_files.sort()

# print(csv_files)

# new dataframe to save all the data
df = pd.DataFrame()

# for loop to open each csv file and save it in the dataframe
for file in csv_files:
    # construct full file path
    file_path = os.path.join(directory, file)

    # read the CSV file into a DataFrame
    temp_df = pd.read_csv(file_path)

    # make the first column the index
    temp_df.set_index(temp_df.columns[0], inplace=True)

    # transpose the DataFrame
    temp_df = temp_df.T

    try:
        # make ID the index
        temp_df.set_index("Código", inplace=True)

        # append the temp_df DataFrame to the main df DataFrame
        df = pd.concat([df, temp_df], ignore_index=False, join="outer")
    except KeyError:
        print(f"Erro. ID: {file}")


# sort the columns by ID column
df.set_index("ID", inplace=True)
df.sort_values("ID", inplace=True)


# save the dataframe as csv in datasets folder
df.to_csv("./datasets/indicadores_sdm.csv", index=True)
