import requests
from bs4 import BeautifulSoup
import numpy as np
from datetime import datetime
import csv

class AAVSODataFetcher:
    def __init__(self, star_name, start_date=None, end_date=None, obscode=None, obs_types='vis', num_results=50, pages=2):
        self.base_url = 'https://app.aavso.org/webobs/results/'
        self.star_name = star_name
        self.start_date = start_date
        self.end_date = end_date
        self.obscode = obscode
        self.obs_types = obs_types
        self.num_results = num_results
        self.pages = pages

    def fetch_and_parse_data(self, include_uncertain=False):
        julian_dates = []
        magnitudes = []

        for page in range(1, self.pages + 1):
            params = {
                'star': self.star_name.replace(' ', '+'),
                'num_results': self.num_results,
                'obs_types': self.obs_types,
                'page': page
            }
            if self.obscode:
                params['obscode'] = self.obscode
            if self.start_date:
                params['start'] = self.start_date
            if self.end_date:
                params['end'] = self.end_date

            url = self.base_url + '?' + '&'.join(f'{key}={value}' for key, value in params.items())
            print("Querying URL:", url)

            response = requests.get(url) #packed url
            if response.status_code != 200:
                print("Failed to fetch data from:", url)
                continue

            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', class_='observations')
            if not table:
                print("No table found on page:", page)
                continue
            rows = table.find_all('tr')[1:] #exclude headers
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 8:
                    try:
                        jd = float(cells[2].text.strip())
                        mag_text = cells[4].text.strip()
                        if '<' in mag_text and not include_uncertain:
                            continue
                        if '<' in mag_text:
                            mag_text = mag_text[1:]
                        mag = float(mag_text)
                        julian_dates.append(jd)
                        magnitudes.append(mag)
                    except ValueError as e:
                        print(f"Skipping row due to error: {e}")
                        continue

        return np.array(julian_dates), np.array(magnitudes)


    def save_to_csv(self, julian_dates, magnitudes, filename='data.csv'):
        data = np.column_stack((julian_dates, magnitudes))
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Julian Date', 'Magnitude'])
            writer.writerows(data)
        print(f"Data saved to {filename}")
