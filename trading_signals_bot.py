#!/usr/bin/env python3
"""
Bot de Sinais Integrado - Binance + Yahoo Finance
"""

import asyncio
import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
from gtts import gTTS
from telegram import Bot
import logging
import warnings
from config import TELEGRAM_CONFIG, TRADING_CONFIG, URLS, LOGGING_CONFIG, BINANCE_CONFIG
from binance import AsyncClient, BinanceSocketManager
import yfinance as yf

warnings.filterwarnings('ignore')

import logging
from config import LOGGING_CONFIG

logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG['LEVEL']),
    format=LOGGING_CONFIG['FORMAT'],
    handlers=[
        logging.FileHandler(LOGGING_CONFIG['log_file_name']),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class TradingSignalsBot:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_CONFIG['BOT_TOKEN'])
        self.symbols_crypto = TRADING_CONFIG['ASSETS']
        self.symbols_stocks = TRADING_CONFIG['SYMBOLS_STOCKS']
        self.timeframes = TRADING_CONFIG['TIMEFRAMES']
        self.rsi_period = TRADING_CONFIG['RSI_PERIOD']
        self.ema_fast = TRADING_CONFIG['EMA_FAST']
        self.ema_slow = TRADING_CONFIG['EMA_SLOW']
        self.rsi_oversold = TRADING_CONFIG['RSI_OVERSOLD']
        self.rsi_overbought = TRADING_CONFIG['RSI_OVERBOUGHT']
        self.last_signals = {}
        self.binance_client = None

    async def start_binance(self):
        self.binance_client = await AsyncClient.create(
            api_key=BINANCE_CONFIG['API_KEY'],
            api_secret=BINANCE_CONFIG['API_SECRET']
        )
        logger.info("Binance client iniciado")

    async def close_binance(self):
        if self.binance_client:
            await self.binance_client.close_connection()
            logger.info("Conexão Binance encerrada")

    async def get_binance_klines(self, symbol, interval, limit=100):
        try:
            klines = await self.binance_client.get_klines(symbol=symbol, interval=interval, limit=limit)
            df = pd.DataFrame(klines, columns=[
                'open_time', 'Open', 'High', 'Low', 'Close', 'Volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            df['Open'] = df['Open'].astype(float)
            df['High'] = df['High'].astype(float)
            df['Low'] = df['Low'].astype(float)
            df['Close'] = df['Close'].astype(float)
            df['Volume'] = df['Volume'].astype(float)
            df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
            df.set_index('open_time', inplace=True)
            return df[['Open', 'High', 'Low', 'Close', 'Volume']]
        except Exception as e:
            logger.error(f"Erro ao obter klines Binance {symbol} {interval}: {e}")
            return None

    def get_stock_data(self, symbol, period='5d', interval='1m'):
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)
            if df.empty:
                logger.warning(f"Yahoo Finance retornou dados vazios para {symbol}")
                return None
            df.index = pd.to_datetime(df.index)
            df.rename(columns={'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close', 'Volume': 'Volume'}, inplace=True)
            return df[['Open', 'High', 'Low', 'Close', 'Volume']]
        except Exception as e:
            logger.error(f"Erro ao obter dados Yahoo Finance para {symbol}: {e}")
            return None

    def calculate_rsi(self, prices, period):
        delta = prices.diff()
        gain = delta.where(delta > 0, 0).rolling(window=period).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def calculate_ema(self, prices, period):
        return prices.ewm(span=period).mean()

    def detect_reversal_candle(self, data, idx):
        if idx < 3:
            return False, None
        current = data.iloc[idx]
        prev1 = data.iloc[idx-1]
        prev2 = data.iloc[idx-2]
        prev3 = data.iloc[idx-3]
        if (prev3['Close'] > prev2['Close'] and
            prev2['Close'] > prev1['Close'] and
            current['Close'] > current['Open'] and
            current['Close'] > prev1['Close']):
            return True, 'BUY'
        if (prev3['Close'] < prev2['Close'] and
            prev2['Close'] < prev1['Close'] and
            current['Close'] < current['Open'] and
            current['Close'] < prev1['Close']):
            return True, 'SELL'
        return False, None

    def analyze(self, data, symbol, timeframe):
        if data is None or len(data) < self.rsi_period + 5:
            return None
        data['RSI'] = self.calculate_rsi(data['Close'], self.rsi_period)
        data['EMA_9'] = self.calculate_ema(data['Close'], self.ema_fast)
        data['EMA_21'] = self.calculate_ema(data['Close'], self.ema_slow)
        idx = len(data) - 1
        rsi = data.iloc[idx]['RSI']
        ema_9 = data.iloc[idx]['EMA_9']
        ema_21 = data.iloc[idx]['EMA_21']
        has_reversal, reversal_type = self.detect_reversal_candle(data, idx)
        signal = None
        if (rsi < self.rsi_oversold and ema_9 > ema_21 and has_reversal and reversal_type == 'BUY'):
            signal = {
                'type': 'BUY',
                'symbol': symbol,
                'timeframe': timeframe,
                'rsi': rsi,
                'ema_9': ema_9,
                'ema_21': ema_21,
                'price': data.iloc[idx]['Close'],
                'timestamp': datetime.utcnow(),
                'data': data
            }
        elif (rsi > self.rsi_overbought and ema_9 < ema_21 and has_reversal and reversal_type == 'SELL'):
            signal = {
                'type': 'SELL',
                'symbol': symbol,
                'timeframe': timeframe,
                'rsi': rsi,
                'ema_9': ema_9,
                'ema_21': ema_21,
                'price': data.iloc[idx]['Close'],
                'timestamp': datetime.utcnow(),
                'data': data
            }
        return signal

    def create_chart(self, signal):
        try:
            data = signal['data'].tail(50)
            mc = mpf.make_marketcolors(up='g', down='r', edge='inherit',
                                       wick={'up': 'green', 'down': 'red'}, volume='in')
            s = mpf.make_mpf_style(marketcolors=mc, gridstyle='-', y_on_right=True)
            apds = [
                mpf.make_addplot(data['EMA_9'], color='blue', width=1.5),
                mpf.make_addplot(data['EMA_21'], color='orange', width=1.5)
            ]
            fig, axes = mpf.plot(data, type='candle', style=s, addplot=apds, volume=True,
                                 title=f"{signal['symbol']} {signal['timeframe']} - Sinal de {signal['type']}",
                                 ylabel='Preço', ylabel_lower='Volume', figsize=(12,8), returnfig=True)
            ax = axes[0]
            last_price = signal['price']
            color = 'green' if signal['type'] == 'BUY' else 'red'
            marker = '^' if signal['type'] == 'BUY' else 'v'
            ax.scatter(len(data)-1, last_price, color=color, s=200, marker=marker, zorder=5)
            ax.annotate(signal['type'], xy=(len(data)-1, last_price), xytext=(10,10),
                        textcoords='offset points', bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.7),
                        fontsize=12, fontweight='bold', color='white')
            chart_path = f"chart_{signal['symbol']}_{signal['timeframe']}_{signal['type']}.png"
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            plt.close()
            return chart_path
        except Exception as e:
            logger.error(f"Erro ao criar gráfico: {e}")
            return None

    def create_audio(self, signal):
        try:
            symbol_name = signal['symbol']
            action = "compra" if signal['type'] == 'BUY' else "venda"
            time_str = signal['timestamp'].strftime("%H:%M UTC")
            text = f"Sinal de {action} em {symbol_name}. Entrada às {time_str}."
            tts = gTTS(text=text, lang='pt', slow=False)
            audio_path = f"signal_{signal['symbol']}_{signal['timeframe']}_{signal['type']}.mp3"
            tts.save(audio_path)
            return audio_path
        except Exception as e:
            logger.error(f"Erro ao criar áudio: {e}")
            return None

    def format_message(self, signal):
        symbol_display = signal['symbol']
        entry_time = signal['timestamp'].strftime("%H:%M:%S UTC")
        expiry_time = (signal['timestamp'] + timedelta(minutes=1)).strftime("%H:%M:%S UTC")
        action_emoji = "🟢" if signal['type'] == 'BUY' else "🔴"
        action_text = "COMPRA" if signal['type'] == 'BUY' else "VENDA"
        rsi_condition = f"RSI {signal['rsi']:.1f} {'< ' + str(self.rsi_oversold) if signal['type'] == 'BUY' else '> ' + str(self.rsi_overbought)}"
        ema_condition = f"EMA 9 {'acima' if signal['type'] == 'BUY' else 'abaixo'} da EMA 21"

        msg = (
            f"✅ Entrada Confirmada\n"
            f"💹 Ativo: {symbol_display}\n"
            f"⏰ Entrada: {entry_time}\n"
            f"⌛ Expiração: {expiry_time}\n"
            f"⏳ Timeframe: {signal['timeframe']}\n"
            f"🧠 Análise: RSI + MME + Padrão gráfico\n"
            f"📘 Detalhes: {rsi_condition} + candle de reversão + cruzamento de MME\n"
            f"{action_emoji} Sinal: {action_text}\n"
            f"💰 Preço: ${signal['price']:.2f}\n"
            f"📊 Gráfico anexado\n"
            f"🔗 {URLS['HOMEBROKER']}"
        )
        return msg

    async def send_signal(self, signal):
        try:
            chart_path = self.create_chart(signal)
            audio_path = self.create_audio(signal)
            message = self.format_message(signal)

            await self.bot.send_message(chat_id=TELEGRAM_CONFIG['CHAT_ID'], text=message)

            if chart_path and os.path.exists(chart_path):
                with open(chart_path, 'rb') as photo:
                    await self.bot.send_photo(chat_id=TELEGRAM_CONFIG['CHAT_ID'], photo=photo,
                                              caption=f"📊 Gráfico - {signal['symbol']} - {signal['type']} ({signal['timeframe']})")
                os.remove(chart_path)

            if audio_path and os.path.exists(audio_path):
                with open(audio_path, 'rb') as audio:
                    await self.bot.send_voice(chat_id=TELEGRAM_CONFIG['CHAT_ID'], voice=audio,
                                              caption=f"🔊 Sinal de voz - {signal['type']}")
                os.remove(audio_path)

            logger.info(f"Sinal enviado: {signal['symbol']} {signal['type']} {signal['timeframe']}")

        except Exception as e:
            logger.error(f"Erro ao enviar sinal: {e}")

    def should_send(self, signal):
        key = f"{signal['symbol']}_{signal['timeframe']}_{signal['type']}"
        now = datetime.utcnow()
        if key in self.last_signals:
            diff = now - self.last_signals[key]
            if diff.total_seconds() < TRADING_CONFIG['DUPLICATE_PREVENTION_MINUTES'] * 60:
                return False
        self.last_signals[key] = now
        return True

    async def analyze_and_send(self, symbol, timeframe, is_crypto=True):
        if is_crypto:
            data = await self.get_binance_klines(symbol, timeframe)
        else:
            # Para ações, o timeframe será ignorado e o intervalo 1m usado para AAPL
            data = self.get_stock_data(symbol)
        signal = self.analyze(data, symbol, timeframe)
        if signal and self.should_send(signal):
            await self.send_signal(signal)

    async def monitor(self):
        await self.start_binance()
        try:
            while True:
                tasks = []
                for tf in self.timeframes:
                    for symb in self.symbols_crypto:
                        tasks.append(self.analyze_and_send(symb, tf, True))
                    for symb in self.symbols_stocks:
                        tasks.append(self.analyze_and_send(symb, tf, False))
                await asyncio.gather(*tasks)
                logger.info(f"Aguardando {TRADING_CONFIG['CHECK_INTERVAL']} segundos para próxima análise...")
                await asyncio.sleep(TRADING_CONFIG['CHECK_INTERVAL'])
        except Exception as e:
            logger.error(f"Erro no monitoramento: {e}")
        finally:
            await self.close_binance()

    async def start(self):
        await self.bot.send_message(
            chat_id=TELEGRAM_CONFIG['USER_ID'],
            text="🤖 Bot iniciado e monitorando ativos: "
                 + ", ".join(self.symbols_crypto + self.symbols_stocks)
        )
        logger.info("Bot iniciado")
        await self.monitor()

async def main():
    bot = TradingSignalsBot()
    await bot.start()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
