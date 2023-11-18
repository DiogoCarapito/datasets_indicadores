import toml

with open("variaveis.toml", "r", encoding="utf-8") as file:
    config = toml.load(file)

# Accessing a value
url_contratualizacao = config["url_pdf_contratualizacao"]


def main():
    print(url_contratualizacao)
    return None


if __name__ == "__main__":
    main()
