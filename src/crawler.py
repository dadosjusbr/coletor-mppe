import requests
import sys
import os 
import pathlib
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

#Year code - complements - year
folder_url = 'https://transparencia.mppe.mp.br/index.php/contracheque/category/{}-{}-{}'

url_complements = {
    'remu':'remuneracao-de-todos-os-membros-ativos', 
	'vi':  'verbas-indenizatorias-e-outras-remuneracoes-temporarias'
}

#Folder-  code - downloadCode - mes - ano
url_formats = {
	'remu': "{}?download={}:membros-ativos-{}-{}",
	'vi': "{}?download={}:virt-{}-{}"
} 

remu_year_codes = {
	2018: 405,
	2019: 445,
	2020: 504,
	2021: 548
}

vi_year_codes = {
	2018: 415,
	2019: 451,
	2020: 510,
	2021: 555
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
	10:'outubro',
	11:'novembro',
	12:'dezembro'
}

def init_download_codes(year, month):
	download_codes = {}
    
	for key in url_complements:
		if key == 'remu':
			url = folder_url.format(remu_year_codes[int(year)], url_complements[key], year)
		else: 
			url = folder_url.format(vi_year_codes[int(year)], url_complements[key], year)
   
		source_page = urlopen(url).read().decode('utf-8')
		soup = BeautifulSoup(source_page, features= 'lxml')

		#Intera sob as tags de download que contém o download code
		for link in soup.findAll('a', {'class': 'btn btn-success'}):
			if month in link['href']:
				download_codes[key] = re.search('download=(.*):membros', link['href']).group(1)
				break
			elif months[int(month)] in link['href']:
				download_codes[key] = re.search('download=(.*):virt', link['href']).group(1)
				break

	return download_codes
			

def download(url, file_path):
	try:
		response = requests.get(url, allow_redirects=True)
		with open(file_path, "wb") as file:
			file.write(response.content)
			file.close()
	except Exception as excep:
		sys.stderr.write("Não foi possível fazer o download do arquivo: " + file_path + '. O seguinte erro foi gerado: ' + excep )
		os._exit(1)

def crawl(year, month, output_path):
	files = []
	download_codes = init_download_codes(year, month)
 
	for key in url_formats:
		pathlib.Path(output_path).mkdir(exist_ok=True)
		file_name = year + "_" + month + "_" + key + '.xls'
		file_path = output_path + '/' + file_name
		
		if key == "remu":
			base_url = folder_url.format(remu_year_codes[int(year)], url_complements[key], year)
			url = url_formats[key].format(base_url, download_codes[key], month, year)
		else:
			base_url = folder_url.format(vi_year_codes[int(year)], url_complements[key], year)
			if int(year) <= 2019 :
				url = url_formats[key].format(base_url, download_codes[key], months[int(month)], year)

		download(url, file_path)
		files.append(file_path)

	return files