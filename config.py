# config.py

TELEGRAM_CONFIG = {
    "BOT_TOKEN": "7629404700:AAHrY8g7DHyz3-iI6nAzorPdAMDcbLvYRkI",
    "USER_ID": "1065139183"
}

TRADING_CONFIG = {
    "ASSETS": ["BTCUSDT", "ETHUSDT"],  # ← corrigido para Binance
    "SYMBOLS_STOCKS": [],  # ← caso queira adicionar ações depois
    "TIMEFRAMES": ["5m"],  # timeframe usado na análise
    "RSI_PERIOD": 14,
    "EMA_FAST": 9,
    "EMA_SLOW": 21,
    "RSI_OVERSOLD": 30,
    "RSI_OVERBOUGHT": 70,
    "CHECK_INTERVAL": 60,  # segundos entre cada varredura
    "DUPLICATE_PREVENTION_MINUTES": 5,  # tempo para evitar sinais duplicados
    "BUY_THRESHOLD": 30,
    "SELL_THRESHOLD": 70
}

SIGNAL_CONFIG = {
    "DELAY_MINUTES": 2,     # Envia sinal com 2 minutos de antecedência
    "EXPIRATION_MINUTES": 1,
    "INCLUDE_CHART": True,
    "INCLUDE_AUDIO": True,
    "TRADING_LINK_HOMEBROKER": "https://www.homebroker.com/pt/invest",
    "TRADING_LINK_BINANCE": "https://www.binance.com/pt-BR"
}

BINANCE_CONFIG = {
    "API_KEY": "Nc6LP69p4QhkBTI3pqX6RKd2GuVUAvvxW8gJlu3UIoXidL31XcvioWduWzjDQqqy",     # Preencha se for usar Binance API
    "API_SECRET": "GDC5JMzgQUjrr3ztvxOaVMlkdCPGN1WbF5Ohx46dyXdvlxj29fMyI5kI3ldzROBW"
}

URLS = {
    "YAHOO_FINANCE_BASE": "https://query1.finance.yahoo.com"
}

LOGGING_CONFIG = {
    "log_to_file": True,
    "log_file_name": "trading_signals.log",
    "LEVEL": "INFO",
    "FORMAT": "%(asctime)s - %(levelname)s - %(message)s"
}
