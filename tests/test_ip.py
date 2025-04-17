import pytest
import requests
from unittest.mock import MagicMock, patch
from desbloqueador_ip import DesbloqueadorIP

@pytest.fixture
def app():
    """Fixture para criar a aplicação"""
    with patch('tkinter.Tk'):
        app = DesbloqueadorIP()
        yield app

def test_get_public_ip_success(app, mock_requests):
    """Testa obtenção bem-sucedida do IP público"""
    ip = app.get_public_ip()
    assert ip == "192.168.1.1"
    mock_requests.assert_called_once()

def test_get_public_ip_multiple_services(app):
    """Testa tentativa de múltiplos serviços quando alguns falham"""
    with patch('requests.get') as mock:
        # Simula falha nos dois primeiros serviços
        mock.side_effect = [
            requests.exceptions.RequestException,
            requests.exceptions.RequestException,
            MagicMock(status_code=200, text="10.0.0.1"),
        ]
        
        ip = app.get_public_ip()
        assert ip == "10.0.0.1"
        assert mock.call_count == 3

def test_get_public_ip_all_services_fail(app):
    """Testa quando todos os serviços falham"""
    with patch('requests.get') as mock:
        mock.side_effect = requests.exceptions.RequestException
        
        with pytest.raises(Exception) as exc_info:
            app.get_public_ip()
        
        assert "Não foi possível obter o IP público" in str(exc_info.value)

@pytest.mark.parametrize("status_code,response_text", [
    (404, "Not Found"),
    (500, "Server Error"),
    (403, "Forbidden")
])
def test_get_public_ip_error_status(app, status_code, response_text):
    """Testa diferentes códigos de erro HTTP"""
    with patch('requests.get') as mock:
        mock.return_value = MagicMock(
            status_code=status_code,
            text=response_text
        )
        
        with pytest.raises(Exception):
            app.get_public_ip()

def test_get_public_ip_timeout(app):
    """Testa timeout na requisição"""
    with patch('requests.get') as mock:
        mock.side_effect = requests.exceptions.Timeout
        
        with pytest.raises(Exception) as exc_info:
            app.get_public_ip()
        
        assert "Não foi possível obter o IP público" in str(exc_info.value)

def test_get_public_ip_connection_error(app):
    """Testa erro de conexão"""
    with patch('requests.get') as mock:
        mock.side_effect = requests.exceptions.ConnectionError
        
        with pytest.raises(Exception) as exc_info:
            app.get_public_ip()
        
        assert "Não foi possível obter o IP público" in str(exc_info.value) 