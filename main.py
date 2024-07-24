import os
import pandas as pd
import yt_dlp
import re
import time
import random
import string

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

def link_valido(link):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, link) is not None

def extrair_nome_video(url):
    partes = url.split('/')
    nome_arquivo = partes[-2]
    return nome_arquivo

def baixar_arquivo(url, caminho, formato):
    user_agent = random.choice(user_agents)
    nome_arquivo = extrair_nome_video(url)
    temp_output = os.path.join(caminho, f'{nome_arquivo}.%(ext)s')
    ydl_opts = {
        'format': 'bestaudio/best' if formato == 'mp3' else 'best',
        'outtmpl': temp_output,
        'quiet': True,
        'noprogress': True, 
        'nooverwrites': False, 
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}] if formato == 'mp3' else [],
        'http_headers': {
            'User-Agent': user_agent,
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1', 
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=True)
            arquivo_baixado = ydl.prepare_filename(result)
            final_output = os.path.join(caminho, f"{nome_arquivo}.{formato}")
            os.rename(arquivo_baixado, final_output)
            return final_output
    except Exception as e:
        print(f"Erro ao baixar {formato} de {url}: {e}")
        return None

def limpar_nome_pasta(nome_pasta):
    return "".join(c for c in nome_pasta if c not in "/<>:\"\\|?*")

def processar_link(link, caminho_download):
    nome_video = extrair_nome_video(link)
    if link.endswith('.mp3'):
        formato = 'mp3'
    else:
        formato = 'mp4'
    
    final_output = os.path.join(caminho_download, f"{nome_video}.{formato}")
    if os.path.exists(final_output):
        print(f"Arquivo já existe: {final_output}. Pulando download.")
        return False

    tentativas = 0
    max_tentativas = 5
    tempo_espera = 60  

    while tentativas < max_tentativas:
        try:
            print(f"Processando link para {formato}: {link}")
            arquivo_baixado = baixar_arquivo(link, caminho_download, formato)
            if arquivo_baixado:
                print(f"Baixado no caminho: {arquivo_baixado}")
                return True
        except Exception as e:
            print(f"Erro ao processar {link} ({formato}): {e}")
            tentativas += 1
            print(f"Erro. Aguardando {tempo_espera} segundos antes de tentar novamente... (Tentativa {tentativas}/{max_tentativas})")
            time.sleep(tempo_espera)
            tempo_espera *= 2  
    print(f"Falha ao baixar {link} ({formato}) após várias tentativas.")
    return False

def main():
    print("Iniciando o processo...")
    df = ler_csv(caminho_csv)
    if df is not None:
        print("CSV lido com sucesso. Processando links...")
        for index, row in df.iterrows():
            nome_pasta = limpar_nome_pasta(row.iloc[0])
            caminho_download = os.path.join(caminho_hd, nome_pasta)
            if not os.path.exists(caminho_download):
                print(f"Criando pasta: {caminho_download}")
                os.makedirs(caminho_download)
            for item in row:
                if isinstance(item, str) and link_valido(item):
                    download_feito = processar_link(item, caminho_download)
                    if download_feito:
                        time.sleep(30)  # Mantendo o intervalo de 30 segundos após cada download
    else:
        print("Falha ao ler o CSV.")

if __name__ == "__main__":
    main()
