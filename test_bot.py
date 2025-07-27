#!/usr/bin/env python3
"""
Script de teste para o Bot de Sinais de Trading
"""

import asyncio
import yfinance as yf
from datetime import datetime
from config import TELEGRAM_CONFIG, TRADING_CONFIG

async def test_data_connection():
    """Testa conexão com Yahoo Finance"""
    print("🔍 Testando conexão com Yahoo Finance...")
    
    for symbol in TRADING_CONFIG['SYMBOLS']:
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d', interval='5m')
            
            if not data.empty:
                last_price = data['Close'].iloc[-1]
                print(f"✅ {symbol}: ${last_price:.2f} - {len(data)} candles obtidos")
            else:
                print(f"❌ {symbol}: Dados vazios")
                
        except Exception as e:
            print(f"❌ {symbol}: Erro - {e}")

async def test_telegram_connection():
    """Testa conexão com Telegram"""
    print("\n🔗 Testando conexão com Telegram...")
    
    try:
        from telegram import Bot
        bot = Bot(token=TELEGRAM_CONFIG['BOT_TOKEN'])
        
        # Testar bot
        bot_info = await bot.get_me()
        print(f"✅ Bot conectado: @{bot_info.username}")
        
        # Testar envio de mensagem
        await bot.send_message(
            chat_id=TELEGRAM_CONFIG['CHAT_ID'],
            text="🧪 Teste de conexão - Bot funcionando!"
        )
        print(f"✅ Mensagem de teste enviada para chat {TELEGRAM_CONFIG['CHAT_ID']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão com Telegram: {e}")
        return False

async def test_technical_analysis():
    """Testa cálculos de análise técnica"""
    print("\n📊 Testando análise técnica...")
    
    try:
        from trading_signals_bot import TradingSignalsBot
        bot = TradingSignalsBot()
        
        for symbol in TRADING_CONFIG['SYMBOLS'][:1]:  # Testar apenas o primeiro símbolo
            print(f"\n📈 Analisando {symbol}...")
            
            data = bot.get_crypto_data(symbol)
            if data is not None and len(data) > 50:
                # Calcular indicadores
                data['RSI'] = bot.calculate_rsi(data['Close'])
                data['EMA_9'] = bot.calculate_ema(data['Close'], bot.ema_fast)
                data['EMA_21'] = bot.calculate_ema(data['Close'], bot.ema_slow)
                
                # Mostrar valores atuais
                current = data.iloc[-1]
                print(f"  💰 Preço atual: ${current['Close']:.2f}")
                print(f"  📊 RSI: {current['RSI']:.1f}")
                print(f"  📈 EMA 9: ${current['EMA_9']:.2f}")
                print(f"  📈 EMA 21: ${current['EMA_21']:.2f}")
                
                # Verificar condições de sinal
                if current['RSI'] < bot.rsi_oversold:
                    print(f"  🟢 RSI em zona de sobrevenda ({current['RSI']:.1f} < {bot.rsi_oversold})")
                elif current['RSI'] > bot.rsi_overbought:
                    print(f"  🔴 RSI em zona de sobrecompra ({current['RSI']:.1f} > {bot.rsi_overbought})")
                else:
                    print(f"  ⚪ RSI em zona neutra ({current['RSI']:.1f})")
                
                if current['EMA_9'] > current['EMA_21']:
                    print(f"  📈 EMA 9 acima da EMA 21 (tendência de alta)")
                else:
                    print(f"  📉 EMA 9 abaixo da EMA 21 (tendência de baixa)")
                
                print(f"  ✅ Análise técnica funcionando para {symbol}")
            else:
                print(f"  ❌ Dados insuficientes para {symbol}")
                
    except Exception as e:
        print(f"❌ Erro na análise técnica: {e}")

async def main():
    """Função principal de teste"""
    print("🧪 TESTE DO BOT DE SINAIS DE TRADING")
    print("=" * 50)
    
    # Testar conexões
    await test_data_connection()
    telegram_ok = await test_telegram_connection()
    await test_technical_analysis()
    
    print("\n" + "=" * 50)
    print("📋 RESUMO DOS TESTES:")
    print(f"  📊 Yahoo Finance: Testado")
    print(f"  🔗 Telegram: {'✅ OK' if telegram_ok else '❌ Erro'}")
    print(f"  📈 Análise Técnica: Testado")
    
    if telegram_ok:
        print("\n🚀 Bot pronto para uso!")
        print("   Execute: python trading_signals_bot.py")
    else:
        print("\n⚠️  Verifique as configurações do Telegram em config.py")

if __name__ == "__main__":
    asyncio.run(main())
