import requests
from utils.sdm_parser import initial_parse, stop_at_bi, header_location_dictionary
import pandas as pd


def scrape_to_txt():
    # html
    html_inicio = "https://sdm.min-saude.pt/BI.aspx?id="
    html_fim = "&CLUSTERS=S"

    # create a lisft from 1 to 448
    list_ids = [i for i in range(1, 5)]

    # dataframe
    df = pd.DataFrame()

    for html_code in list_ids:
        # compose the url
        html = html_inicio + str(html_code) + html_fim

        try:
            # request the url
            rqst = requests.get(html, timeout=30)
            # status_codes[html_code] = rqst.status_code

            # parse the html into a list of strings
            parsed_html = initial_parse(rqst.content)

            # remove all the items in the list that comes after the first "BI" string if it exists
            parsed_html = stop_at_bi(parsed_html)

            # create a dictionary with the header location, so the text can be concatenated between the headers
            header_location = header_location_dictionary(parsed_html)

            print(header_location)

            # create a txt file where each line is an item in the list
            # with open(f"sdm/indicador_{html_code}.txt", "w", encoding="utf-8") as file:
            # write the url in the first line
            #    file.write(html + "\n")

            # iterate over the list and write each item in a line
            #    for item in parsed_html:
            #        file.write(item + "\n")

            # success message
            print(f"{html_code} Scraped!")

        # exception if the request times out
        except requests.exceptions.Timeout:
            print(f"Request for {html_code} timed out")

            # record in a folder the html code that timed out
            with open("sdm/timeout.csv", "a", encoding="utf-8") as file:
                file.write(f"Time out\n{html_code}\n")

        # save the dataframe to a csv file
        df.to_csv("sdm/header_location.csv", index=False)


if __name__ == "__main__":
    scrape_to_txt()
