import os
from bs4 import BeautifulSoup as bs
import requests
import datetime

def get_excel_file(source_url, output_directory):

    soup = bs(requests.get(source_url).text, 'lxml').find_all("div", {"class": "sc-fzoJMP"})[0]

    soup_file = soup.find('a')['href']
    soup_name = soup.find("span", {"class": "file-title"}).text

    file_name_complete_path = os.path.join(output_directory, soup_name.replace(" ", "_").replace("/", ""))

    with open (file_name_complete_path, 'wb') as file:
        response = requests.get(soup_file)
        file.write(response.content)

if __name__ == "__main__":

    BFI_SPREADSHEET_URL = 'https://www.bfi.org.uk/industry-data-insights/weekend-box-office-figures'
    OUTPUT_DIRECTORY = '/home/edmundludlow/UKBOA_Website/bfi_spreadsheets_store/spreadsheet_holding_space'

    today = datetime.date.today()
    weekday = today.weekday()

    if (weekday == 3):
        get_excel_file(BFI_SPREADSHEET_URL, OUTPUT_DIRECTORY)
        print("complete")