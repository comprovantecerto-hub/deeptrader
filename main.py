from flask import Flask
import threading
import os
import requests
import schedule
import time
from datetime import datetime
import pytz

print("🚀 INICIANDO BOT - CÓDIGO CORRIGIDO!")

# Servidor web simples para manter porta aberta
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 DEEPTRADER BOT ONLINE - RENDER 24/7 - BOT ATIVO!"

def run_web_server():
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 Servidor web na porta {port}")
    app.run(host='0.0.0.0', port=port)

# Configurações do Telegram
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHANNEL_ID = os.environ.get('TELEGRAM_CHANNEL_ID', '')

# Configurar fuso horário de São Paulo
timezone_brasil = pytz.timezone('America/Sao_Paulo')

def get_horario_brasilia():
    """Retorna o horário atual de Brasília"""
    return datetime.now(timezone_brasil)

# Estratégia de Sinais - 24H
SINAIS_DIA = {
    # MADRUGADA
    "00:00": {"ativo": "BTC/USDT", "direcao": "VENDA", "prob": 82},
    "01:00": {"ativo": "ETH/USDT", "direcao": "COMPRA", "prob": 83},
    "02:00": {"ativo": "XRP/USDT", "direcao": "VENDA", "prob": 81},
    "03:00": {"ativo": "BTC/USDT", "direcao": "COMPRA", "prob": 84},
    "04:00": {"ativo": "ETH/USDT", "direcao": "VENDA", "prob": 82},
    "05:00": {"ativo": "XRP/USDT", "direcao": "COMPRA", "prob": 83},
    
    # MANHÃ
    "07:00": {"ativo": "BTC/USDT", "direcao": "COMPRA", "prob": 92},
    "08:00": {"ativo": "ETH/USDT", "direcao": "VENDA", "prob": 84},
    "09:00": {"ativo": "XRP/USDT", "direcao": "COMPRA", "prob": 91},
    "10:00": {"ativo": "BTC/USDT", "direcao": "VENDA", "prob": 86},
    "11:00": {"ativo": "ETH/USDT", "direcao": "COMPRA", "prob": 94},
    
    # TARDE
    "12:00": {"ativo": "XRP/USDT", "direcao": "VENDA", "prob": 87},
    "13:00": {"ativo": "BTC/USDT", "direcao": "COMPRA", "prob": 92},
    "14:00": {"ativo": "ETH/USDT", "direcao": "VENDA", "prob": 84},
    "15:00": {"ativo": "XRP/USDT", "direcao": "COMPRA", "prob": 89},
    "16:00": {"ativo": "BTC/USDT", "direcao": "VENDA", "prob": 91},
    "17:00": {"ativo": "ETH/USDT", "direcao": "COMPRA", "prob": 93},
    
    # NOITE
    "19:00": {"ativo": "XRP/USDT", "direcao": "COMPRA", "prob": 88},
    "20:00": {"ativo": "BTC/USDT", "direcao": "COMPRA", "prob": 85},
    "21:00": {"ativo": "ETH/USDT", "direcao": "COMPRA", "prob": 90},
    "22:00": {"ativo": "XRP/USDT", "direcao": "VENDA", "prob": 86},
}

