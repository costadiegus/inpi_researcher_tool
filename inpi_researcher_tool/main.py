from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import time

import csv


def salvar_saida(texto):
    with open("output.csv", "a", encoding="utf-8") as arquivo:
        # Escrever o texto no arquivo com uma nova linha
        arquivo.write(texto + "\n")


def ler_arquivo_csv(nome_arquivo):
    lista_de_processos = []

    # Abrir o arquivo CSV para leitura
    with open(nome_arquivo, mode="r", encoding="utf-8") as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)

        # Iterar por cada linha no arquivo e adicionar à lista
        for linha in leitor_csv:
            lista_de_processos.append(linha[0])

    return lista_de_processos


# Uso da função
nome_arquivo = "processos.csv"
lista_de_processos = ler_arquivo_csv(nome_arquivo)


# Configuração do WebDriver para Firefox
"""driver = webdriver.Firefox(
    service=webdriver.firefox.service.Service(GeckoDriverManager().install())
)"""

# Configuração do WebDriver para Chrome
driver = webdriver.Chrome()

# Exibir a lista resultante
for processo in lista_de_processos:
    print(processo)
    # Acesse a página desejada
    driver.get("https://busca.inpi.gov.br/pePI/servlet/LoginController?action=login")

    # Esperar a página carregar (ajuste o tempo se necessário)
    time.sleep(3)

    # Localizar o elemento <area> pelo atributo href e clicar nele
    area = driver.find_element(
        By.CSS_SELECTOR, "area[href='/pePI/jsp/marcas/Pesquisa_num_processo.jsp']"
    )
    area.click()

    # Esperar para ver o resultado da ação (ajuste o tempo se necessário)
    time.sleep(3)

    # Preencher o campo de texto (altere o 'ID_DO_CAMPO_DE_TEXTO' conforme necessário)
    campo_texto = driver.find_element(By.NAME, "NumPedido")
    campo_texto.send_keys(processo)

    # Clicar no botão "Pesquisar" (altere o 'ID_DO_BOTAO' conforme necessário)
    botao_pesquisar = driver.find_element(By.NAME, "botao")
    botao_pesquisar.click()

    # Esperar a página carregar (ajuste o tempo se necessário)
    time.sleep(3)

    # Obter o texto específico da página de resultados (ajuste o seletor conforme necessário)
    status = driver.find_element(
        By.XPATH, "/html/body/form/div/div/table[3]/tbody/tr[2]/td[6]/font"
    ).text
    marca = driver.find_element(
        By.XPATH, "/html/body/form/div/div/table[3]/tbody/tr[2]/td[4]/font/b"
    ).text
    salvar_saida(f"{processo};{marca};{status}")

# Fechar o navegador
driver.quit()
