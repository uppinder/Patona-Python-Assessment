import os
import csv
import string
from urllib import request as Request
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class Scraper:
    def __init__(self) -> None:
        # URL with list of diseases and icons
        self.url = 'https://dermnetnz.org/image-library'

        # Initalize list of uppercase alphabets
        self.alphabets = string.ascii_uppercase

        # Setup Chrome Webdriver
        chrome_options = Options()
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        self.driver = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(), options=chrome_options)

    def load_page(self) -> None:
        # Get URL
        self.driver.get(self.url)

        # Wait until page is loaded
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'imageList')))
        except TimeoutException:
            print('Timed out waiting for page to load.')

    def download_icon(self, img_url: str, disease_starts_with: str, disease_name: str) -> None:
        icons_dir = 'icons/' + disease_starts_with
        if not os.path.isdir(icons_dir):
            os.makedirs(icons_dir)
        icon_file_name = icons_dir + '/' + disease_name + '.jpg'
        opener = Request.build_opener()
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        Request.install_opener(opener)
        Request.urlretrieve(img_url, icon_file_name)

    def scrape(self) -> None:
        self.load_page()

        # Build BeautifulSoup request
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        list_of_diseases = soup.find_all('div', class_='imageList')

        # Write to csv file
        with open('diseases.csv', 'w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(['Disease Name', 'Disease Url', 'Image Url'])
            for disease in list_of_diseases:
                # Gather information about the disease
                disease_starts_with = disease['data-leter']
                disease_information = disease.find_all(
                    'a', class_='imageList__group__item')
                for information in disease_information:
                    disease_name = information.find('h6').text
                    disease_url = 'https://dermnetnz.org' + information['href']
                    img_url = information.find('img')['src']

                    # Write to CSV file
                    csv_writer.writerow([disease_name, disease_url, img_url])

                    # Download Image
                    self.download_icon(
                        img_url, disease_starts_with, disease_name)

    def stop(self) -> None:
        self.driver.quit()


if __name__ == '__main__':
    scraper = Scraper()
    scraper.scrape()
    scraper.stop()
