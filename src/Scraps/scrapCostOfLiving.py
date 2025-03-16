import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.3'
    }

    csv_file = '../data/bronze/CostOfLiving_urls.csv'
    df_urls = pd.read_csv(csv_file)
    data = []

    # Limiter aux 5 premières URLs
    for url in df_urls['url']:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an error for bad responses
            soup = BeautifulSoup(response.content, 'html.parser')

            # Récupération du pays
            h1_text = soup.h1.text if soup.h1 else ""
            match = re.search(r'in\s([A-Za-z\s]+)', h1_text)
            pays = match.group(1).strip().replace(' ', '_') if match else "Unknown"

            # Récupération des données de la table
            table = soup.select_one('table.data_wide_table.new_bar_table')
            if table:
                rows = table.select('tr')
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) > 1:
                        data.append([pays, cells[0].text.strip(), cells[1].text.strip()])
        except Exception as e:
            print(f"Error processing URL {url}: {e}")

    # Sauvegarde des données dans un fichier CSV
    res = pd.DataFrame(data, columns=['Pays', 'Item', 'Price'])
    dir_path = '../data/bronze'
    os.makedirs(dir_path, exist_ok=True)
    res.to_csv(os.path.join(dir_path, 'CostOfLiving.csv'), index=False)
    print("Fichier CSV sauvegardé.")
