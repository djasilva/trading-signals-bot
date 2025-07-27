#!/usr/bin/env python3
"""
Script de demonstração - Gera um sinal de trading para mostrar funcionalidade completa
"""

import asyncio
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from trading_signals_bot import TradingSignalsBot
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DemoBot(TradingSignalsBot):
    def generate_demo_signal_data(self, symbol, signal_type='BUY'):
        """Gera dados que resultarão em um sinal específico"""
        try:
            import random
            
            # Preço base
            base_price = 45000 if 'BTC' in symbol else 2500
            
            # Gerar 100 candles
            dates = pd.date_range(end=datetime.now(), periods=100, freq='1H')
            data = []
            
            # Criar sequência específica para garantir padrão de reversão
            prices = []
            current_price = base_price
            
            # Gerar preços base
            for i in range(100):
                if i < 96:  # Primeiros 96 candles - movimento normal
                    change = random.uniform(-0.005, 0.005)
                    current_price *= (1 + change)
                elif signal_type == 'BUY':
                    # Últimos 4 candles - criar padrão de reversão para compra
                    if i == 96:  # 3 candles atrás - alta
                        current_price *= 1.01
                    elif i == 97:  # 2 candles atrás - queda
                        current_price *= 0.99
                    elif i == 98:  # 1 candle atrás - mais queda
                        current_price *= 0.98
                    else:  # i == 99 - candle atual - reversão (alta)
                        current_price *= 1.02
                else:  # SELL
                    # Últimos 4 candles - criar padrão de reversão para venda
                    if i == 96:  # 3 candles atrás - baixa
                        current_price *= 0.99
                    elif i == 97:  # 2 candles atrás - alta
                        current_price *= 1.01
                    elif i == 98:  # 1 candle atrás - mais alta
                        current_price *= 1.02
                    else:  # i == 99 - candle atual - reversão (baixa)
                        current_price *= 0.98
                
                prices.append(current_price)
            
            # Criar dados OHLC
            for i, (date, price) in enumerate(zip(dates, prices)):
                if i == 99:  # Último candle - garantir padrão correto
                    if signal_type == 'BUY':
                        # Candle verde: close > open e close > close anterior
                        open_price = price * 0.995
                        close_price = price
                        high = price * 1.002
                        low = open_price * 0.998
                        # Garantir que close > close anterior
                        if i > 0:
                            close_price = max(close_price, prices[i-1] * 1.001)
                    else:  # SELL
                        # Candle vermelho: close < open e close < close anterior
                        open_price = price * 1.005
                        close_price = price
                        high = open_price * 1.002
                        low = price * 0.998
                        # Garantir que close < close anterior
                        if i > 0:
                            close_price = min(close_price, prices[i-1] * 0.999)
                else:
                    # Candles normais
                    variation = random.uniform(0.995, 1.005)
                    open_price = price * variation
                    close_price = price
                    high = max(open_price, close_price) * random.uniform(1.001, 1.005)
                    low = min(open_price, close_price) * random.uniform(0.995, 0.999)
                
                volume = random.randint(1000, 10000)
                
                data.append({
                    'Open': open_price,
                    'High': high,
                    'Low': low,
                    'Close': close_price,
                    'Volume': volume
                })
            
            df = pd.DataFrame(data, index=dates)
            
            # Calcular indicadores
            df['RSI'] = self.calculate_rsi(df['Close'])
            df['EMA_9'] = self.calculate_ema(df['Close'], 9)
            df['EMA_21'] = self.calculate_ema(df['Close'], 21)
            
            # Forçar condições para garantir sinal
            if signal_type == 'BUY':
                # RSI em sobrevenda
                df.loc[df.index[-1], 'RSI'] = 25
                # EMA 9 > EMA 21 (tendência de alta)
                ema21_value = df.loc[df.index[-1], 'EMA_21']
                df.loc[df.index[-1], 'EMA_9'] = ema21_value * 1.01
            else:  # SELL
                # RSI em sobrecompra
                df.loc[df.index[-1], 'RSI'] = 75
                # EMA 9 < EMA 21 (tendência de baixa)
                ema21_value = df.loc[df.index[-1], 'EMA_21']
                df.loc[df.index[-1], 'EMA_9'] = ema21_value * 0.99
            
            logger.info(f"📊 Dados de demonstração gerados para {symbol} - Sinal: {signal_type}")
            logger.info(f"   RSI final: {df['RSI'].iloc[-1]:.1f}")
            logger.info(f"   EMA 9: {df['EMA_9'].iloc[-1]:.2f}")
            logger.info(f"   EMA 21: {df['EMA_21'].iloc[-1]:.2f}")
            logger.info(f"   Últimos 4 closes: {df['Close'].iloc[-4:].values}")
            
            return df
            
        except Exception as e:
            logger.error(f"Erro ao gerar dados de demo: {e}")
            return None
    
    def get_crypto_data(self, symbol, period='5d', interval='1h'):
        """Override para usar dados de demonstração"""
        # Alternar entre sinais de compra e venda para demonstração
        signal_type = 'BUY' if 'BTC' in symbol else 'SELL'
        return self.generate_demo_signal_data(symbol, signal_type)

async def demo_signals():
    """Executa demonstração de sinais"""
    print("🎬 DEMONSTRAÇÃO DE SINAIS DE TRADING")
    print("=" * 50)
    
    bot = DemoBot()
    
    # Testar conexão Telegram
    try:
        await bot.bot.send_message(
            chat_id=bot.bot._chat_id if hasattr(bot.bot, '_chat_id') else '1065139183',
            text="🎬 Iniciando demonstração de sinais de trading!"
        )
    except:
        pass
    
    print("📊 Gerando sinais de demonstração...")
    
    # Analisar BTC (configurado para gerar sinal de COMPRA)
    print("\n🟢 Testando sinal de COMPRA (BTC)...")
    btc_signal = bot.analyze_signals('BTC-USD')
    
    if btc_signal:
        print(f"✅ Sinal de {btc_signal['type']} detectado para BTC!")
        print(f"   RSI: {btc_signal['rsi']:.1f}")
        print(f"   Preço: ${btc_signal['price']:.2f}")
        
        # Enviar sinal completo
        await bot.send_telegram_signal(btc_signal)
        print("📱 Sinal enviado para Telegram!")
    else:
        print("❌ Nenhum sinal detectado para BTC")
    
    # Aguardar um pouco
    await asyncio.sleep(3)
    
    # Analisar ETH (configurado para gerar sinal de VENDA)
    print("\n🔴 Testando sinal de VENDA (ETH)...")
    eth_signal = bot.analyze_signals('ETH-USD')
    
    if eth_signal:
        print(f"✅ Sinal de {eth_signal['type']} detectado para ETH!")
        print(f"   RSI: {eth_signal['rsi']:.1f}")
        print(f"   Preço: ${eth_signal['price']:.2f}")
        
        # Enviar sinal completo
        await bot.send_telegram_signal(eth_signal)
        print("📱 Sinal enviado para Telegram!")
    else:
        print("❌ Nenhum sinal detectado para ETH")
    
    print("\n" + "=" * 50)
    print("🎉 Demonstração concluída!")
    print("📱 Verifique seu Telegram para ver os sinais completos")
    print("   (mensagem + gráfico + áudio)")

if __name__ == "__main__":
    try:
        asyncio.run(demo_signals())
    except KeyboardInterrupt:
        print("\n🛑 Demonstração interrompida")
    except Exception as e:
        print(f"❌ Erro na demonstração: {e}")
