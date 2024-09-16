#Não me responsabilizo pelo uso indeviso dessa aplicação
#Projeto puramente feito para estudo

#É aconselhável o minimo de conhecimento de sql para o uso desse arquivo

#instale um ambiente virtual, e dentro dele instale o playwright, e o pyodbc
#Junto com isso tenha um banco de dados já pronto, ou faça um

#É aconselhável que as colunas no banco de dados sejam:
#id_horario(int), nome(varchar), horaOnline(time), diaOnline(date), vezes(int)

#se caso queira esse arquivo em .exe, importe o auto-py-to-exe e faça por ele

from playwright.sync_api import Playwright, sync_playwright
import time
from datetime import datetime
from plyer import notification
import pyodbc

#Database
dados_conexao = (
    "Driver={SQL Server};"
    "Server= ;" #adicione o seu server
    "Database= ;" #adicione o seu banco de dados
)

conexao = pyodbc.connect(dados_conexao)
print("Conexão Bem Sucedida")

cursor = conexao.cursor()

nome = input("Qual nome aparece no direct da pessoa?\n")

#contador
contador = 0
def incrementa_contador():
    global contador
    contador += 1
    return contador

#configs
user = '' #o user da sua conta
password = '' #a senha da sua conta

date = datetime.now().date()
hour = datetime.now().time()
vezes = incrementa_contador()
id = 1

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    #Página
    page.goto("https://www.instagram.com/")

    #Login
    page.get_by_label("Telefone, nome de usuário ou").click()
    page.get_by_label("Telefone, nome de usuário ou").fill(user)
    page.get_by_label("Telefone, nome de usuário ou").click()
    page.get_by_label("Senha").click()
    page.get_by_label("Senha").fill(password)
    page.get_by_role("button", name="Entrar", exact=True).click()

    #Espera do login
    time.sleep(3)

    #Pulando o notificações e indo para a conversa
    page.get_by_role("button", name="Agora não").click()
    page.goto("https://www.instagram.com/direct")
    page.get_by_role("button", name="Agora não").click()
    time.sleep(10)

    while True:
        try:
            page.goto("https://www.instagram.com/direct")
            if page.get_by_role("button", name=f"Avatar do usuário Online {nome} Online agora").click():
                page.goto("https://www.instagram.com/direct/inbox")
                time.sleep(30)
            else:
                notification.notify(
                    title=f"{nome} tá online",
                    message=f"{nome} ficou online",
                    timeout=15,
                    app_icon="image/cat.ico"
                )

                comando = f"""INSERT INTO 'Nome_tabela'(coluna1, coluna2, coluna3, coluna4, coluna5)
                VALUES
                    ({id},'{nome}','{hour}', '{date}',{vezes})"""
                cursor.execute(comando)
                cursor.commit()

                time.sleep(900)
        except Exception as e:
            print(f"ocorreu um erro: {e}")
            time.sleep(30)
    # ---------------------


with sync_playwright() as playwright:
    run(playwright)