import os
import requests
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

class DesbloqueadorIP:
    def __init__(self, master):
        self.master = master
        self.master.title("Desbloqueador de IP")
        self.master.geometry("600x400")
        
        # Configuração do Chrome
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless=new")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-infobars")
        self.chrome_options.add_argument("--disable-notifications")
        self.chrome_options.add_argument("--disable-popup-blocking")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--start-maximized")
        
        # Configurações experimentais
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.chrome_options.add_experimental_option('detach', False)
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Preferências
        prefs = {
            'profile.default_content_setting_values.notifications': 2,
            'profile.default_content_settings.popups': 0,
            'profile.default_content_setting_values.automatic_downloads': 1
        }
        self.chrome_options.add_experimental_option('prefs', prefs)

        # Interface
        self.start_button = tk.Button(self.master, text="Iniciar Desbloqueio", command=self.iniciar_desbloqueio)
        self.start_button.pack(pady=20)

        self.progress = tk.ttk.Progressbar(self.master, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        self.log_text = tk.Text(self.master, wrap="word", height=10, width=50)
        self.log_text.pack(pady=10)

    def get_public_ip(self):
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=10)
            if response.status_code == 200:
                return response.json()['ip']
            else:
                raise Exception(f"Erro na API: {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro de conexão: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro ao obter IP público: {str(e)}")

    def iniciar_desbloqueio(self):
        try:
            self.start_button.configure(state="disabled")
            self.progress["value"] = 0
            self.log_text.delete(1.0, tk.END)
            
            # Obter IP público
            self.atualizar_log("Obtendo IP público...")
            ip_publico = self.get_public_ip()
            self.atualizar_log(f"IP público obtido: {ip_publico}")
            self.atualizar_progresso(20, "IP obtido com sucesso")

            # Inicializar driver
            self.atualizar_log("Inicializando navegador...")
            service = Service('chromedriver.exe')
            self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
            self.atualizar_progresso(40, "Navegador inicializado")

            # Resto do processo...
            self.atualizar_progresso(100, "Processo concluído")
            
        except Exception as e:
            self.atualizar_log(f"Erro ao iniciar o desbloqueio: {str(e)}")
            self.progress["value"] = 0
        finally:
            self.start_button.configure(state="normal")
            if hasattr(self, 'driver'):
                self.driver.quit()

    def atualizar_log(self, mensagem):
        self.log_text.insert(tk.END, mensagem + "\n")
        self.log_text.see(tk.END)

    def atualizar_progresso(self, valor, mensagem=""):
        self.progress["value"] = valor
        if mensagem:
            self.atualizar_log(mensagem)

if __name__ == "__main__":
    root = tk.Tk()
    app = DesbloqueadorIP(root)
    root.mainloop() 