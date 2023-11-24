import os
import pandas as pd
import unicodedata

caminho_raw = os.getcwd()+'/data/raw'

def left(s):
    return s[:6]

def right(s):
    return s[-20:]

def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

def limpar_texto(texto):
    # Remover acentos
    texto_sem_acentos = remover_acentos(texto)
    # Remover espaços iniciais e finais
    texto_sem_espacos = texto_sem_acentos.strip()
    # Converter para minúsculas
    texto_limpo = texto_sem_espacos.lower()
    return texto_limpo

df = pd.read_csv(f'{caminho_raw}/agencias.csv')
# Suponhamos que você tenha um DataFrame chamado df
# Limpeza de Nomes de Colunas
df = df.rename(columns=str.lower)
df = df.rename(columns=lambda x: x.strip().replace(" ", ""))
df.columns
#df = df.apply(lambda col: col.fillna(0) if col.name not in ["codmun_ibge", "data"] else col, axis=0)
df['segmento'] = df['segmento'].fillna('')
df['segmento'] = df['segmento'].apply(limpar_texto)
df.groupby('segmento').count()
segmentos_desejados = ['segmentos_desejados','banco comercial estrangeiro - filial no pais','banco do brasil - banco multiplo', 'banco multiplo','banco multiplo cooperativo','caixa economica federal']
df = df[df['segmento'].isin(segmentos_desejados)]
df.describe()
df.info()
df.columns

def left(s):
    return s[:6]

def right(s):
    return s[-19:]

df['anomes'] = df['arquivo'].apply(right).apply(left).apply(int)

# Crie um novo DataFrame com as colunas filtradas
#df = df[colunas_filtradas]
df["data_inicio"] = pd.to_datetime(df["datainício"], format="%Y%m")

df.groupby(['municipioibge','anomes']).agg(contagem = ('municipioibge','size')).reset_index()
df.groupby(['municipioibge']).max('data_inicio').reset_index()
df.groupby(['nomeinstituição','segmento','municipioibge','anomes']).agg(contagem = ('municipioibge','size')).reset_index()
