from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import tkinter as tk
from tkinter import messagebox
import sys
import os
import requests

def get_public_ip():
    """Obtém o IP público (externo) da conexão de internet"""
    try:
        # Usando diferentes serviços de IP para garantir confiabilidade
        services = [
            "https://api.ipify.org",
            "https://ipinfo.io/ip",
            "https://api.myip.com",
            "https://checkip.amazonaws.com"
        ]
        
        for service in services:
            try:
                response = requests.get(service, timeout=5)
                if response.status_code == 200:
                    # Remove quaisquer espaços em branco ou quebras de linha
                    ip = response.text.strip()
                    return ip
            except:
                continue
                
        # Se chegamos aqui, nenhum serviço funcionou
        raise Exception("Não foi possível obter o IP público")
    except Exception as e:
        raise Exception(f"Erro ao obter IP público: {str(e)}")

def resource_path(relative_path):
    """Retorna caminho absoluto para recursos, funciona para desenvolvimento e para o executável"""
    try:
        # PyInstaller cria um temp folder e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def show_success_message():
    """Mostra uma mensagem de sucesso"""
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    messagebox.showinfo("Sucesso", "O processo de desbloqueio foi concluído com sucesso!")
    root.destroy()

def main():
    # Configurações do Chrome em modo headless (invisível)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Credenciais de login - substitua com as credenciais reais
    username = "gleisontostes@gmail.com"
    password = "EngField#"
    
    try:
        # Primeiro obtém o IP público antes de iniciar o navegador
        public_ip = get_public_ip()
        print(f"IP público detectado: {public_ip}")
        
        # Iniciar o navegador Chrome
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navegar para a página de login
        driver.get("https://www.superdominios.org/home/clientarea.php")
        
        # Preencher o campo de email
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "inputEmail"))
        ).send_keys(username)
        
        # Preencher o campo de senha
        driver.find_element(By.ID, "inputPassword").send_keys(password)
        
        # Clicar no botão de login
        driver.find_element(By.ID, "login").click()
        
        # Aguardar 3 segundos após o login
        time.sleep(3)
        
        # Navegar para a página de desbloqueio
        driver.get("https://www.superdominios.org/home/clientarea.php?action=productdetails&id=86027&modop=custom&a=management&mg-page=unban")
        
        # Encontrar o campo de IP e limpar qualquer valor existente
        ip_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "ipAddress"))
        )
        ip_field.clear()
        
        # Inserir o IP público no campo
        ip_field.send_keys(public_ip)
        
        # Clicar no botão de desbloqueio
        # Usando XPath para encontrar o botão com o texto exato
        unblock_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn--success') and text()[contains(., 'Desbloquear')]]"))
        )
        unblock_button.click()
        
        # Aguardar um momento para garantir que a ação foi concluída
        time.sleep(2)
        
        # Mostrar mensagem de sucesso com o IP desbloqueado
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Sucesso", f"O IP {public_ip} foi desbloqueado com sucesso!")
        root.destroy()
        
    except Exception as e:
        # Em caso de erro, exibir uma mensagem
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erro", f"Ocorreu um erro durante o processo: {str(e)}")
        root.destroy()
    
    finally:
        # Fechar o navegador se estiver inicializado
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    main()