[![Github Actions Workflow](https://github.com/DiogoCarapito/datasets_indicadores/actions/workflows/main.yaml/badge.svg)](https://github.com/DiogoCarapito/datasets_indicadores/actions/workflows/main.yaml)

# Datasets de Indicadores dos Cuidados Saúde Primários
Um conjunto de datasets úteis no contexto dos Indicadores dos Cuidados de Saúde Primários Portugueses
- Lista de indicadores com intervalo aceitável e esperado (completo)
- Matriz multidimensional das USF e UCSP (em construção)
- Lista de indicadores com imapto no IDG (em construção)
- Scrapping de dados do portal do SNS (em construção)

## Estrutura do repositório
- ```main.py``` - script principal que orquestra todo o processo de ETL
- ```utils/``` - pasta com funções auxiliares
- ```scripts/``` - pasta com scripts de extração de dados. são usados pelo main.py ou podem ser executados individualmente em cli
- ```datasets/``` - pasta com datasets produzidos
- ```datasets/indicadores_em_csv/``` - pasta com os ficheiros .csv com informação sobre todos os indicadores resultantes do processo extração do SDM
- ```tests/``` - pasta com testes unitários
- ```variaveis.toml``` - ficheiro de configuração com variáveis globais (url do PDF da contratualização, paginas com a localização das tabelas, número total de indicadores existentes no SDM)

## TODO
Scripts
- [x] migração de scripts de extração para a pasta scripts/
- [ ] andicionar pre-processamento ao scripts/extracao_indicadores_matrix_multidimensional.py para gerar o ficheiro matrix_multidimensional.csv correto
- [ ] adicionar pre-processamento ao scripts/extracao_indicadores_impacto_idg.py para gerar o ficheiro indicadores_impacto_idg.csv correto
- [x] completar o posprocessamento do script sdm_scrapper.py
- [ ] script para confirmar se novos indicadores foram adicionados ao SDM e actualizar o variaveis.toml

- [ ] script para extrarir metainformação do SDM

Test
- [ ] gerar testes unitários (coverage actual 8%)
    - [ ] utils/
        - [ ] sdm_parser.py
        - [ ] sdm_scrapper.py
        - [ ] pdf_tools.py
    - [ ] scripts/
        - [ ] extracao_indicadores_matrix_multidimensional.py
        - [ ] extracao_indicadores_impacto_idg.py
        - [ ] extracao_indicadores_intervalos.py
        - [ ] sdm_scrapper.py
    - [ ] main.py

main.py
- [ ] orquestrar todo o processo de ETL na funcção main.py
- [ ] produzir os seguintes datasets com a função main.py
    - [ ] .csv com todos indicadores, com intervalo aceitável e esperado, sem tem impacto no IDG ou não
    - [ ] .csv com apenas indicadores com impacto no IDG, com intervalo aceitável e esperado, com peso com base no impacto no IDG (teórico e contratualizado)
    - [ ] pasta com o .txt para cada indicador com o texto vindos do SDM

## cheat sheet
### venv
create venv
```bash
python3 -m venv .venv
```

activate venv
```bash
source .venv/bin/activate
```