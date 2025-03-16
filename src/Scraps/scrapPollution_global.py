import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.3'
    }

    csv_file = '../../data/bronze/Pollution_urls.csv'
    df_urls = pd.read_csv(csv_file)
    # df_urls = ['https://www.numbeo.com/pollution/country_result.jsp?country=Cambodia']
    data = []

    for url in df_urls['url']:
    # for url in df_urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an error for bad responses
            soup = BeautifulSoup(response.content, 'html.parser')

            # Récupération du pays
            h1_text = soup.h1.text if soup.h1 else ""
            match = re.search(r'in\s([A-Za-z\s]+)', h1_text)
            pays = match.group(1).strip().replace(' ', '_') if match else "Unknown"
            print(f"Processing {pays}...")
            # Récupération des données de la table
            table = soup.select_one('table.table_indices')
            if table:
                rows = table.select('tr')
                indice = []
                for x in [1, 2]:
                    cells = rows[x].find_all('td')
                    indice.append(cells[1].text.strip())
                if len(indice) > 1:
                    data.append([pays, indice[0], indice[1]])
        except Exception as e:
            print(f"Error processing URL {url}: {e}")

    
    # Sauvegarde des données dans un fichier CSV
    dir_path = '../../data/bronze'
    os.makedirs(dir_path, exist_ok=True)

    res = pd.DataFrame(data, columns=['Country', 'Pollution_index','Pollution_index_Exp'])
    res.to_csv(os.path.join(dir_path, 'Pollution_global.csv'), index=False)
    print("Fichier CSV sauvegardé.")
