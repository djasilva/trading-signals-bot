#!/usr/bin/env python3
"""
Script de configuração e instalação do Bot de Sinais de Trading
"""

import subprocess
import sys
import os

def install_requirements():
    """Instala as dependências necessárias"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatível")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requer Python 3.8+")
        return False

def create_directories():
    """Cria diretórios necessários"""
    directories = ['logs', 'charts', 'audio']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Diretório '{directory}' criado")

def test_telegram_connection():
    """Testa a conexão com o Telegram"""
    print("🔗 Testando conexão com Telegram...")
    try:
        import asyncio
        from telegram import Bot
        from config import TELEGRAM_CONFIG
        
        async def test_bot():
            bot = Bot(token=TELEGRAM_CONFIG['BOT_TOKEN'])
            try:
                await bot.get_me()
                print("✅ Conexão com Telegram OK")
                return True
            except Exception as e:
                print(f"❌ Erro na conexão com Telegram: {e}")
                return False
        
        return asyncio.run(test_bot())
    except Exception as e:
        print(f"❌ Erro ao testar Telegram: {e}")
        return False

def main():
    """Função principal de setup"""
    print("🚀 Configurando Bot de Sinais de Trading")
    print("=" * 50)
    
    # Verificar versão do Python
    if not check_python_version():
        return False
    
    # Criar diretórios
    create_directories()
    
    # Instalar dependências
    if not install_requirements():
        return False
    
    # Testar conexão com Telegram
    if not test_telegram_connection():
        print("⚠️  Aviso: Problema na conexão com Telegram")
        print("   Verifique o Bot Token e Chat ID em config.py")
    
    print("\n" + "=" * 50)
    print("✅ Setup concluído!")
    print("\n📋 Para executar o bot:")
    print("   python trading_signals_bot.py")
    print("\n📋 Para parar o bot:")
    print("   Ctrl+C")
    print("\n📋 Logs serão salvos em: trading_bot.log")
    
    return True

if __name__ == "__main__":
    main()
