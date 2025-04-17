import pytest
from unittest.mock import MagicMock, patch
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException
from desbloqueador_ip import DesbloqueadorIP

@pytest.fixture
def app():
    """Fixture para criar a aplicação"""
    with patch('tkinter.Tk'):
        app = DesbloqueadorIP()
        yield app

def test_iniciar_desbloqueio_success(app, mock_driver, mock_env_vars, mock_requests):
    """Testa o processo completo de desbloqueio com sucesso"""
    # Configura os mocks para simular elementos da página
    email_field = MagicMock()
    password_field = MagicMock()
    login_button = MagicMock()
    ip_field = MagicMock()
    unblock_button = MagicMock()
    
    # Configura o comportamento do WebDriverWait
    with patch('selenium.webdriver.support.ui.WebDriverWait') as mock_wait:
        mock_wait.return_value.until.side_effect = [
            email_field,
            ip_field,
            unblock_button
        ]
        
        # Configura o mock do driver para encontrar elementos
        mock_driver.find_element.side_effect = [
            password_field,
            login_button
        ]
        
        # Executa o desbloqueio
        app.iniciar_desbloqueio()
        
        # Verifica se as credenciais foram usadas corretamente
        email_field.send_keys.assert_called_once_with("test@example.com")
        password_field.send_keys.assert_called_once_with("test123")
        login_button.click.assert_called_once()
        
        # Verifica se o IP foi preenchido
        ip_field.clear.assert_called_once()
        ip_field.send_keys.assert_called_once_with("192.168.1.1")
        
        # Verifica se o botão de desbloqueio foi clicado
        unblock_button.click.assert_called_once()

def test_iniciar_desbloqueio_login_failed(app, mock_driver, mock_env_vars, mock_requests):
    """Testa falha no login"""
    # Simula URL com erro de login
    mock_driver.current_url = "https://example.com/login?incorrect=true"
    
    with patch('tkinter.messagebox.showerror') as mock_error:
        app.iniciar_desbloqueio()
        mock_error.assert_called_once()
        assert "credenciais incorretas" in mock_error.call_args[0][1]

@pytest.mark.parametrize("exception,expected_message", [
    (TimeoutException, "Tempo limite excedido"),
    (WebDriverException, "Erro no navegador"),
    (Exception, "Ocorreu um erro")
])
def test_iniciar_desbloqueio_errors(app, mock_driver, mock_env_vars, mock_requests, exception, expected_message):
    """Testa diferentes tipos de erros durante o processo"""
    with patch('selenium.webdriver.support.ui.WebDriverWait') as mock_wait:
        mock_wait.return_value.until.side_effect = exception("Erro de teste")
        
        with patch('tkinter.messagebox.showerror') as mock_error:
            app.iniciar_desbloqueio()
            mock_error.assert_called_once()

def test_iniciar_desbloqueio_driver_cleanup(app, mock_driver, mock_env_vars, mock_requests):
    """Testa se o driver é fechado corretamente mesmo com erros"""
    with patch('selenium.webdriver.support.ui.WebDriverWait') as mock_wait:
        mock_wait.return_value.until.side_effect = Exception("Erro de teste")
        
        app.iniciar_desbloqueio()
        mock_driver.quit.assert_called_once()

def test_iniciar_desbloqueio_button_state_recovery(app, mock_driver, mock_env_vars, mock_requests):
    """Testa se o botão volta ao estado normal após erro"""
    with patch('selenium.webdriver.support.ui.WebDriverWait') as mock_wait:
        mock_wait.return_value.until.side_effect = Exception("Erro de teste")
        
        app.iniciar_desbloqueio()
        assert app.start_button["state"] == "normal"
        assert app.start_button["text"] == "Iniciar Desbloqueio"

def test_iniciar_desbloqueio_progress_updates(app, mock_driver, mock_env_vars, mock_requests):
    """Testa se a barra de progresso é atualizada corretamente"""
    progress_values = []
    
    def mock_atualizar_progresso(valor, mensagem):
        progress_values.append(valor)
    
    app.atualizar_progresso = mock_atualizar_progresso
    
    with patch('selenium.webdriver.support.ui.WebDriverWait') as mock_wait:
        mock_wait.return_value.until.side_effect = [
            MagicMock(),  # email field
            MagicMock(),  # ip field
            MagicMock()   # unblock button
        ]
        
        app.iniciar_desbloqueio()
        
        # Verifica se todos os valores esperados foram registrados
        assert 10 in progress_values  # Obtendo IP
        assert 30 in progress_values  # Iniciando navegador
        assert 40 in progress_values  # Realizando login
        assert 60 in progress_values  # Login realizado
        assert 70 in progress_values  # Acessando página
        assert 80 in progress_values  # Preenchendo IP
        assert 90 in progress_values  # Iniciando desbloqueio
        assert 100 in progress_values # Concluído 