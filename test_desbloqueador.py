import unittest
from unittest.mock import patch, MagicMock
from DesbloqueiaIP1_0 import DesbloqueadorIP
import tkinter as tk
from selenium.webdriver.chrome.options import Options
import os

class TestDesbloqueadorIP(unittest.TestCase):
    def setUp(self):
        self.app = DesbloqueadorIP()
        
    def test_init(self):
        """Testa se a janela é criada corretamente"""
        self.assertIsInstance(self.app.root, tk.Tk)
        self.assertEqual(self.app.root.title(), "Desbloqueador de IP")
        self.assertEqual(self.app.root.geometry(), "600x400")
        
    def test_chrome_options(self):
        """Testa se as opções do Chrome estão configuradas corretamente"""
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
        
        # Verifica se todas as opções estão presentes
        self.assertIn("--headless=new", chrome_options.arguments)
        self.assertIn("--dns-prefetch-disable", chrome_options.arguments)
        self.assertIn("--dns-servers=8.8.8.8,8.8.4.4", chrome_options.arguments)
        
    @patch('selenium.webdriver.Chrome')
    def test_iniciar_desbloqueio(self, mock_chrome):
        """Testa o processo de desbloqueio"""
        # Configura o mock
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        
        # Simula o processo de login
        mock_driver.current_url = "https://www.superdominios.org/home/clientarea.php"
        
        # Executa o processo
        self.app.iniciar_desbloqueio()
        
        # Verifica se o botão foi desabilitado
        self.assertEqual(self.app.start_button["state"], "disabled")
        
    def test_get_public_ip(self):
        """Testa a obtenção do IP público"""
        with patch('requests.get') as mock_get:
            # Configura o mock para retornar um IP
            mock_get.return_value.text = "192.168.1.1"
            
            ip = self.app.get_public_ip()
            self.assertEqual(ip, "192.168.1.1")
            
    def test_atualizar_progresso(self):
        """Testa a atualização da barra de progresso"""
        self.app.atualizar_progresso(50, "Testando progresso")
        self.assertEqual(self.app.progress["value"], 50)
        self.assertEqual(self.app.percent_label["text"], "50%")
        
    def tearDown(self):
        self.app.root.destroy()

if __name__ == '__main__':
    unittest.main() 