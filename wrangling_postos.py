import os
import pandas as pd
import unicodedata
from unicodedata import normalize

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

df = pd.read_csv(f'{caminho_raw}/postos.csv')
# Suponhamos que você tenha um DataFrame chamado df
# Limpeza de Nomes de Colunas
df = df.rename(columns=str.lower)
df = df.rename(columns=lambda x: x.strip().replace(" ", ""))
df.columns
#df = df.apply(lambda col: col.fillna(0) if col.name not in ["codmun_ibge", "data"] else col, axis=0)
df['segmento'] = df['segmento'].fillna('')
df['segmento'] = df['segmento'].apply(limpar_texto)
df.groupby('segmento').count()

segmentos_desejados = ['cooperativa de credito']
df = df[df['segmento'].isin(segmentos_desejados)]
df.describe()
df.info()
df.columns

def left(s):
    return s[:6]

def right(s):
    return s[-17:]
df['arquivo'].head().apply(right).apply(left).apply(int)

df['anomes'] = df['arquivo'].apply(right).apply(left).apply(int)

# Crie um novo DataFrame com as colunas filtradas
#df = df[colunas_filtradas]

df.groupby(['municipioibge','anomes']).agg(contagem = ('municipioibge','size')).reset_index()
df.groupby(['nomeinstituição','segmento','municipioibge','anomes']).agg(contagem = ('municipioibge','size')).reset_index()
