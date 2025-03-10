import os
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import json
from datetime import datetime
import re
import os
from src.alertasonoro import AlertaSonoro

class ColetorPrecosBahia:
    def __init__(self):
        # Inicialização do Selenium
        options = webdriver.ChromeOptions()
        options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )  # Evita detecção
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        # Inicializa o navegador
        self.url = "https://precodahora.ba.gov.br/produtos/"
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
        )

        # Define a cidade padrão
        self.cidade_atual: str = "N/A"
        self.produto_atual: str = "N/A"

        # Criar DataFrame para armazenar os dados
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

    def handle_captcha(self):
        """
        Verifica se há um CAPTCHA e pausa a execução para resolução manual.
        """
        time.sleep(3)
        captcha_url = "https://precodahora.ba.gov.br/challenge/"

        if self.driver.current_url == captcha_url:
            print(
                "⚠️ CAPTCHA encontrado! Resolva manualmente e pressione Enter para continuar."
            )
            AlertaSonoro.alerta()
            input("Pressione Enter depois de resolver o CAPTCHA...")

    def extrair_dados_produtos(self):
        """
        Extrai os dados dos produtos da página atual.
        """
        try:
            item_cards = self.driver.find_elements(
                by=By.CSS_SELECTOR, value="div.flex-item2"
            )
            # Se há uma lista de produtos, é por que há produtos disponíveis
            self.produto_encontrado(self.cidade_atual, self.produto_atual)
            for item_card in item_cards:
                # Captura os dados do produto
                name = item_card.find_element(By.TAG_NAME, "strong").text
                try:
                    ean = item_card.find_element(By.CSS_SELECTOR, "span.search-gtin").get_attribute("data-gtin")
                except NoSuchElementException:
                    # EAN não informado
                    ean = "N/A"
                try:
                    # Verifica se existe a classe "sobre-desconto"
                    desconto = item_card.find_elements(By.CLASS_NAME, "sobre-desconto")

                    if desconto:
                        # Se houver desconto, pegar o preço na terceira div e a loja na sexta div
                        price = item_card.find_element(
                            By.CSS_SELECTOR, "div.flex-item2 > div:nth-child(3)"
                        ).text
                        store = item_card.find_element(
                            By.CSS_SELECTOR, "div.flex-item2 > div:nth-child(6)"
                        ).text
                        endereco_element = item_card.find_element(
                            By.CSS_SELECTOR, "div.flex-item2 > div:nth-child(7)"
                        )
                    else:
                        # Se não houver desconto, pegar o preço na segunda div e a loja na quinta div
                        price = item_card.find_element(
                            By.CSS_SELECTOR, "div.flex-item2 > div:nth-child(2)"
                        ).text
                        store = item_card.find_element(
                            By.CSS_SELECTOR, "div.flex-item2 > div:nth-child(5)"
                        ).text
                        endereco_element = item_card.find_element(
                            By.CSS_SELECTOR, "div.flex-item2 > div:nth-child(6)"
                        )
                except NoSuchElementException:
                    print("Preço ou loja não encontrados!")
                    price = "N/A"
                    store = "N/A"  # Define valores padrão caso os elementos não sejam encontrados

                price = self.formatar_preco(price)  # Converte para float
                endereco = endereco_element.text
                dados_endereco = self.extrair_endereco(endereco)

                # Criamos o dicionário diretamente
                produto = {
                    "ean": ean,
                    "descricao": name,
                    "preco": price,
                    "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "codmunicipio": self.codmunicipio(dados_endereco["cidade"]),
                    "codestado": "29",
                    "rede_fonte": store,
                    "logradouro": dados_endereco["logradouro"],
                    "bairro": dados_endereco["bairro"],
                    "cep": dados_endereco["cep"],
                    "cidade": dados_endereco["cidade"],
                    "uf": "BA",
                }
                self.adicionar_resultado(produto)  # Passamos o dicionário diretamente
        except NoSuchElementException as e:
            self.produto_nao_encontrado(self.cidade_atual, self.produto_atual)
            print("Elemento não encontrado:", e)

    def adicionar_resultado(self, produto: dict):
        """Adiciona o produto coletado ao DataFrame de forma segura."""
        novo_df = pd.DataFrame([produto])

        if self.resultado.empty:
            self.resultado = novo_df
        else:
            self.resultado = pd.concat([self.resultado, novo_df], ignore_index=True)
    
    def limpar_resultados(self):
        """
        Limpa o arquivo de resultados.
        
        Usados nos testes.
        """
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

    def salvar_arquivo_resultados(self, nome_arquivo_csv: str, nome_arquivo_json: str):
        """Salva o arquivo de resultados coletados nos formatos CSV quanto em JSON na pasta output."""
        caminho_output = "output"

        # Garante que o diretório exista
        os.makedirs(caminho_output, exist_ok=True)

        # Define os caminhos completos dos arquivos
        caminho_csv = os.path.join(caminho_output, nome_arquivo_csv)
        caminho_json = os.path.join(caminho_output, nome_arquivo_json)

        self.resultado.to_csv(caminho_csv, index=False)
        self.resultado.to_json(
            caminho_json, orient="records", indent=4, force_ascii=False
        )

        print(
            f"✅ Resultados salvos com sucesso!\n- CSV: {caminho_csv}\n- JSON: {caminho_json}"
        )

    def fechar_navegador(self):
        """Fecha o navegador controlado pelo Selenium."""
        self.driver.quit()

    def formatar_preco(self, preco_str) -> float:
        """Remove 'R$', ignora texto promocional e converte valores para float."""
        preco_str = preco_str.replace("R$", "").strip()  # Remove "R$"
        preco_str = preco_str.replace(".", "")  # Remove "."
        preco_str = preco_str.replace(",", ".")  # Troca "," por "."

        # Pega apenas o último número válido (se houver promoções)
        numeros = [s for s in preco_str.split() if s.replace(".", "").isdigit()]
        if numeros:
            return float(numeros[-1])
        raise ValueError(f"Formato de preço inválido: {preco_str}")

    import re

    def extrair_endereco(self, endereco):
        """Separa logradouro, número, bairro, CEP e cidade a partir do endereço completo."""

        endereco = endereco.strip()  # Remove espaços extras

        # Expressão regular para encontrar CEP (8 dígitos seguidos)
        cep_match = re.search(r"\b\d{8}\b", endereco)
        cep = cep_match.group() if cep_match else ""

        # Remover CEP da string para facilitar o parsing
        endereco_sem_cep = endereco.replace(cep, "").strip()

        # Separar cidade (parte após a vírgula)
        if "," in endereco_sem_cep:
            endereco_principal, cidade = endereco_sem_cep.rsplit(",", 1)
            cidade = cidade.strip()
        else:
            endereco_principal = endereco_sem_cep
            cidade = ""

        # Separar logradouro, número e bairro
        partes = endereco_principal.split()

        logradouro = []
        numero = ""
        bairro = ""

        for i, parte in enumerate(partes):
            if (
                parte.isdigit()
            ):  # O primeiro número encontrado deve ser o número do endereço
                numero = parte
                bairro = " ".join(partes[i + 1 :])  # O restante será o bairro
                break
            else:
                logradouro.append(parte)

        logradouro = " ".join(logradouro)

        return {
            "logradouro": logradouro,
            "numero": numero,
            "bairro": bairro,
            "cep": cep,
            "cidade": cidade,
            "uf": "BA",
        }

    def codmunicipio(self, cidade) -> int:
        if cidade == "SALVADOR":
            return 2910800
        elif cidade == "FEIRA DE SANTANA":
            return 2927408
        else:
            return 0

    def mudar_cidade(self, cidade: str):
        """Muda a cidade de pesquisa no site."""
        """Pesquisa um produto no site e extrai os dados."""
        self.cidade_atual = cidade
        self.driver.get(self.url)
        try:
            # Verificar se o site está pedindo CAPTCHA
            self.handle_captcha()

            # Digita no campo de pesquisa
            button = self.driver.find_element(by=By.CLASS_NAME, value="location-info")
            button.click()
            time.sleep(3)

            button = self.driver.find_element(by=By.ID, value="add-center")
            button.click()
            time.sleep(3)

            element = self.driver.find_element(by=By.CLASS_NAME, value="sbar-municipio")
            time.sleep(3)
            element.send_keys(cidade)
            time.sleep(3)

            button = self.driver.find_element(by=By.CLASS_NAME, value="set-mun")
            button.click()
            time.sleep(3)

            button = self.driver.find_element(by=By.ID, value="aplicar")
            button.click()
            time.sleep(3)

        except NoSuchElementException as e:
            print("Elemento não encontrado:", e)

    def pesquisar_produto(self, produto: str):
        """Pesquisa um produto no site e extrai os dados."""
        self.driver.get(self.url)
        self.produto_atual = produto
        try:
            # Verificar se o site está pedindo CAPTCHA
            self.handle_captcha()

            # Digita no campo de pesquisa
            element = self.driver.find_element(by=By.ID, value="top-sbar")
            element.send_keys(produto)
            time.sleep(3)

            # Aperta o botão de pesquisa
            button = self.driver.find_element(by=By.CLASS_NAME, value="fa-search")
            button.click()
            time.sleep(3)

            # Extrai as informações de produtos
            self.extrair_dados_produtos()
        except NoSuchElementException as e:
            print("Elemento não encontrado:", e)
    
    def produto_encontrado(self, cidade: str, produto: str):
        """
        Realiza algum procedimento quando um produto é encontrado.
        """
        with open("output/produtos_encontrados.txt", "a") as f:
            f.write(produto + "," + cidade + "\n")

    def produto_nao_encontrado(self, cidade: str, produto: str):
        """
        Realiza algum procedimento quando um produto não é encontrado.
        """
        with open("output/produtos_nao_encontrados.txt", "w") as f:
            f.write(produto + "," + cidade + "\n")
