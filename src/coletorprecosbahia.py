from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import time


class ColetorPrecosBahia:
    def __init__(self):
        options = webdriver.ChromeOptions()
        self.url = "https://precodahora.ba.gov.br/produtos/"
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
        )

    def pesquisar_produto(self, string: str):
        self.driver.get(self.url)
        try:
            element = self.driver.find_element(by=By.ID, value="top-sbar")
            element.send_keys(string)
            time.sleep(3)

        
            try:
                captcha_element = self.driver.find_element(by=By.CLASS_NAME, value="btn-danger")

                if captcha_element.is_displayed():
                    print("Captcha encontrado. Resolva-o manualmente.")
                    time.sleep(10)
                    element = self.driver.find_element(by=By.ID, value="top-sbar")
                    element.send_keys(string)
                    time.sleep(3)
                    
            except NoSuchElementException:
                pass  # Se não achar o captcha, continua 
            
            

            button = self.driver.find_element(by=By.CLASS_NAME, value="fa-search")
            button.click()
            time.sleep(3)

            self.pesquisar_preco()
        except NoSuchElementException as e:
            print("Elemento não encontrado:", e)

    def pesquisar_preco(self):
        try:
            item_cards = self.driver.find_elements(by=By.CSS_SELECTOR, value="div.flex-item2")
            for item_card in item_cards:
                # Obtém o nome
                name_element = item_card.find_element(by=By.TAG_NAME, value="strong")
                name = name_element.text
                print("\n" + name)

                # Obtém o EAN
                ean_element = item_card.find_element(by=By.CSS_SELECTOR, value="span.search-gtin")
                ean = ean_element.get_attribute("data-gtin")
                print(ean)

                # Obtém o Preço
                price_element = item_card.find_element(
                    by=By.CSS_SELECTOR, value="div.flex-item2 > div:nth-child(2)"
                )
                price = price_element.text
                is_discounted = False
                if "De" in price or "por:" in price:
                    price_element = item_card.find_element(
                        by=By.CSS_SELECTOR, value="div.flex-item2 > div:nth-child(3)"
                    )
                    price = price_element.text
                    is_discounted = True
                print(price)

                # Obtém o nome do estabelecimento
                # Aqui procuramos pelo ícone e em seguida pelo div que contém o nome do estabelecimento
                div_index = 5
                if is_discounted:
                    div_index += 1  # Se o preço for com desconto, o índice do div muda
                store_element = item_card.find_element(
                    by=By.CSS_SELECTOR,
                    value=f"div.flex-item2 > div:nth-child({div_index})",
                )
                store = store_element.text
                print(store)

                div_index = 6
                if is_discounted:
                    div_index += 1  # Se o preço for com desconto, o índice do div muda
                adress_element = item_card.find_element(
                    by=By.CSS_SELECTOR,
                    value=f"div.flex-item2 > div:nth-child({div_index})",
                )
                address = adress_element.text
                print(address)

                div_index = 5

        except NoSuchElementException as e:
            print("Elemento de preço não encontrado:", e)
