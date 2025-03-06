from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import json

class ColetorPrecosBahia:
    def __init__(self):
        options = webdriver.ChromeOptions()
        self.url = "https://precodahora.ba.gov.br/produtos/"
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
        )
        self.resultado = pd.DataFrame(
            columns=[
                "ean",
                "descricao",
                "preco",
                "data_coleta",
                "codmunicipio",
                "codestado",
                "rede_fonte",
                "bairro",
                "cidade",
                "uf",
                "cnpj",
            ]
        )

    def handle_captcha(self) -> None:
        time.sleep(3)
        captcha_url = "https://precodahora.ba.gov.br/challenge/"
        if self.driver.current_url == captcha_url: # verifica URL atual do navegador controlado pelo SELENIUM
            print("Captcha encontrado. Resolva-o manualmente.")
            time.sleep(20)

    def pesquisar_produto(self, string: str):
        self.driver.get(self.url)
        try:
            # Verificar se o site está pedindo captcha
            self.handle_captcha()
            # Digita no campo de pesquisa
            element = self.driver.find_element(by=By.ID, value="top-sbar")
            element.send_keys(string)
            time.sleep(3)
            # Aperta o botão de pesquisa
            button = self.driver.find_element(by=By.CLASS_NAME, value="fa-search")
            button.click()
            time.sleep(3)
            # Extrai as informações de produtos
            self.extrair_dados_produtos()
        except NoSuchElementException as e:
            print("Elemento não encontrado:", e)

    def extrair_dados_produtos(self):
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
                self.criar_resultado(
                    ean=ean,
                    descricao=name,
                    preco=float(price),
                    data_coleta="2025-03-04",
                    codmunicipio="",  # Não temos essa informação
                    codestado="",  # Não temos essa informação
                    rede_fonte=store,
                    bairro="",
                    cidade="",
                    uf="",
                    cnpj="",
                )

        except NoSuchElementException as e:
            print("Elemento de preço não encontrado:", e)

    def criar_resultado(self, ean: str, descricao: str, preco: float, data_coleta: str, codmunicipio: int, codestado: int, rede_fonte: str, bairro: str, cidade: str, uf: str, cnpj: str):
        # Cria um dicionário com os dados
        item = {
            "ean": ean,
            "descricao": descricao,
            "preco": preco,
            "data_coleta": data_coleta,
            "codmunicipio": codmunicipio,
            "codestado": codestado,
            "rede_fonte": rede_fonte,
            "bairro": bairro,
            "cidade": cidade,
            "uf": uf,
            "cnpj": cnpj,
        }
        self.resultado = pd.concat([self.resultado, pd.DataFrame([item])])
    
    def salvar_resultado(self, nome_arquivo: str):
        self.resultado.to_csv(nome_arquivo, index=False)

    def fechar_navegador(self):
        self.driver.quit()
