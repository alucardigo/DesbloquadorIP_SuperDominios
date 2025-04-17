# Desbloqueador de IP

Um aplicativo Python para desbloquear IPs automaticamente através do painel de controle da Super Domínios.

## Funcionalidades

- Interface gráfica amigável
- Desbloqueio automático de IP
- Feedback visual em tempo real
- Logs detalhados do processo
- Execução em segundo plano

## Requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- ChromeDriver compatível com sua versão do Chrome

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/alucardigo/DesbloquadorIP_SuperDominios.git
cd desbloqueador-ip
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Baixe o ChromeDriver:
- Verifique sua versão do Chrome
- Baixe o ChromeDriver compatível em: https://chromedriver.chromium.org/downloads
- Coloque o arquivo `chromedriver.exe` na pasta do projeto

## Configuração

1. Abra o arquivo `DesbloqueiaIP1.0.py`
2. Substitua as credenciais de login:
```python
username = "seu-email@exemplo.com"
password = "sua-senha"
```

## Uso

Execute o programa:
```bash
python DesbloqueiaIP1.0.py
```

Ou use o executável:
```bash
DesbloqueadorIP.exe
```

## Compilação

Para criar o executável:
```bash
pyinstaller --onefile --windowed --name="DesbloqueadorIP" DesbloqueiaIP1.0.py
```

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contribuição

Contribuições são bem-vindas! Por favor, leia as [diretrizes de contribuição](CONTRIBUTING.md) para detalhes sobre o processo de submissão de pull requests. 