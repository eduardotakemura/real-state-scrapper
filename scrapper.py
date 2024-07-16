from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas
import re
import time
import os
import math

class Scrapper:
    def __init__(self):
        # Browser setting #
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        chromedriver_path = r"C:\Users\eduar\Desktop\Folders\Downloads\chromedriver-win64\chromedriver.exe"
        self.service = Service(chromedriver_path)
        self.base_delay = 10

    def get_first_page(self, url):
        try:
            self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
            self.driver.get(url)
            time.sleep(self.base_delay)
            search = self.driver.find_element(By.CLASS_NAME, 'BoxLineClamped_boxLineClamped__w_0Vt')
            total_entries = search.find_element(By.CLASS_NAME, 'CozyTypography').text
            print(total_entries)
            self.driver.quit()
            return total_entries

        except Exception as e:
            print(e)
            self.driver.quit()
            return False

    def extract_id(self,url):
        pattern = r'imovel/(\d+)/'
        match = re.search(pattern, url)
        number_sequence = match.group(1)
        return number_sequence

    def save_to_csv(self, data, file_name):
        file = f"{file_name}.csv"
        df = pandas.DataFrame(data)
        file_exists = os.path.isfile(file)
        df.to_csv(f"scraps/{file}", mode='a', header=not file_exists, index=False)

    def scrap_page(self,url,file_name,entries,fields_config):
        start = time.time()
        # Set the page to Scrap #
        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.driver.get(url)

        # Calculate the number of cycles required #
        cycles = math.ceil(int(entries)/12)

        errors = 0
        houses = []
        seen_cards = set()
        for _ in range(cycles):
            # Wait for the page to load
            time.sleep(self.base_delay)

            # Find all the divs representing houses
            all_cards = self.driver.find_elements(By.CSS_SELECTOR, 'div.Row_row__Sdd0v > div.Column_column__yCK1J')
            new_cards = []

            for card in all_cards:
                try:
                    # Retrieve data from each card #
                    rs_type = card.find_element(By.CSS_SELECTOR, 'h2.Cozy__CardTitle-Metadata').text
                    price = card.find_element(By.CSS_SELECTOR, 'div.Cozy__CardTitle-Title > h3').text
                    condo = card.find_element(By.CSS_SELECTOR, 'div.Cozy__CardTitle-Subtitle > h3').text
                    address = card.find_element(By.CSS_SELECTOR, 'div.Cozy__CardContent-Container > h2').text
                    size = card.find_element(By.CSS_SELECTOR, 'div.Cozy__CardContent-Container > h3').text
                    link = card.find_element(By.CLASS_NAME, 'StyledLink_styledLink__P_6FN').get_attribute('href')

                    # Check if already stored this card #
                    card_id = self.extract_id(link)
                    if card_id not in seen_cards:
                        base_card = {
                            "type": rs_type,
                            "price1": price,
                            "price2": condo,
                            "address": address,
                            "size": size,
                            "link": link,
                        }
                        new_card = {key: value for key, value in base_card.items() if
                                    fields_config.get(key, True)}
                        new_card["card_id"] = card_id
                        new_cards.append(new_card)
                        seen_cards.add(card_id)

                except Exception as e:
                    print(f"Error extracting data from a card: {e}")
                    errors += 1

            if new_cards:
                houses.extend(new_cards)
                self.save_to_csv(new_cards,file_name)
                #print(f"Scraped {len(new_cards)} new items.")

            try:
                show_more = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Ver mais"]')
                show_more.click()
            except Exception as e:
                print(f"No more 'Show more' button or other error: {e}")
                break

        file = pandas.read_csv(f"scraps/{file_name}.csv")
        rows = file.shape[0]
        end = time.time()
        scrap_duration = round((end - start)/60,2)
        print(f"Number of errors: {errors}; Total Entries Scrapped: {rows}; Total Duration: {scrap_duration} minutes;")
        self.driver.quit()
        return errors, rows, scrap_duration

