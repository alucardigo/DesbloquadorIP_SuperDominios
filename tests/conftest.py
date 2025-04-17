import pytest
from unittest.mock import MagicMock, patch
import tkinter as tk
from desbloqueador_ip import DesbloqueadorIP
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def mock_tkinter():
    """Mock para componentes do Tkinter"""
    with patch('tkinter.Tk') as mock_tk:
        # Configura o mock da janela principal
        mock_window = MagicMock()
        mock_window.title.return_value = "Desbloqueador de IP"
        mock_tk.return_value = mock_window
        
        # Configura o mock do botão
        mock_button = MagicMock()
        mock_button.configure.return_value = None
        mock_button.__getitem__.return_value = "Iniciar Desbloqueio"
        mock_button.__setitem__.return_value = None
        
        # Configura o mock da barra de progresso
        mock_progress = MagicMock()
        mock_progress.configure.return_value = None
        mock_progress.__getitem__.return_value = 0
        mock_progress.__setitem__.return_value = None
        
        # Configura o mock da área de texto
        mock_text = MagicMock()
        mock_text.get.return_value = "Sistema inicializado\n"
        mock_text.insert.return_value = None
        
        yield mock_window, mock_button, mock_progress, mock_text

@pytest.fixture
def app(mock_tkinter):
    """Fixture que retorna uma instância do DesbloqueadorIP com mocks"""
    mock_window, mock_button, mock_progress, mock_text = mock_tkinter
    app = DesbloqueadorIP()
    app.root = mock_window
    app.start_button = mock_button
    app.progress = mock_progress
    app.log_text = mock_text
    return app

@pytest.fixture
def mock_driver():
    """Mock para o WebDriver do Selenium"""
    with patch('selenium.webdriver.Chrome') as mock_chrome:
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        yield mock_driver

@pytest.fixture
def mock_env_vars():
    """Mock para variáveis de ambiente"""
    with patch.dict('os.environ', {
        'SUPERDOMINIOS_USERNAME': 'test@example.com',
        'SUPERDOMINIOS_PASSWORD': 'testpassword'
    }):
        yield

@pytest.fixture
def mock_requests():
    """Mock para requisições HTTP"""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '192.168.1.1'
        mock_get.return_value = mock_response
        yield mock_get

@pytest.fixture
def mock_chrome_options():
    """Mock para opções do Chrome"""
    with patch('selenium.webdriver.ChromeOptions') as mock_options:
        mock_options_instance = MagicMock()
        mock_options.return_value = mock_options_instance
        yield mock_options_instance

@pytest.fixture
def chrome_options():
    """Fixture para configurações do Chrome"""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return options 