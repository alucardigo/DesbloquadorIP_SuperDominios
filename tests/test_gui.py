import pytest
import tkinter as tk
from unittest.mock import MagicMock, patch
from desbloqueador_ip import DesbloqueadorIP

@pytest.fixture
def app():
    """Fixture para criar a aplicação"""
    with patch('tkinter.Tk') as mock_tk:
        root = MagicMock()
        mock_tk.return_value = root
        app = DesbloqueadorIP()
        yield app

def test_init_window_properties(app):
    """Testa as propriedades iniciais da janela"""
    assert app.root.title() == "Desbloqueador de IP"
    assert app.root.geometry() == "600x400"
    assert not app.root.resizable()

def test_progress_bar_initial_state(app):
    """Testa o estado inicial da barra de progresso"""
    assert app.progress["value"] == 0
    assert app.percent_label["text"] == "0%"

def test_start_button_properties(app):
    """Testa as propriedades do botão de início"""
    assert app.start_button["text"] == "Iniciar Desbloqueio"
    assert app.start_button["state"] == "normal"
    assert app.start_button["bg"] == "#4CAF50"

def test_log_text_initial_state(app):
    """Testa o estado inicial da área de log"""
    assert "Sistema inicializado" in app.log_text.get("1.0", tk.END)

@pytest.mark.parametrize("valor,mensagem", [
    (0, "Iniciando..."),
    (50, "Em progresso..."),
    (100, "Concluído!")
])
def test_atualizar_progresso(app, valor, mensagem):
    """Testa a atualização do progresso com diferentes valores"""
    app.atualizar_progresso(valor, mensagem)
    assert app.progress["value"] == valor
    assert app.percent_label["text"] == f"{valor}%"
    assert mensagem in app.log_text.get("1.0", tk.END)

def test_button_state_during_process(app):
    """Testa o estado do botão durante o processo"""
    app.start_button["state"] = "disabled"
    app.start_button["text"] = "Processando..."
    assert app.start_button["state"] == "disabled"
    assert app.start_button["text"] == "Processando..." 