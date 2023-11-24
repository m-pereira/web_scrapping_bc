import os
import pandas as pd
caminho_raw = os.getcwd()+'/data/raw'

df = pd.read_csv(f'{caminho_raw}/estban.csv')
df.columns
# Suponhamos que você tenha um DataFrame chamado df
# Limpeza de Nomes de Colunas
df = df.rename(columns=str.lower)

# Seleção de Colunas
substrings = ['160','ibge','data','nome','cnpj','161', '162', '163','164','165','166','167','168','169','420','432']

colunas_filtradas = [coluna for coluna in df.columns if any(sub in coluna for sub in substrings)]

# Crie um novo DataFrame com as colunas filtradas
df = df[colunas_filtradas]

# Substituição de Valores Nulos em Colunas Numéricas
df = df.apply(lambda col: col.fillna(0) if col.name not in ["codmun_ibge", "data"] else col, axis=0)
df.columns
# Criação de Novas Colunas
df["operacoes_credito_c_imob"] = df["verbete_160_operacoes_de_credito"]
df["credito_comercial"] = df["verbete_161_empres_e_tit_descontados"] + df["verbete_162_financiamentos"]
df["credito_rural"] = df["verbete_160_operacoes_de_credito"] - df["credito_comercial"] -  df['verbete_169_financiamentos_imobiliarios']
df["captacao"] = df["verbete_432_depositos_a_prazo"] + df["verbete_420_depositos_de_poupanca"]

# Limpeza de Nomes de Colunas Novas
df.columns = df.columns.str.replace("#", "")
df.columns = df.columns.str.replace("base", "")
df.head()

# Manipulação de Datas
df["data_ref"] = pd.to_datetime(df["data_"], format="%Y%m")

# Exibição do DataFrame Resultante
print(df)

df.to_csv(os.path.join("data", "cleaned", "estban.csv"))

