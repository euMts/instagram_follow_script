from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import constants
import os

# - DEFININDO VARIAVEIS -
contas = constants.contas
senhas = constants.senhas
esconderNavegador = constants.esconderNavegador
contasParaSeguir = constants.contasParaSeguir
ativas = []
drivers = [] # diferentes nomes para drivers do selenium, diferentes instancias de navegador

# - DEFININDO FUNCÕES -
# ESCONDER CARACTERES DE UMA STRING
def password(entrada):
    temp = ""
    for x in range(len(entrada)):
        temp += "*"
    return temp

# GERAR INSTANCIA DOS NAVEGADORES
def gerarInstancias(contas, senhas): # gerarInstancias(listaContendoContas, listaContendoSenhas)
    for x in range(len(contas)): # cria x instancias de navegador referentes ao numero de contas subscritas no arquivo constants.py
        options = Options()
        options.headless = esconderNavegador # True: esconder navegador; False: mostrar navegador
        drivers.append(webdriver.Firefox(options=options))
        drivers[x].maximize_window()
        print(f"Iniciando instancia referente a conta:\n'{contas[f'conta{x}']}' de senha {password(str(senhas[f'conta{x}']))}")
        ativas.append(contas[f'conta{x}'])
        try:
            entrarNoInsta(drivers[x], contas[f"conta{x}"], senhas[f"conta{x}"])
            print(f"Instancia de '{contas[f'conta{x}']}' logada e pronta para uso.")
        except Exception as e:
            print(f"Erro durante a inicializacao de '{contas[f'conta{x}']}'", e)
            break
        print()

# ENTRANDO NO INSTAGRAM
def entrarNoInsta(driver, login, senha): # entra na conta x(login, senha) na instancia x(driver)
    loginInputXpath = ('//input[@name="username"]') # input login
    senhaInputXpath = ('//input[@name="password"]') # input senha
    botaoLoginXpath = ('//*[@id="loginForm"]/div/div[3]/button') # botao 'entrar'
    iconeLogadoXpath = ('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]') # icone da foto (verifica se entrou na conta)
    driver.get("https://www.instagram.com/")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, loginInputXpath))) # espera o elemento ficar disponível
    driver.find_element_by_xpath(loginInputXpath).send_keys(login)
    sleep(1)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, senhaInputXpath)))
    driver.find_element_by_xpath(senhaInputXpath).send_keys(senha)
    sleep(1)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, botaoLoginXpath)))
    driver.find_element_by_xpath(botaoLoginXpath).click()
    sleep(1)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, iconeLogadoXpath)))
    sleep(2)

def seguirConta(driver, alvo, paramConta): # alvo = arroba da pessoa | media de 3s para seguir cada conta
    fotoXpath = ('//img[@data-testid="user-avatar"]')
    seguindoXpath = ('//span[@class="glyphsSpriteFriend_Follow u-__7"]')
    seguirXpath = ("//span[@class='vBF20 _1OSdk']")
    alvoSemArroba = ""
    if alvo[0] == "@":
        for x in range(1, len(alvo)):
            alvoSemArroba += alvo[x]
    else:
        alvoSemArroba = alvo
    print(f'Conta: \'{contas[f"conta{paramConta}"]}\' - Seguindo {alvo}')
    try:
        driver.get(f"https://www.instagram.com/{alvoSemArroba}/")
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, fotoXpath)))
        if driver.find_elements_by_xpath(seguindoXpath):
            pass
        else:
            driver.find_element_by_xpath(seguirXpath).click()
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, seguindoXpath)))
        print(f'Conta: \'{contas[f"conta{paramConta}"]}\' - A conta: {alvo} foi seguida com sucesso.\n')
    except Exception as e:
        print("erro", e)

# ENCERRAR TODOS OS DRIVERS
def encerrarDrivers():
    for x in range(len(drivers)):
        drivers[x].quit()

# - INICIALIZACAO -
gerarInstancias(contas, senhas)
os.system('cls' if os.name == 'nt' else 'clear')
print(f"Pronto para seguir {len(contasParaSeguir)} {'usuário' if len(contasParaSeguir) == 1 else 'usuários'}.\nUtilizando {len(contas)} contas. {ativas}")
print(f"Tempo estimado: {(len(contasParaSeguir)*3)*len(contas)} segundos ({(len(contasParaSeguir)*3)*len(contas)/60:.2f} minutos)\n")
for y in range(len(contasParaSeguir)):
    for x in range(len(contas)):
        seguirConta(drivers[x], contasParaSeguir[y], x)
print(f"Todas as {len(contasParaSeguir)} contas foram seguidas.\nEncerrando navegadores...")
encerrarDrivers()
print("Navegadores finalizados, encerrando.")
input()
