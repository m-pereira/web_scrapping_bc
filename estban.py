import os
import requests
from io import BytesIO
from zipfile import ZipFile, BadZipFile
import pandas as pd

# Caminho do diretório que você deseja criar (substitua pelo caminho desejado)
caminho_do_diretorio = os.getcwd()+'/data/zip'
caminho_do_arquivo_parquet = os.getcwd()+'/data/raw'

# Use os.makedirs() para criar o diretório
if not os.path.exists(caminho_do_diretorio):
    os.makedirs(caminho_do_diretorio)
    print("Diretório criado com sucesso.")
else:
    print("O diretório já existe.")


if not os.path.exists(caminho_do_arquivo_parquet):
    os.makedirs(caminho_do_arquivo_parquet)
    print("Diretório criado com sucesso.")
else:
    print("O diretório já existe.")


# Vetor com as partes finais das URLs
ano = 2023
mes = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
partes_finais_url = [f"{ano}{m:02d}_ESTBAN_AG" for m in range(1, 13)]

# Loop sobre as partes finais do URL
for parte_final_url in partes_finais_url:
    # Construa a URL completa
    url = f"https://www.bcb.gov.br/content/estatisticas/estatistica_bancaria_estban/agencia/{parte_final_url}.csv.zip"
    # Combine o diretório temporário com o nome do arquivo zip
    caminho_local = os.path.join(caminho_do_diretorio, f"{parte_final_url}.zip")

    # Use requests para baixar o arquivo zip
    response = requests.get(url)
    with open(caminho_local, 'wb') as f:
        f.write(response.content)

    # Verifique se o download foi bem-sucedido
    if os.path.exists(caminho_local):
        print(f"Download concluído com sucesso. O arquivo está em: {caminho_local}")
    else:
        print("Erro ao baixar o arquivo.")
# Descompacte os arquivos zip

for filename in os.listdir(caminho_do_diretorio):
    if filename.endswith(".zip"):
        zip_path = os.path.join(caminho_do_diretorio, filename)
        try:
            with ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(caminho_do_diretorio)
            print(f'Arquivo ZIP "{filename}" descompactado com sucesso.')
        except BadZipFile:
            print(f'Arquivo ZIP "{filename}" está corrompido. Ignorando.')



# Leia os arquivos CSV e concatene em um único DataFrame
frames = []
for filename in os.listdir(caminho_do_diretorio):
    if filename.endswith(".CSV"):
        file_path = os.path.join(caminho_do_diretorio, filename)
        df = pd.read_csv(file_path, sep=';', skiprows=2, encoding='ISO-8859-1')
        frames.append(df)

# Concatene todos os DataFrames em um único DataFrame
result_df = pd.concat(frames, ignore_index=True)
result_df
# Salve o DataFrame em um arquivo RDS
result_df
result_df.to_pickle(os.path.join("data", "raw", "estban.pkl"))
result_df.to_parquet(os.path.join("data", "raw", "estban.parquet"))
result_df.to_csv(os.path.join("data", "raw", "estban.csv"))

