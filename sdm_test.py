import requests
from utils.sdm_parser import initial_parse, main_parse

html_inicio = "https://sdm.min-saude.pt/BI.aspx?id="
html_fim = "&CLUSTERS=S"

# create a lisft from 1 to 448
list_ids = [i for i in range(70, 100)]
#list_ids = [39]


for html_code in list_ids:
    # compose the url
    html = html_inicio + str(html_code) + html_fim

    try:
        rqst = requests.get(html, timeout=12)
        # status_codes[html_code] = rqst.status_code

        parsed_html = initial_parse(rqst.content)

        if parsed_html[3][:4] == "Erro":
            print(f"Erro no BI indicador {html_code}")
            continue
        # print the first 100 in the list
        # for each in parsed_html[:100]:
        #    print(each)
        for key, value in main_parse(parsed_html).items():
            print(key, value)

    except requests.exceptions.Timeout:
        print(f"Request for {html_code} timed out")
        #break
        pass
