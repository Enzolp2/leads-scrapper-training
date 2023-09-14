from config import URLS
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_data(soup):
    data = soup.find_all('strong')

    fundacao = []
    funcionarios = []
    endereco = []
    atuacao = []

    for i in data:
        if "Fundação" in i.parent.text:
            fundacao.append(i.parent.text[10:])
        if "Funcionários" in i.parent.text:
            funcionarios.append(i.parent.text[14:])
        if "Endereço" in i.parent.text:
            endereco.append(i.parent.text[10:])
        if "Área de atuação" in i.parent.text:
            atuacao.append(i.parent.text[17:])
    
    # Delete duplciate data
    del fundacao[72]
    del endereco[72]

    return fundacao, funcionarios, endereco, atuacao

def get_customers(soup):
    customers_names = soup.find_all('h2')
    customers = []
    for i in customers_names:
        customers.append(i.text)

    # Deleting front
    for i in range(3):
        del customers[0]
        
    # Deleting back
    for i in range(2):
        del customers[-1]
    
    return customers

def export_csv(customers, fundacao, funcionarios, endereco, atuacao):
    if len(customers) == len(fundacao) == len(funcionarios) == len(endereco) == len(atuacao):
        df = pd.DataFrame({
                'Nome': customers,
                'Data Fundação': fundacao,
                'Média Funcionários': funcionarios,
                'Endereço': endereco,
                'Área Atuação': atuacao
            })
        
        df.to_csv('export/ferramental.csv', index=False)
    else:
        print('> Erro! Dados Possuem tamanhos diferentes')
    

def scrape(url):

    """ Creating Soup Object """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    customers = get_customers(soup)
    fundacao, funcionarios, endereco, atuacao = get_data(soup)
    export_csv(customers, fundacao, funcionarios, endereco, atuacao)



def main():
    url = URLS[0]
    scrape(url)

    print('> Planilha criada com sucesso!')

if __name__ == "__main__":
    main()
 