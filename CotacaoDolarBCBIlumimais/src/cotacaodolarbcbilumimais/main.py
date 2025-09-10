from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def create_headless_web_driver():
    options = webdriver.ChromeOptions() 
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_argument("--headless=new") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option("useAutomationExtension", False) 
    driver = webdriver.Chrome(options=options) 
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
    return driver

def create_web_driver():
    options = webdriver.ChromeOptions() 
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option("useAutomationExtension", False) 
    driver = webdriver.Chrome(options=options) 
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
    return driver

def find_element_presence_by_xpath(driver, page_element_xpath):
    page_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, page_element_xpath))
    )
    return page_element

def find_element_visibility_by_xpath(driver, page_element_xpath):
    page_element = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, page_element_xpath))
    )
    return page_element





def recupera_dloar_ptax_bcb(): 
    driver = create_headless_web_driver()
    try:
        driver.get("https://www.bcb.gov.br/")        
        page_element = find_element_presence_by_xpath(driver, '//div[contains(@class,"cotacao")]//table[1]//tr[1]//td[2]')
        dolar_ptax_compra = page_element.text.strip().lower()
        return dolar_ptax_compra
    except Exception as e:
        raise e
    finally:
        driver.close()


"""
======================================
ROBOT
======================================
"""
try:
    print('Iniciando processamento.')
    valor_dolar_ptax = recupera_dloar_ptax_bcb()
    print(f'Valor do dólar PTAX recuperado: {valor_dolar_ptax}.')
    print('Importando o valor no Ilumimais ...')
    web_driver = acessa_ilumimais()
    ilumimais_login(web_driver, 'atilano.couto@mspbrasil.com.br', '123@')
    ilumimais_navigate_to_cotacao(web_driver)
    print('Valor importado com sucesso.')
    web_driver.close()
except Exception as e:
    print(f'Erro ao processar: {e}')
finally:
    print('Fim do processamento.')
    