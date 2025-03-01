import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

def buscar_preco(EAN, navegador="chrome"):
    try:
        print("Iniciando a busca...") 

        # Configuração do driver para Chrome
        if navegador.lower() == "chrome":
            options = Options()
            options.headless = False
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        else:
            raise ValueError("Navegador não suportado. Use 'chrome'.")

        
        driver.get("https://precodahora.ba.gov.br/produtos/")
        print("Acessando o site...") 

      
        wait = WebDriverWait(driver, 10) 
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "top-sbar")))  # ID correto do campo de busca
        print("Campo de busca encontrado.")
        
       
        search_box.send_keys(EAN)
        print(f"EAN {EAN} digitado no campo de busca.")

        
        print("Esperando o botão de busca...")  
        botao_busca = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-top-sbar")))  # Classe do botão de busca
        print("Botão de busca encontrado.")

        
        botao_busca.click() 
        print("Botão de busca clicado.")  

        
        print("Aguardando a página carregar...") 
        time.sleep(5)  


        print("Conteúdo da página após a busca:")
        print(driver.page_source[:500])  

        time.sleep(5)

        # Tentar obter o preço
        print("Tentando encontrar o preço...") 
        try:
            preco = driver.find_element(By.CLASS_NAME, "precoProduto") 
            if preco:
                print(f"Produto {EAN} encontrado! Preço: {preco.text}")
            else:
                print(f"Produto {EAN} não encontrado ou preço não disponível.")
        except NoSuchElementException:
            print(f"Produto {EAN} não encontrado ou preço não disponível.")
        
        print("URL da página atual:", driver.current_url)
        print("Conteúdo da página:", driver.page_source[:500]) 

        print("Pressione ENTER para fechar o navegador...")
        input()

        driver.quit() 

    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        print(f"Ocorreu um erro específico do Selenium: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

buscar_preco("7896004713274")
