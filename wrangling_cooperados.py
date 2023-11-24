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

df = pd.read_csv(f'{caminho_raw}/cooperados.csv')
