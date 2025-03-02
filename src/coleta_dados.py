from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def configurar_navegador(com_proxy=False):
    options = Options()
    if com_proxy:
        options.add_argument('--proxy-server=http://50.174.7.159:80')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver

def buscar_preco(EAN, navegador="chrome"):
    driver = None
    try:
        print("Iniciando a busca...") 
        driver = configurar_navegador(com_proxy=False)
        driver.get("https://precodahora.ba.gov.br/produtos/")
        print("Acessando o site...") 
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "top-sbar"))
        )
        print("Campo de busca encontrado.")
        search_box.send_keys(EAN)
        print(f"EAN {EAN} digitado no campo de busca.")
        botao_busca = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-top-sbar"))
        )
        botao_busca.click() 
        print("Botão de busca clicado.")  
        time.sleep(5)
        try:
            info_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "list-info.mt-2.mb-2"))
            )
            print("Informações encontradas dentro da class 'list-info mt-2 mb-2'.")
            info_text = info_div.text.strip()
            print(f"Informações antes do <hr>: {info_text}")
        except Exception as e:
            print(f"Erro ao buscar informações: {e}")
            raise
        try:
            cases_info = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "cases"))
            ).text.strip()
            print(f"Número de resultados encontrados: {cases_info}")
        except Exception as e:
            print(f"Erro ao buscar o número de resultados: {e}")
            raise
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        print("Tentando com proxy...")
        if driver:
            driver.quit()
        driver = configurar_navegador(com_proxy=True)
        try:
            driver.get("https://precodahora.ba.gov.br/produtos/")
            print("Acessando o site novamente com proxy...") 
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "top-sbar"))
            )
            search_box.send_keys(EAN)
            print(f"EAN {EAN} digitado no campo de busca.")
            botao_busca = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "btn-top-sbar"))
            )
            botao_busca.click() 
            print("Botão de busca clicado.")  
            time.sleep(5)
            info_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "list-info.mt-2.mb-2"))
            )
            print("Informações encontradas dentro da class 'list-info mt-2 mb-2'.")
            info_text = info_div.text.strip()
            print(f"Informações antes do <hr>: {info_text}")
            cases_info = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "cases"))
            ).text.strip()
            print(f"Número de resultados encontrados: {cases_info}")
        except Exception as e:
            print(f"Ocorreu um erro ao tentar buscar novamente: {e}")
    finally:
        if driver:
            driver.quit()

buscar_preco("7896004713274")
