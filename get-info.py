import pandas as pd
from config import CSV_DIR
import os
import requests
from bs4 import BeautifulSoup
from googleapi import google

CSV_FILES = [CSV_DIR+'/'+file for file in os.listdir(CSV_DIR)]

def google_search(company):
    """ Return phone number of the company """

    search_url = f"https://www.google.com/search?q={company}"
    try:
        response = requests.get(search_url)
        if response.status_code >= 200 and response.status_code < 300:
            soup = BeautifulSoup(response.text, 'html.parser')
            with open('output.html', 'w', encoding='utf-8') as file:
                file.write(soup.prettify())
            phone_number = soup.find('div', {'class': 'AVsepf u2x1Od'}).find('span', {'class': 'BNeawe tAd8D AP7Wnd'})
        else:
            print('>> Status Code error', response.status_code)
            return 'None'
    except Exception as e:
        print('>> Request error', e)
        return 'None'

    return phone_number.text.strip()

def export_csv(nomes, telefones):

    df = pd.DataFrame({
        'Nome': nomes,
        'Telefones': telefones
    })
    try:
        df.to_csv('export/phone-number.csv', index=False)
        return True
    except Exception as e:
        print('> Erro ao exportar planilha', e)

def main():
    print('> Init Collect Phone Number')
    print('> DATABASES:', CSV_FILES)

    """ Join CSV Databases """
    files = []
    for file in CSV_FILES:
        files.append(pd.read_csv(file)['Nome'])
    customers_df = pd.concat(files, ignore_index=True)
    
    """ Searching Phone Number """
    phone_numbers = []
    customers = []
    i = 1
    for customer in customers_df:
        print(f'{i}/{len(customers_df)}')
        phone_number = google_search(customer)
        if phone_number == 'None':
            phone_numbers.append('-')
        else:
            phone_numbers.append(phone_number)
        customers.append(customer)
        i += 1
    
    """ Exporting to CSV File """
    if export_csv(customers, phone_numbers):
        print('> Planilha exportada com sucesso!')


if __name__ == "__main__":
    main()