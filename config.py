"""
Configurações do Bot de Sinais de Trading
"""

# Configurações do Telegram
TELEGRAM_CONFIG = {
    'BOT_TOKEN': '7629404700:AAHrY8g7DHyz3-iI6nAzorPdAMDcbLvYRkI',
    'CHAT_ID': '1065139183'
}

# Configurações de Trading
TRADING_CONFIG = {
    'SYMBOLS': ['BTC-USD', 'ETH-USD'],  # Símbolos padrão do Yahoo Finance
    'TIMEFRAME': '1d',  # Mudando para 1 dia temporariamente para teste
    'CHECK_INTERVAL': 60,  # segundos
    'RSI_PERIOD': 14,
    'EMA_FAST': 9,
    'EMA_SLOW': 21,
    'RSI_OVERSOLD': 30,
    'RSI_OVERBOUGHT': 70
}

# Configurações de Sinal
SIGNAL_CONFIG = {
    'DUPLICATE_PREVENTION_MINUTES': 5,
    'SIGNAL_EXPIRY_MINUTES': 1,
    'CHART_CANDLES': 50
}

# Links e URLs
URLS = {
    'HOMEBROKER': 'https://www.homebroker.com/pt/invest'
}

# Configurações de Logging
LOGGING_CONFIG = {
    'LEVEL': 'INFO',
    'FORMAT': '%(asctime)s - %(levelname)s - %(message)s',
    'FILE': 'trading_bot.log'
}
