# 📦 Guia de Instalação - Bot de Sinais de Trading

## 🚀 Instalação Rápida (Recomendada)

### 1. Preparar o Ambiente
```bash
# Verificar versão do Python (requer 3.8+)
python --version

# Se necessário, instalar Python 3.8+ do site oficial
```

### 2. Executar Setup Automático
```bash
# Instalar dependências e configurar
python setup.py
```

### 3. Testar o Bot
```bash
# Executar testes de conectividade
python test_bot.py
```

### 4. Iniciar o Bot
```bash
# Método 1: Script de inicialização (recomendado)
python run_bot.py

# Método 2: Execução direta
python trading_signals_bot.py
```

---

## 🔧 Instalação Manual

### 1. Instalar Dependências
```bash
pip install yfinance==0.2.28
pip install pandas==2.1.4
pip install numpy==1.24.3
pip install mplfinance==0.12.10b0
pip install matplotlib==3.8.2
pip install gtts==2.5.1
pip install python-telegram-bot==20.7

# Ou usar o arquivo requirements.txt
pip install -r requirements.txt
```

### 2. Verificar Configurações
Edite o arquivo `config.py` se necessário:
```python
TELEGRAM_CONFIG = {
    'BOT_TOKEN': '7629404700:AAHrY8g7DHyz3-iI6nAzorPdAMDcbLvYRkI',
    'CHAT_ID': '1065139183'
}
```

### 3. Criar Diretórios
```bash
mkdir logs charts audio
```

---

## 🧪 Testes e Verificação

### Teste Completo
```bash
python test_bot.py
```

### Testes Individuais

#### Testar Yahoo Finance
```python
import yfinance as yf
data = yf.Ticker('BTC-USD').history(period='1d', interval='5m')
print(f"Dados obtidos: {len(data)} candles")
```

#### Testar Telegram
```python
import asyncio
from telegram import Bot

async def test():
    bot = Bot(token='SEU_BOT_TOKEN')
    await bot.send_message(chat_id='SEU_CHAT_ID', text='Teste!')

asyncio.run(test())
```

---

## 📱 Configuração do Telegram

### 1. Criar Bot no Telegram
1. Abra o Telegram e procure por `@BotFather`
2. Digite `/newbot`
3. Escolha um nome e username para seu bot
4. Copie o **Bot Token** fornecido

### 2. Obter Chat ID
1. Adicione seu bot a um grupo ou chat privado
2. Envie uma mensagem para o bot
3. Acesse: `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates`
4. Procure pelo **chat id** na resposta JSON

### 3. Configurar no Bot
Edite `config.py`:
```python
TELEGRAM_CONFIG = {
    'BOT_TOKEN': 'SEU_BOT_TOKEN_AQUI',
    'CHAT_ID': 'SEU_CHAT_ID_AQUI'
}
```

---

## 🐛 Solução de Problemas

### Erro: "ModuleNotFoundError"
```bash
# Instalar dependência faltante
pip install nome_do_modulo

# Ou reinstalar todas
pip install -r requirements.txt
```

### Erro: "Telegram Unauthorized"
- Verifique se o Bot Token está correto
- Confirme se o Chat ID está correto
- Teste enviar mensagem manual para o bot

### Erro: "Yahoo Finance Connection"
- Verifique conexão com internet
- Tente usar VPN se houver bloqueio regional
- Aguarde alguns minutos e tente novamente

### Erro: "Permission Denied"
```bash
# Linux/Mac: dar permissão de execução
chmod +x *.py

# Windows: executar como administrador
```

### Bot não envia sinais
- Verifique se as condições de mercado atendem aos critérios
- Confirme se não há sinais duplicados (prevenção de 5 min)
- Verifique logs em `trading_bot.log`

---

## 📊 Estrutura de Arquivos Final

```
trading-signals-bot/
├── trading_signals_bot.py    # Bot principal
├── config.py                 # Configurações
├── requirements.txt          # Dependências Python
├── setup.py                 # Script de instalação
├── run_bot.py               # Script de inicialização
├── test_bot.py              # Testes de conectividade
├── trading_signals.pine     # Código Pine Script (TradingView)
├── README.md                # Documentação principal
├── INSTALL.md               # Este guia de instalação
└── trading_bot.log          # Logs (criado automaticamente)
```

---

## ⚡ Comandos Rápidos

```bash
# Setup completo
python setup.py

# Testar tudo
python test_bot.py

# Iniciar bot (interativo)
python run_bot.py

# Iniciar bot (direto)
python trading_signals_bot.py

# Parar bot
Ctrl+C
```

---

## 🔄 Atualizações

Para atualizar o bot:
1. Faça backup do arquivo `config.py`
2. Baixe a nova versão
3. Restaure suas configurações
4. Execute `python setup.py` novamente

---

## 📞 Suporte

Se encontrar problemas:
1. ✅ Verifique este guia de instalação
2. 🧪 Execute `python test_bot.py`
3. 📝 Consulte os logs em `trading_bot.log`
4. 🔍 Verifique se todas as dependências estão instaladas
5. 🌐 Confirme conexão com internet e Telegram

---

**🎯 Bot pronto para detectar sinais de BTC e ETH 24/7!**
