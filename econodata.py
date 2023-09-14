from config import URLS
import requests
from bs4 import BeautifulSoup
import pandas as pd

def open_page():
    with open('500 Maiores Empresas de Ferramentaria no Brasil.html', 'r', encoding='utf-8') as arquivo_html:
        conteudo_html = arquivo_html.read()
    return conteudo_html

def create_soupObject_by_url(url):
    """
    A função create_soupObject_by_url é responsável por criar
    um objeto BeautifulSoup a partir do conteúdo de uma URL fornecida.
    Este objeto BeautifulSoup pode ser usado para analisar e extrair
    informações de páginas da web em HTML.
    """
    try:
        response = requests.get(url)
    except Exception as e:
        print('> Erro na requisição', e)
        return None
    if response.status_code >= 200 and response.status_code < 300:
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print('> Erro na função create_soupObject_by_url', e)
    else:
        print('> Erro no status_code')

    return soup

def create_soupObject_by_source(source):
    try:
        soup = BeautifulSoup(source, 'html.parser')
    except Exception as e:
        print('> Erro na função create_soupObject_by_url', e)
    return soup

def scrape(url='', source=None):
    
    if url == '' and source is None:
        return None
    elif url == '':
        soup = create_soupObject_by_source(source)
    elif source is None:
        soup = create_soupObject_by_url(url)

    if soup is not None:
        nomes = []
        datas = []
        funcionarios = []
        enderecos = []
        area_atuacao = []

        # Getting links for scrapping with index
        for i in range(1, 501):
            row_element = soup.find('tr', {'aria-rowindex': i})

            nomes.append(row_element.find('a', {'class': 'link-text'}).text.strip())
            address_1 = row_element.find('div', {'class': 'table-font-small table-cell-endereco'}).text.strip()
            address_2 = row_element.find('div', {'class': 'table-font-big table-cell-endereco'}).text.strip()
            enderecos.append(address_1 + ' - ' + address_2)
            area_atuacao.append(soup.find('div', {'class': 'table-font-small table-cell-endereco mt-1'}).text.strip())
            
        try:
            export_csv(nomes, ['-' for i in nomes], ['-' for i in nomes], enderecos, area_atuacao)
            print('> Planilha exportada com sucesso.')
        except Exception as e:
            print('> Erro ao exportar para csv...', e)
        
    else:
        print('> Não foi possível criar o objeto BeautifulSoup principal')

def export_csv(nomes, datas, funcionarios, enderecos, atuacao):

    df = pd.DataFrame({
        'Nome': nomes,
        'Data Fundação': datas,
        'Média Funcionários': funcionarios,
        'Endereço': enderecos,
        'Área Atuação': atuacao
    })
    df.to_csv('export/econodata.csv', index=False)
 

def main():
    print('> Iniciando coleta de dados...')

    conteudo_html = open_page()
    scrape(source=conteudo_html)


    print('> Coleta de dados finalizada.')

if __name__ == "__main__":
    main()  