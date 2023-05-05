import sys
import os
import pathlib
import requests

import re
from bs4 import BeautifulSoup
from urllib.request import urlopen


# Url base refente ao  direntório que contém as planilhas: year_code - url_complement - key
folder_url = 'https://transparencia.mppe.mp.br/index.php/contracheque/category/{}-{}-{}'

# Complementos para folder_url
url_complements = {
    "contracheque": 'remuneracao-de-todos-os-membros-ativos',
    "verbas-indenizatorias":  'verbas-indenizatorias-e-outras-remuneracoes-temporarias'
}

# Formato de envio da requisição: folder_url - download_code - month - year
url_formats = {
    "contracheque": "{}?download={}:membros-ativos-{}-{}",
    "verbas-indenizatorias": "{}?download={}:virt-{}-{}"
}

# Todos os anos possuem um código associado para remunerações simples variando ano-a-ano
remu_year_codes = {
    2018: 405,
    2019: 445,
    2020: 504,
    2021: 548,
    2022: 623,
    2023: 714
}

# Todos os anos possuem um código associado para verbas indenizatórias variando ano-a-ano
vi_year_codes = {
    2018: 415,
    2019: 451,
    2020: 510,
    2021: 555,
    2022: 629,
    2023: 721
}

# Verbas indenizatórias referentes á 2018 e 2019 recebem o nome do mẽs como parâmetro
months = {
    1: 'janeiro',
    2: 'fevereiro',
    3: 'marco',
    4: 'abril',
    5: 'maio',
    6: 'junho',
    7: 'julho',
    8: 'agosto',
    9: 'setembro',
    10: 'outubro',
    11: 'novembro',
    12: 'dezembro'
}

# Retorna um dicionário com códigos que compõe as urls relativa ao mês em questão para remunerações simples e vi.


def download_codes(year, month):
    download_codes = {}

    for key in url_complements:

        if key == "contracheque":
            url = folder_url.format(
                remu_year_codes[int(year)], url_complements[key], year)
        else:
            url = folder_url.format(
                vi_year_codes[int(year)], url_complements[key], year)

        source_page = urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(source_page, features='lxml')

        # Intera sob as tags de download que contém o download code
        for link in soup.findAll('a', {'class': 'btn btn-success'}):
            # Remunerações contém no link o numero do mês
            if key == "contracheque":
                target = '-' + month + '-' + year
                if target in link['href']:
                    download_codes[key] = re.search(
                        'download=(.*):membros', link['href']).group(1)
                    break
            else:
                # Verbas indenizatórias para meses anteriores ou iguais a 2019 contém o nome do Mês
                if int(year) <= 2019:
                    if months[int(month)] in link['href']:
                        download_codes[key] = re.search(
                            'download=(.*):virt', link['href']).group(1)
                        break
                else:
                    # Caso de busca especifico para verbas indenizatórias para meses posteriores ou iguais á 2020
                    target = month + year
                    if target in link['href']:
                        download_codes[key] = re.search(
                            'download=(.*):indeniz', link['href']).group(1)
                        break

    return download_codes


def download(url, file_path):
    try:
        # headers = {
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        #     "Accept-Encoding": "gzip, deflate, br",
        #     "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        #     "Connection": "keep-alive",
        #     "Cookie": "_ga=GA1.1.1330144668.1676574013; flagcontraste=null; 0462c4abb8339dfd7189f3f9af521737=7ae96d441e0bad694b1152e71dc8c208; _ga_23M5320ZK9=GS1.1.1683223486.8.1.1683223494.0.0.0",
        #     "Host": "transparencia.mppe.mp.br",
        #     "Referer": url,
        #     "sec-ch-ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        #     "sec-ch-ua-mobile": "?0",
        #     "sec-ch-ua-platform": "Linux",
        #     "Sec-Fetch-Dest": "document",
        #     "Sec-Fetch-Mode": "navigate",
        #     "Sec-Fetch-Site": "same-origin",
        #     "Sec-Fetch-User": "?1",
        #     "Upgrade-Insecure-Requests": "1",
        #     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        # }

        proxies = {
            "https": "35.198.45.239:3129",
        }
        response = requests.get(url, allow_redirects=True, proxies=proxies)
        with open(file_path, "wb") as file:
            file.write(response.content)
            file.close()
    except Exception as excep:
        sys.stderr.write("Não foi possível fazer o download do arquivo: " +
                         file_path + '. O seguinte erro foi gerado: ' + excep)
        os._exit(1)


def crawl(year, month, output_path):
    files = []
    codes = download_codes(year, month)
    try:
        for key in url_formats:
            pathlib.Path(output_path).mkdir(exist_ok=True)
            file_name = "membros-ativos-" + key + "-" + month + "-" + year + '.xlsx'
            file_path = output_path + '/' + file_name

            if key == "contracheque":
                base_url = folder_url.format(
                    remu_year_codes[int(year)], url_complements[key], year)
                url = url_formats[key].format(
                    base_url, codes[key], month, year)
            else:
                base_url = folder_url.format(
                    vi_year_codes[int(year)], url_complements[key], year)
                if int(year) <= 2019:
                    url = url_formats[key].format(
                        base_url, codes[key], months[int(month)], year)

                # Para anos posteriores à 2019 a url para download de verbas indenizatórias segue o formato
                else:
                    url = base_url + \
                        '?download={}:indeniz{}{}'.format(
                            codes[key], month, year)

            download(url, file_path)
            files.append(file_path)
    except:
        sys.stderr.write(f"Não existe planilha para {month}/{year}")
        sys.exit(4)

    return files