def enviar_sinal_telegram(horario):
    """Envia sinal para o Telegram"""
    try:
        if horario in SINAIS_DIA:
            sinal = SINAIS_DIA[horario]
            
            hora_brasilia = get_horario_brasilia().strftime('%H:%M')
            print(f"🎯 [{hora_brasilia}] Enviando sinal {horario} - {sinal['ativo']} {sinal['direcao']}")
            
            # Calcular segundas chances
            hora = int(horario.split(":")[0])
            minuto = int(horario.split(":")[1])
            
            segunda_chance = f"{hora:02d}:{minuto+5:02d}"
            terceira_chance = f"{hora:02d}:{minuto+10:02d}"
            
            emoji = "🟢" if sinal["direcao"] == "COMPRA" else "🔴"
            
            mensagem = f"""
🎯 *SINAL CONFIRMADO - CRYPTO* 🎯

💰 *Par: {sinal['ativo']}*
📊 *Direção: {sinal['direcao']}* {emoji}
⏰ *Horário: {horario}*
🎰 *Probabilidade: {sinal['prob']}%*

⚡ *ENTRADA IMEDIATA*
🔄 *GALE 1: {segunda_chance}*
🔄 *GALE 2: {terceira_chance}*

📈 *MARTINGALE RECOMENDADO*

⚠️ *Opere com responsabilidade!*
🤖 *DeepTrader Pro - ATIVO!*
            """
            
            if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHANNEL_ID:
                print("❌ Variáveis de ambiente não configuradas!")
                return
            
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": TELEGRAM_CHANNEL_ID,
                "text": mensagem,
                "parse_mode": "Markdown"
            }
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                print(f"✅ Sinal {horario} enviado com SUCESSO!")
            else:
                print(f"❌ Erro {response.status_code} ao enviar sinal {horario}")
                
    except Exception as e:
        print(f"❌ Erro em {horario}: {e}")

def agendar_sinais():
    """Agenda todos os sinais do dia"""
    for horario in SINAIS_DIA.keys():
        schedule.every().day.at(horario).do(enviar_sinal_telegram, horario)
    print(f"⏰ {len(SINAIS_DIA)} sinais agendados!")
    
    # Mostrar próximos sinais
    hora_brasilia = get_horario_brasilia()
    print(f"🕐 Horário atual: {hora_brasilia.strftime('%H:%M')} (Brasília)")
    
    print("📋 Próximos sinais hoje:")
    for horario in sorted(SINAIS_DIA.keys()):
        sinal = SINAIS_DIA[horario]
        print(f"   🕒 {horario} - {sinal['ativo']} - {sinal['direcao']} ({sinal['prob']}%)")

def iniciar_bot():
    """Função principal do bot"""
    print("=" * 60)
    print("🤖 DEEPTRADER PRO BOT - SISTEMA PRINCIPAL INICIADO!")
    print(f"📊 {len(SINAIS_DIA)} sinais/dia - FUSO BRASÍLIA")
    print("=" * 60)
    
    # Mostrar configuração
    hora_brasilia = get_horario_brasilia()
    print(f"🇧🇷 Horário Brasília: {hora_brasilia.strftime('%d/%m/%Y %H:%M')}")
    
    # Testar Telegram
    print("🔍 Testando Telegram...")
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHANNEL_ID:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
            response = requests.get(url)
            if response.status_code == 200:
                print("✅ Conexão Telegram: OK")
                
                # Enviar mensagem de inicialização
                mensagem = f"🚀 *BOT INICIADO!* 🚀\n\n✅ Sistema ativo\n🇧🇷 Horário: {hora_brasilia.strftime('%H:%M')}\n📊 {len(SINAIS_DIA)} sinais programados\n\n🤖 _DeepTrader Pro - Online!_"
                url_msg = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                payload = {
                    "chat_id": TELEGRAM_CHANNEL_ID,
                    "text": mensagem,
                    "parse_mode": "Markdown"
                }
                requests.post(url_msg, json=payload)
                print("✅ Mensagem de inicialização enviada!")
            else:
                print("❌ Problema com Telegram")
        except:
            print("⚠️  Erro no Telegram, mas bot continua...")
    else:
        print("❌ Variáveis de ambiente não configuradas")
    
    # Agendar sinais
    agendar_sinais()
    
    print("⏰ Bot principal rodando - Aguardando horários...")
    print("💡 Próximo sinal: 12:00 - XRP/USDT - VENDA")
    
    # Loop principal do bot
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print(f"❌ Erro no loop: {e}")
            time.sleep(30)

# Iniciar servidor web em thread separada
print("🌐 Iniciando servidor web em thread separada...")
web_thread = threading.Thread(target=run_web_server)
web_thread.daemon = True
web_thread.start()

print("✅ Servidor web rodando em background!")

# INICIAR O BOT PRINCIPAL
if __name__ == "__main__":
    iniciar_bot()
