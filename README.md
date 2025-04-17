# Desbloqueador de IP

Aplicação Python para desbloqueio automático de IPs através do painel de controle Super Domínios.

## 🚀 Funcionalidades

- Interface gráfica amigável
- Desbloqueio automático de IP
- Feedback visual em tempo real
- Logs detalhados do processo
- Execução em segundo plano

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- ChromeDriver compatível com sua versão do Chrome

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/alucardigo/DesbloquadorIP_SuperDominios.git
cd DesbloquadorIP_SuperDominios
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Baixe o ChromeDriver:
- Acesse https://chromedriver.chromium.org/downloads
- Baixe a versão compatível com seu Chrome
- Coloque o arquivo `chromedriver.exe` na raiz do projeto

4. Configure suas credenciais:
- Crie um arquivo `.env` baseado no `.env.example`
- Preencha suas credenciais do Super Domínios

## 🛠️ Uso

1. Execute o programa:
```bash
python DesbloqueiaIP1_0.py
```

2. Clique no botão "Iniciar Desbloqueio"

3. Aguarde o processo ser concluído

## 📦 Criação do Executável

Para criar um executável do programa:

```bash
pyinstaller --noconfirm --onefile --windowed --name="DesbloqueadorIP" --distpath="." DesbloqueiaIP1.0.py
```

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request 
