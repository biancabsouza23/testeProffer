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
        print("Iniciando a busca...")  # Diagnóstico

        # Configuração do driver para Chrome
        if navegador.lower() == "chrome":
            options = Options()
            options.headless = False  # Mudei para False para visualizar o navegador
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        else:
            raise ValueError("Navegador não suportado. Use 'chrome'.")

        # Acessando o site e realizando a busca
        driver.get("https://precodahora.ba.gov.br/produtos/")
        print("Acessando o site...")  # Diagnóstico

        # Esperar o campo de busca ficar visível e interagível
        wait = WebDriverWait(driver, 10)  # Aguarda até 10 segundos
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "top-sbar")))  # ID correto do campo de busca
        print("Campo de busca encontrado.")  # Diagnóstico
        
        # Digitar o EAN no campo de busca
        search_box.send_keys(EAN)
        print(f"EAN {EAN} digitado no campo de busca.")  # Diagnóstico

        # Esperar o botão de busca se tornar visível e clicável
        print("Esperando o botão de busca...")  # Diagnóstico
        botao_busca = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-top-sbar")))  # Classe do botão de busca
        print("Botão de busca encontrado.")  # Diagnóstico

        # Clicar no botão de busca
        botao_busca.click()  # Clicar no botão de busca
        print("Botão de busca clicado.")  # Diagnóstico

        # Aguardar o carregamento completo da página de resultados
        print("Aguardando a página carregar...")  # Diagnóstico
        time.sleep(5)  # Pausa adicional de 5 segundos para garantir que a página carregue completamente

        # Verificar o conteúdo da página carregada para depuração
        print("Conteúdo da página após a busca:")
        print(driver.page_source[:500])  # Exibe os primeiros 500 caracteres do conteúdo da página carregada

        # Adicionar um tempo de espera extra antes de tentar localizar o preço
        time.sleep(5)

        # Tentar obter o preço
        print("Tentando encontrar o preço...")  # Diagnóstico
        try:
            preco = driver.find_element(By.CLASS_NAME, "precoProduto")  # Substitua com o seletor correto
            if preco:
                print(f"Produto {EAN} encontrado! Preço: {preco.text}")
            else:
                print(f"Produto {EAN} não encontrado ou preço não disponível.")
        except NoSuchElementException:
            print(f"Produto {EAN} não encontrado ou preço não disponível.")
        
        # Exibir a URL da página carregada e o conteúdo HTML
        print("URL da página atual:", driver.current_url)
        print("Conteúdo da página:", driver.page_source[:500])  # Exibe os primeiros 500 caracteres

        # Pausar para manter o navegador aberto
        print("Pressione ENTER para fechar o navegador...")
        input()  # Espera o usuário apertar ENTER antes de fechar o navegador

        driver.quit()  # Fechar o navegador

    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        print(f"Ocorreu um erro específico do Selenium: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Teste com o EAN
buscar_preco("7896004713274")
