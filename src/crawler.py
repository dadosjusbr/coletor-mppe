import requests
import sys
import os 
import pathlib

url_formats = {
    'remu': "https://transparencia.mppe.mp.br/index.php/contracheque/category/{}-remuneracao-de-todos-os-membros-ativos-{}?download=4784:membros-ativos-{}-{}"
    } 

year_codes = {
	2018: 405,
	2019: 445,
	2020: 504
}
 
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
	
	for key in url_formats:
		pathlib.Path(output_path).mkdir(exist_ok=True)
		file_name = year + "_" + month + "_" + key + '.xlsx'
		file_path = output_path + '/' + file_name 
		url = url_formats[key].format(year_codes[int(year)], year, month, year)
		download(url, file_path)

		files.append(file_path)

	return files