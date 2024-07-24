import os
import pandas as pd
import re
import time
import random
import requests
from bs4 import BeautifulSoup

caminho_csv = r''
caminho_hd = r''

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Firefox/57.0 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/64.0.3282.140 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/47.0.2526.106 Safari/537.36',
]

def ler_csv(caminho):
    if not os.path.exists(caminho):
        print(f"Arquivo não encontrado: {caminho}")
        return None
    try:
        print(f"Lendo CSV do caminho: {caminho}")
        return pd.read_csv(caminho)
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return None

def limpar_nome_pasta(nome_pasta):
    return "".join(c for c in nome_pasta if c not in "/<>:\"\\|?*")

def baixar_srt(identifier, caminho_download):
    base_url = "https://vfvideos-thumb.nyc3.digitaloceanspaces.com/kraush-unicv/video/"
    srt_url = base_url + f"{identifier}/legenda-ptbr.srt"
    user_agent = random.choice(user_agents)
    headers = {'User-Agent': user_agent}
    
    try:
        response = requests.get(srt_url, headers=headers)
        if response.status_code == 200:
            srt_path = os.path.join(caminho_download, f"{identifier}.srt")
            if os.path.exists(srt_path):
                print(f"SRT já existe: {srt_path}. Pulando download.")
                return False
            with open(srt_path, 'wb') as file:
                file.write(response.content)
            print(f"SRT baixado para {srt_path}")
            return True
        else:
            print(f"SRT não encontrado para {identifier}")
    except Exception as e:
        print(f"Erro ao acessar {srt_url}: {e}")
    return False

def main():
    print("Iniciando o processo...")
    df = ler_csv(caminho_csv)
    if df is not None:
        print("CSV lido com sucesso. Processando títulos...")
        for index, row in df.iterrows():
            nome_pasta = limpar_nome_pasta(row.iloc[0])  # Nome da pasta na coluna A
            caminho_download = os.path.join(caminho_hd, nome_pasta)
            if not os.path.exists(caminho_download):
                print(f"Criando pasta: {caminho_download}")
                os.makedirs(caminho_download)
            
            identifier = row.iloc[1]  # Identifier na coluna B
            if isinstance(identifier, str):
                baixar_srt(identifier, caminho_download)
                time.sleep(0)  # Intervalo de 5 segundos após cada download
    else:
        print("Falha ao ler o CSV.")

if __name__ == "__main__":
    main()
