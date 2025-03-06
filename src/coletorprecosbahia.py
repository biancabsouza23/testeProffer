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
from datetime import datetime


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
                # Captura os dados do produto
                name = item_card.find_element(By.TAG_NAME, "strong").text
                ean = item_card.find_element(By.CSS_SELECTOR, "span.search-gtin").get_attribute("data-gtin")
                price = item_card.find_element(By.CSS_SELECTOR, "div.flex-item2 > div:nth-child(2)").text
                store = item_card.find_element(By.CSS_SELECTOR, "div.flex-item2 > div:nth-child(5)").text
                price = self.formatar_preco(price)  # Converte para float
                
                data_coleta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # dicionário com os dados do produto
                produto = {
                    "ean": ean,
                    "descricao": name,
                    "preco": price,
                    "data_coleta": data_coleta,
                    "codmunicipio": "",
                    "codestado": "",
                    "rede_fonte": store,
                    "bairro": "",
                    "cidade": "",
                    "uf": "",
                    "cnpj": "",
                }
                
                self.criar_resultado(produto)  # Passamos o dicionário diretamente
            
        except NoSuchElementException as e:
            print("Elemento não encontrado:", e)

    def criar_resultado(self, produto: dict):
        """Adiciona o produto coletado ao DataFrame de forma segura"""
        novo_df = pd.DataFrame([produto])  # Cria DataFrame do novo produto

        if self.resultado.empty:
            self.resultado = novo_df  # Se for vazio, apenas atribuímos o novo DataFrame
        else:
            self.resultado = pd.concat([self.resultado, novo_df], ignore_index=True)  # Concatenamos com índice atualizado

    
    def salvar_resultado(self, nome_arquivo_csv: str, nome_arquivo_json: str):
        """Salva os resultados coletados tanto em CSV quanto em JSON."""

        # Salvar como CSV
        self.resultado.to_csv(nome_arquivo_csv, index=False)

        # Salvar como JSON
        self.resultado.to_json(nome_arquivo_json, orient="records", indent=4, force_ascii=False)

        print(f"Resultados salvos com sucesso!\n- CSV: {nome_arquivo_csv}\n- JSON: {nome_arquivo_json}")



    def fechar_navegador(self):
        self.driver.quit()

    def formatar_preco(self, preco_str) -> float:
        """Remove 'R$', ignora texto promocional e converte valores para float."""
        preco_str = preco_str.replace("R$", "").strip()  # Remove "R$"
        preco_str = preco_str.replace(",", ".")  # Troca "," por "."

        # Caso o preço tenha texto promocional, pega o último valor
        # List Comprehension
        numeros = [s for s in preco_str.split() if s.replace(".", "").isdigit()]
        if numeros:
            return float(numeros[-1])  # Pega o último número como preço correto
        raise ValueError(f"Formato de preço inválido: {preco_str}") 

