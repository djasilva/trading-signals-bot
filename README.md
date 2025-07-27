# 🤖 Bot de Sinais de Trading - BTC/ETH

Bot automatizado para detecção de sinais de compra e venda em tempo real para Bitcoin (BTC) e Ethereum (ETH), com envio de alertas via Telegram.

## 📋 Funcionalidades

### ⚡ Principais Recursos
- **Monitoramento 24/7** de BTC/USDT e ETH/USDT
- **Análise técnica automática** com RSI, médias móveis e padrões gráficos
- **Alertas via Telegram** com mensagem formatada, gráfico e áudio
- **Timeframe de 5 minutos** com verificação a cada 1 minuto
- **Prevenção de sinais duplicados**

### 🎯 Condições de Sinal
O bot só envia sinais quando **TODOS** os 3 critérios são atendidos:

1. **RSI**: Abaixo de 30 (compra) ou acima de 70 (venda)
2. **Médias Móveis**: Cruzamento da EMA 9 com EMA 21
3. **Padrão Gráfico**: Candle de reversão confirmado

### 📱 Conteúdo do Alerta
Cada sinal enviado contém:
- ✅ Confirmação de entrada
- 💹 Ativo (BTC/USDT ou ETH/USDT)
- ⏰ Horário de entrada
- ⌛ Horário de expiração (+1 minuto)
- 🧠 Análise técnica detalhada
- 📊 Gráfico com marcações visuais
- 🔊 Áudio com sinal de voz
- 🔗 Link da corretora Homebroker

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- Conexão com internet
- Bot do Telegram configurado

### 1. Clone ou baixe os arquivos
```bash
# Baixe todos os arquivos do projeto para uma pasta
```

### 2. Execute o setup automático
```bash
python setup.py
```

Este comando irá:
- Verificar a versão do Python
- Instalar todas as dependências
- Criar diretórios necessários
- Testar a conexão com o Telegram

### 3. Configuração Manual (se necessário)
Se preferir instalar manualmente:

```bash
pip install -r requirements.txt
```

## 🚀 Como Executar

### Iniciar o Bot
```bash
python trading_signals_bot.py
```

### Parar o Bot
Pressione `Ctrl+C` no terminal

## 📊 Tecnologias Utilizadas

- **Python 3.11+** - Linguagem principal
- **yfinance** - Cotações em tempo real do Yahoo Finance
- **pandas** - Manipulação de dados financeiros
- **mplfinance** - Geração de gráficos de candles
- **gTTS** - Síntese de voz para áudio
- **python-telegram-bot** - Integração com Telegram
- **asyncio** - Processamento assíncrono

## ⚙️ Configurações

### Arquivo `config.py`
Todas as configurações podem ser ajustadas no arquivo `config.py`:

```python
# Configurações de Trading
TRADING_CONFIG = {
    'SYMBOLS': ['BTC-USD', 'ETH-USD'],
    'TIMEFRAME': '5m',
    'CHECK_INTERVAL': 60,  # segundos
    'RSI_PERIOD': 14,
    'EMA_FAST': 9,
    'EMA_SLOW': 21,
    'RSI_OVERSOLD': 30,
    'RSI_OVERBOUGHT': 70
}
```

### Telegram
As credenciais do Telegram já estão configuradas:
- **Bot Token**: 7629404700:AAHrY8g7DHyz3-iI6nAzorPdAMDcbLvYRkI
- **Chat ID**: 1065139183

## 📈 Lógica de Análise Técnica

### RSI (Relative Strength Index)
- **Período**: 14 candles
- **Sobrevenda**: RSI < 30 (sinal de compra)
- **Sobrecompra**: RSI > 70 (sinal de venda)

### Médias Móveis Exponenciais (EMA)
- **EMA Rápida**: 9 períodos
- **EMA Lenta**: 21 períodos
- **Sinal de Compra**: EMA 9 cruza acima da EMA 21
- **Sinal de Venda**: EMA 9 cruza abaixo da EMA 21

### Padrões de Reversão
- **Compra**: Candle verde após sequência de queda
- **Venda**: Candle vermelho após sequência de alta

## 📁 Estrutura de Arquivos

```
trading-signals-bot/
├── trading_signals_bot.py    # Bot principal
├── config.py                 # Configurações
├── requirements.txt          # Dependências
├── setup.py                 # Script de instalação
├── README.md                # Este arquivo
└── trading_bot.log          # Logs (criado automaticamente)
```

## 🔧 Logs e Monitoramento

### Arquivo de Log
- **Local**: `trading_bot.log`
- **Conteúdo**: Todas as atividades do bot
- **Formato**: Data/hora, nível, mensagem

### Exemplo de Log
```
2024-01-15 14:30:15 - INFO - Iniciando monitoramento de sinais...
2024-01-15 14:30:16 - INFO - Analisando BTC-USD...
2024-01-15 14:30:18 - INFO - Analisando ETH-USD...
2024-01-15 14:30:20 - INFO - Aguardando próxima verificação...
```

## 🚨 Exemplo de Sinal

```
✅ Entrada Confirmada
💹 Ativo: BTC/USDT
⏰ Entrada: 14:32:15
⌛ Expiração: 14:33:15
🧠 Análise: RSI + MME + Padrão gráfico
📘 Detalhes: RSI 28.5 < 30 + candle de reversão + cruzamento de MME
🟢 Sinal: COMPRA
💰 Preço: $43,250.00
📊 Gráfico anexado
🔗 https://www.homebroker.com/pt/invest
```

## ⚠️ Avisos Importantes

1. **Risco Financeiro**: Este bot é para fins educacionais. Trading envolve riscos.
2. **Teste Primeiro**: Teste em conta demo antes de usar com dinheiro real.
3. **Monitoramento**: Sempre monitore o desempenho do bot.
4. **Conexão**: Mantenha conexão estável com internet.
5. **Atualizações**: Verifique regularmente por atualizações.

## 🔮 Funcionalidades Futuras

- [ ] Backtest histórico
- [ ] Painel web de controle
- [ ] Mais indicadores técnicos
- [ ] Sinais manuais
- [ ] Alertas sonoros locais
- [ ] Histórico de performance

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs em `trading_bot.log`
2. Confirme se todas as dependências estão instaladas
3. Teste a conexão com internet e Telegram

## 📄 Licença

Este projeto é fornecido "como está" para fins educacionais.

---

**⚡ Bot desenvolvido para monitoramento automatizado de sinais de trading em BTC e ETH**
