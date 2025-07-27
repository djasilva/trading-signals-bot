#!/usr/bin/env python3
"""
Script de inicialização do Bot de Sinais de Trading
"""

import os
import sys
import subprocess
import asyncio
from datetime import datetime

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    required_packages = [
        'yfinance', 'pandas', 'numpy', 'mplfinance', 
        'matplotlib', 'gtts', 'telegram', 'asyncio'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️  Pacotes faltando: {', '.join(missing_packages)}")
        print("Execute: pip install -r requirements.txt")
        return False
    
    print("✅ Todas as dependências estão instaladas!")
    return True

def check_config():
    """Verifica se o arquivo de configuração existe"""
    print("\n🔧 Verificando configurações...")
    
    if not os.path.exists('config.py'):
        print("❌ Arquivo config.py não encontrado!")
        return False
    
    try:
        from config import TELEGRAM_CONFIG, TRADING_CONFIG
        
        # Verificar configurações do Telegram
        if not TELEGRAM_CONFIG.get('BOT_TOKEN') or not TELEGRAM_CONFIG.get('CHAT_ID'):
            print("❌ Configurações do Telegram incompletas!")
            return False
        
        print("✅ Configurações OK!")
        return True
        
    except ImportError as e:
        print(f"❌ Erro ao importar configurações: {e}")
        return False

def create_log_file():
    """Cria arquivo de log se não existir"""
    log_file = 'trading_bot.log'
    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.write(f"# Log do Bot de Sinais - Iniciado em {datetime.now()}\n")
        print(f"📝 Arquivo de log criado: {log_file}")

def show_startup_info():
    """Mostra informações de inicialização"""
    print("\n" + "="*60)
    print("🤖 BOT DE SINAIS DE TRADING - BTC/ETH")
    print("="*60)
    print("📊 Ativos: BTC/USDT, ETH/USDT")
    print("⏰ Timeframe: 5 minutos")
    print("🔄 Verificação: A cada 1 minuto")
    print("📈 Indicadores: RSI + EMA 9/21 + Padrões de Reversão")
    print("📱 Alertas: Telegram (texto + gráfico + áudio)")
    print("🔗 Corretora: https://www.homebroker.com/pt/invest")
    print("="*60)

def show_controls():
    """Mostra controles do bot"""
    print("\n📋 CONTROLES:")
    print("  🟢 Para INICIAR: O bot iniciará automaticamente")
    print("  🔴 Para PARAR: Pressione Ctrl+C")
    print("  📊 Para LOGS: Verifique trading_bot.log")
    print("  🧪 Para TESTE: Execute python test_bot.py")
    print("\n⚠️  IMPORTANTE:")
    print("  • Mantenha o terminal aberto")
    print("  • Verifique sua conexão com internet")
    print("  • O bot roda 24/7 até ser interrompido")
    print("  • Sinais são enviados apenas quando TODOS os critérios são atendidos")

async def start_bot():
    """Inicia o bot principal"""
    try:
        print("\n🚀 Iniciando bot...")
        from trading_signals_bot import TradingSignalsBot
        
        bot = TradingSignalsBot()
        await bot.start()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Bot interrompido pelo usuário")
        print("✅ Desligamento seguro concluído")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        print("💡 Verifique os logs em trading_bot.log")

def main():
    """Função principal"""
    print("🔄 Preparando Bot de Sinais de Trading...")
    
    # Verificações pré-inicialização
    if not check_dependencies():
        print("\n❌ Falha na verificação de dependências")
        print("💡 Execute: python setup.py")
        return
    
    if not check_config():
        print("\n❌ Falha na verificação de configurações")
        return
    
    # Preparar ambiente
    create_log_file()
    
    # Mostrar informações
    show_startup_info()
    show_controls()
    
    # Confirmar inicialização
    print("\n" + "="*60)
    try:
        input("Pressione ENTER para iniciar o bot (ou Ctrl+C para cancelar)...")
    except KeyboardInterrupt:
        print("\n🚫 Inicialização cancelada pelo usuário")
        return
    
    # Iniciar bot
    print("\n🎯 Iniciando monitoramento...")
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print("\n👋 Até logo!")

if __name__ == "__main__":
    main()
