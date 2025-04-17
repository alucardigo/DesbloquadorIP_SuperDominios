import pytest
import tkinter as tk
from unittest.mock import Mock, patch
from selenium.webdriver.chrome.options import Options
from DesbloqueiaIP1_0 import DesbloqueadorIP

@pytest.fixture
def app():
    root = tk.Tk()
    app = DesbloqueadorIP(root)
    yield app
    root.destroy()

@pytest.fixture
def mock_driver():
    with patch('selenium.webdriver.Chrome') as mock:
        driver = Mock()
        mock.return_value = driver
        yield driver

def test_init_window_properties(app):
    assert app.master.title() == "Desbloqueador de IP"
    assert app.master.geometry() == "600x400"
    assert app.start_button["state"] == "normal"
    assert app.progress["value"] == 0

def test_chrome_options(app):
    assert isinstance(app.chrome_options, Options)
    args = app.chrome_options.arguments
    assert "--headless=new" in args
    assert "--no-sandbox" in args
    assert "--disable-dev-shm-usage" in args
    assert "--disable-gpu" in args
    assert "--disable-extensions" in args
    assert "--disable-infobars" in args
    assert "--disable-notifications" in args
    assert "--disable-popup-blocking" in args
    assert "--disable-blink-features=AutomationControlled" in args
    assert "--window-size=1920,1080" in args
    assert "--start-maximized" in args

def test_button_state(app):
    assert app.start_button["state"] == "normal"
    app.start_button.configure(state="disabled")
    assert app.start_button["state"] == "disabled"
    app.start_button.configure(state="normal")
    assert app.start_button["state"] == "normal"

def test_progress_updates(app):
    app.atualizar_progresso(50, "Teste de progresso")
    assert app.progress["value"] == 50
    assert "Teste de progresso" in app.log_text.get("1.0", tk.END)

def test_log_updates(app):
    app.atualizar_log("Teste de log")
    assert "Teste de log" in app.log_text.get("1.0", tk.END)
    
    app.log_text.delete("1.0", tk.END)
    app.atualizar_log("Novo teste")
    assert "Novo teste" in app.log_text.get("1.0", tk.END)

@patch('requests.get')
def test_iniciar_desbloqueio_success(mock_get, app, mock_driver):
    mock_get.return_value.json.return_value = {'ip': '192.168.1.1'}
    mock_get.return_value.status_code = 200
    
    app.iniciar_desbloqueio()
    
    assert "Obtendo IP público..." in app.log_text.get("1.0", tk.END)
    assert "IP público obtido: 192.168.1.1" in app.log_text.get("1.0", tk.END)
    assert "Inicializando navegador..." in app.log_text.get("1.0", tk.END)
    assert "Navegador inicializado" in app.log_text.get("1.0", tk.END)
    assert "Processo concluído" in app.log_text.get("1.0", tk.END)
    assert app.progress["value"] == 100
    assert app.start_button["state"] == "normal"

@patch('requests.get')
def test_iniciar_desbloqueio_error(mock_get, app):
    mock_get.side_effect = Exception("Erro de conexão")
    
    app.iniciar_desbloqueio()
    
    assert "Erro ao iniciar o desbloqueio" in app.log_text.get("1.0", tk.END)
    assert app.progress["value"] == 0
    assert app.start_button["state"] == "normal" 