from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
import pandas as pd
from time import sleep
proxy = "PROXY_URL"
options = webdriver.ChromeOptions()
options.add_argument(
"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36") 
options.proxy = Proxy({ 'proxyType': ProxyType.MANUAL, 'httpProxy' : f'{proxy}'})
options.add_argument("start-maximized")
options.add_argument("--window-size=1920,1080")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
# Aguardar a página terminar de carregar.
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)
driver.get("https://steamdb.info/sales/")

driver.implicitly_wait(5)
exibicao = driver.find_element(By.ID, 'dt-length-0') 
driver.execute_script("arguments[0].scrollIntoView();", exibicao)
exibicao.click()

driver.implicitly_wait(5)
all_itens = driver.find_element(By.XPATH, '//*[@id="dt-length-0"]/option[8]') 
all_itens.click()

sleep(2)

tabela = driver.find_element(By.XPATH, '//*[@id="DataTables_Table_0"]')

# Extrai os título/cabeçalho
cabecalhos = tabela.find_element(By.TAG_NAME, "thead").find_elements(By.TAG_NAME, "th")
nomes_colunas = [cabecalho.text for cabecalho in cabecalhos]

# Corrigindo nomes na coluna
nomes_colunas[0] = 'Store_link'
nomes_colunas[1] = 'Imagem_URL'


print(nomes_colunas)



# Extrair linhas da tabela
linhas = tabela.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
dados = []

for linha in linhas:
    celulas = linha.find_elements(By.TAG_NAME, "td")
    linha_dados = []
    
    for i, celula in enumerate(celulas):
        driver.execute_script("arguments[0].scrollIntoView();", celula)

        if i == 0:
            link = celula.find_element(By.CLASS_NAME, "info-icon")
            link_url = link.get_attribute("href")
            linha_dados.append(link_url)
            
        elif i == 1:
            img_tag = celula.find_element(By.TAG_NAME, "img")
            imagem_url = img_tag.get_attribute("src")
            linha_dados.append(imagem_url)
        else:
            linha_dados.append(celula.text)
    
    dados.append(linha_dados)

df = pd.DataFrame(dados, columns=nomes_colunas)

# df.to_excel("scrap_steamdb_sales.xlsx", index=False)

driver.quit()