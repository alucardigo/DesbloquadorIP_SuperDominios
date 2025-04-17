from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import requests
import traceback
from datetime import datetime

class DesbloqueadorIP:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Desbloqueador de IP")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Configurar tema
        self.root.configure(bg="#f0f0f0")
        
        # Frame principal
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True)
        
        # Título
        self.title_label = tk.Label(
            self.main_frame,
            text="Desbloqueador de IP",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        )
        self.title_label.pack(pady=(0, 20))
        
        # Frame de status
        self.status_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.status_frame.pack(fill="x", pady=(0, 20))
        
        # Barra de progresso
        self.progress = ttk.Progressbar(
            self.status_frame,
            orient="horizontal",
            length=400,
            mode="determinate"
        )
        self.progress.pack(side="left", padx=(0, 10))
        
        # Label de porcentagem
        self.percent_label = tk.Label(
            self.status_frame,
            text="0%",
            font=("Arial", 10),
            bg="#f0f0f0"
        )
        self.percent_label.pack(side="left")
        
        # Área de log
        self.log_frame = tk.Frame(self.main_frame, bg="white")
        self.log_frame.pack(fill="both", expand=True)
        
        self.log_text = tk.Text(
            self.log_frame,
            wrap="word",
            font=("Consolas", 10),
            bg="white",
            fg="black",
            height=10
        )
        self.log_text.pack(side="left", fill="both", expand=True)
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.log_frame, orient="vertical", command=self.log_text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=self.scrollbar.set)
        
        # Botão de iniciar
        self.start_button = tk.Button(
            self.main_frame,
            text="Iniciar Desbloqueio",
            font=("Arial", 12),
            command=self.iniciar_desbloqueio,
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10
        )
        self.start_button.pack(pady=(20, 0))
        
        # Configurar o log
        self.log_text.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] Sistema inicializado\n")
        self.log_text.see("end")
        
    def atualizar_progresso(self, valor, mensagem):
        self.progress["value"] = valor
        self.percent_label["text"] = f"{valor}%"
        self.log_text.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {mensagem}\n")
        self.log_text.see("end")
        self.root.update()
        
    def get_public_ip(self):
        """Obtém o IP público (externo) da conexão de internet"""
        try:
            self.atualizar_progresso(10, "Obtendo IP público...")
            
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
                        ip = response.text.strip()
                        self.atualizar_progresso(20, f"IP público obtido: {ip}")
                        return ip
                except:
                    continue
                    
            raise Exception("Não foi possível obter o IP público")
        except Exception as e:
            raise Exception(f"Erro ao obter IP público: {str(e)}")
            
    def iniciar_desbloqueio(self):
        self.start_button["state"] = "disabled"
        self.start_button["text"] = "Processando..."
        
        try:
            # Configurações do Chrome
            chrome_options = Options()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--dns-prefetch-disable")
            chrome_options.add_argument("--dns-servers=8.8.8.8,8.8.4.4")
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            chrome_options.add_experimental_option("detach", False)
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            
            # Credenciais
            username = os.getenv("SUPERDOMINIOS_USERNAME", "gleisontostes@gmail.com")
            password = os.getenv("SUPERDOMINIOS_PASSWORD", "EngField#")
            
            # Obter IP público
            public_ip = self.get_public_ip()
            
            # Iniciar navegador
            self.atualizar_progresso(30, "Iniciando navegador...")
            driver = webdriver.Chrome(options=chrome_options)
            
            # Login
            self.atualizar_progresso(40, "Realizando login...")
            driver.get("https://www.superdominios.org/home/clientarea.php")
            
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "inputEmail"))
            ).send_keys(username)
            
            driver.find_element(By.ID, "inputPassword").send_keys(password)
            driver.find_element(By.ID, "login").click()
            
            # Verificar login
            time.sleep(5)
            current_url = driver.current_url
            if "incorrect=true" in current_url:
                raise Exception("Falha no login: credenciais incorretas")
            
            self.atualizar_progresso(60, "Login realizado com sucesso")
            
            # Navegar para página de desbloqueio
            self.atualizar_progresso(70, "Acessando página de desbloqueio...")
            driver.get("https://www.superdominios.org/home/clientarea.php?action=productdetails&id=86027&modop=custom&a=management&mg-page=unban")
            
            # Preencher IP
            self.atualizar_progresso(80, "Preenchendo IP para desbloqueio...")
            ip_field = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "ipAddress"))
            )
            ip_field.clear()
            ip_field.send_keys(public_ip)
            
            # Clicar no botão de desbloqueio
            self.atualizar_progresso(90, "Iniciando processo de desbloqueio...")
            unblock_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn--success') and text()[contains(., 'Desbloquear')]]"))
            )
            unblock_button.click()
            
            time.sleep(5)
            
            # Sucesso
            self.atualizar_progresso(100, f"IP {public_ip} desbloqueado com sucesso!")
            messagebox.showinfo("Sucesso", f"O IP {public_ip} foi desbloqueado com sucesso!")
            
        except Exception as e:
            error_msg = str(e)
            traceback_str = traceback.format_exc()
            
            # Salvar log de erro
            with open("desbloqueio_error_log.txt", "w") as f:
                f.write(f"Erro: {error_msg}\n\n")
                f.write(traceback_str)
            
            self.atualizar_progresso(0, f"Erro: {error_msg}")
            messagebox.showerror("Erro", f"Ocorreu um erro durante o processo: {error_msg}\n\nDetalhes foram salvos em 'desbloqueio_error_log.txt'")
        
        finally:
            if 'driver' in locals():
                driver.quit()
            
            self.start_button["state"] = "normal"
            self.start_button["text"] = "Iniciar Desbloqueio"
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DesbloqueadorIP()
    app.run()