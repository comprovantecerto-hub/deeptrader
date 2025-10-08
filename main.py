from flask import Flask
import threading
import os
import requests
import schedule
import time
from datetime import datetime
import pytz

print("🚀 INICIANDO BOT - CÓDIGO URGENTE CORRIGIDO!")

# Servidor web simples para manter porta aberta
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 DEEPTRADER BOT ONLINE - SERVIDOR ATIVO!"

def run_web_server():
    """Executa servidor web em thread SEPARADA"""
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 Servidor web iniciando na porta {port}...")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# Configurações do Telegram
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHANNEL_ID = os.environ.get('TELEGRAM_CHANNEL_ID', '')

# Configurar fuso horário de São Paulo
timezone_brasil = pytz.timezone('America/Sao_Paulo')

def get_horario_brasilia():
    """Retorna o horário atual de Brasília"""
    agora = datetime.now(timezone_brasil)
    return agora

# Estratégia de Sinais - 24H - HORÁRIOS REAIS DE BRASÍLIA
SINAIS_DIA = {
    # MANHÃ - BRASÍLIA
    "10:00": {"ativo": "ETH/USDT", "direcao": "VENDA", "prob": 84},
    "11:00": {"ativo": "XRP/USDT", "direcao": "COMPRA", "prob": 91},
    "12:00": {"ativo": "BTC/USDT", "direcao": "VENDA", "prob": 86},
    "13:00": {"ativo": "ETH/USDT", "direcao": "COMPRA", "prob": 94},
    
    # TARDE - BRASÍLIA
    "14:00": {"ativo": "XRP/USDT", "direcao": "VENDA", "prob": 87},
    "15:00": {"ativo": "BTC/USDT", "direcao": "COMPRA", "prob": 92},
    "16:00": {"ativo": "ETH/USDT", "direcao": "VENDA", "prob": 84},
    "17:00": {"ativo": "XRP/USDT", "direcao": "COMPRA", "prob": 89},
    "18:00": {"ativo": "BTC/USDT", "direcao": "VENDA", "prob": 91},
    "19:00": {"ativo": "ETH/USDT", "direcao": "COMPRA", "prob": 93},
    
    # NOITE - BRASÍLIA
    "21:00": {"ativo": "XRP/USDT", "direcao": "COMPRA", "prob": 88},
    "22:00": {"ativo": "BTC/USDT", "direcao": "COMPRA", "prob": 85},
    "23:00": {"ativo": "ETH/USDT", "direcao": "COMPRA", "prob": 90},
    "00:00": {"ativo": "XRP/USDT", "direcao": "VENDA", "prob": 86},
    
    # MADRUGADA - BRASÍLIA
    "01:00": {"ativo": "BTC/USDT", "direcao": "VENDA", "prob": 82},
    "02:00": {"ativo": "ETH/USDT", "direcao": "COMPRA", "prob": 83},
    "03:00": {"ativo": "XRP/USDT", "direcao": "VENDA", "prob": 81},
    "04:00": {"ativo": "BTC/USDT", "direcao": "COMPRA", "prob": 84},
    "05:00": {"ativo": "ETH/USDT", "direcao": "VENDA", "prob": 82},
    "06:00": {"ativo": "XRP/USDT", "direcao": "COMPRA", "prob": 83},
    "09:00": {"ativo": "BTC/USDT", "direcao": "COMPRA", "prob": 92},
}

def enviar_sinal_telegram(horario):
    """Envia sinal para o Telegram"""
    try:
        if horario in SINAIS_DIA:
            sinal = SINAIS_DIA[horario]
            
            hora_brasilia = get_horario_brasilia().strftime('%H:%M')
            print(f"🎯 [{hora_brasilia}] ENVIANDO SINAL {horario} - {sinal['ativo']} {sinal['direcao']}")
            
            # Calcular OP 2 e OP 3
            hora = int(horario.split(":")[0])
            minuto = int(horario.split(":")[1])
            
            op2 = f"{hora:02d}:{minuto+5:02d}"
            op3 = f"{hora:02d}:{minuto+10:02d}"
            
            emoji = "🟢" if sinal["direcao"] == "COMPRA" else "🔴"
            
            mensagem = f"""🎯 *INICIANDO OPERAÇÃO AO VIVO* 🎯

💰 *Par: {sinal['ativo']}*
📊 *Direção: {sinal['direcao']}* {emoji}
⏰ *Horário: {horario}*
🎰 *Probabilidade: {sinal['prob']}%*

⚡ *ENTRADA IMEDIATA*
🔄 *OP 2: {op2}*
🔄 *OP 3: {op3}*

⚠️ *Opere com responsabilidade!*"""
            
            if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHANNEL_ID:
                print("❌ Variáveis de ambiente não configuradas!")
                return
            
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": TELEGRAM_CHANNEL_ID,
                "text": mensagem,
                "parse_mode": "Markdown"
            }
            
            print(f"📤 Enviando para Telegram: {sinal['ativo']} {sinal['direcao']}")
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                print(f"✅✅✅ SINAL {horario} ENVIADO COM SUCESSO! ✅✅✅")
            else:
                print(f"❌ ERRO {response.status_code}: {response.text}")
                
    except Exception as e:
        print(f"❌ ERRO CRÍTICO em {horario}: {e}")

def agendar_sinais():
    """Agenda todos os sinais do dia"""
    print("⏰ AGENDANDO SINAIS...")
    for horario in SINAIS_DIA.keys():
        schedule.every().day.at(horario).do(enviar_sinal_telegram, horario)
    print(f"✅ {len(SINAIS_DIA)} SINAIS AGENDADOS!")
    
    # Mostrar próximos sinais
    hora_brasilia = get_horario_brasilia()
    print(f"🇧🇷 HORÁRIO BRASÍLIA: {hora_brasilia.strftime('%d/%m/%Y %H:%M')}")
    
    print("📋 PRÓXIMOS SINAIS HOJE:")
    for horario in sorted(SINAIS_DIA.keys()):
        sinal = SINAIS_DIA[horario]
        print(f"   🕒 {horario} - {sinal['ativo']} - {sinal['direcao']} ({sinal['prob']}%)")

def testar_telegram():
    """Testa a conexão com Telegram"""
    print("🔍 TESTANDO CONEXÃO COM TELEGRAM...")
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHANNEL_ID:
        print("❌ VARIÁVEIS DE AMBIENTE NÃO CONFIGURADAS!")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print("✅ CONEXÃO TELEGRAM: OK")
            
            # Enviar mensagem de teste
            hora_brasilia = get_horario_brasilia().strftime('%H:%M')
            mensagem = f"🔧 *BOT RECONFIGURADO - TESTE* 🔧\n\n✅ Sistema corrigido\n🇧🇷 Horário: {hora_brasilia}\n📊 {len(SINAIS_DIA)} sinais agendados\n\n⚡ *PRÓXIMOS SINAIS:*\n• 11:00 - XRP/USDT - COMPRA\n• 12:00 - BTC/USDT - VENDA\n\n🤖 _Bot operacional!_"
            
            url_msg = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": TELEGRAM_CHANNEL_ID,
                "text": mensagem,
                "parse_mode": "Markdown"
            }
            response_msg = requests.post(url_msg, json=payload, timeout=10)
            
            if response_msg.status_code == 200:
                print("✅ MENSAGEM DE TESTE ENVIADA!")
            else:
                print(f"❌ ERRO AO ENVIAR TESTE: {response_msg.status_code}")
            
            return True
        else:
            print(f"❌ ERRO TELEGRAM: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ERRO NO TESTE: {e}")
        return False

def iniciar_bot_principal():
    """Função principal do bot - CORRIGIDA"""
    print("=" * 70)
    print("🤖 DEEPTRADER PRO BOT - SISTEMA PRINCIPAL INICIADO!")
    print(f"📊 {len(SINAIS_DIA)} SINAIS/ DIA - HORÁRIO BRASÍLIA")
    print("=" * 70)
    
    # Mostrar horário atual
    hora_brasilia = get_horario_brasilia()
    print(f"🇧🇷 HORÁRIO ATUAL: {hora_brasilia.strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Testar Telegram
    testar_telegram()
    
    # Agendar sinais
    agendar_sinais()
    
    print("🚀 BOT PRINCIPAL RODANDO - AGUARDANDO SINAIS...")
    print("💡 PRÓXIMO SINAL: 11:00 - XRP/USDT - COMPRA")
    
    # Loop principal do bot - AGORA FUNCIONANDO
    contador = 0
    while True:
        try:
            schedule.run_pending()
            contador += 1
            if contador % 30 == 0:  # Log a cada 30 segundos
                hora = get_horario_brasilia().strftime('%H:%M:%S')
                print(f"⏰ Bot ativo - {hora} - Aguardando sinais...")
            time.sleep(1)
        except Exception as e:
            print(f"❌ ERRO NO LOOP: {e}")
            time.sleep(10)

# 🚀 INICIAR TUDO CORRETAMENTE
if __name__ == "__main__":
    # Primeiro: iniciar servidor web em thread SEPARADA
    print("🌐 INICIANDO SERVIDOR WEB EM THREAD SEPARADA...")
    web_thread = threading.Thread(target=run_web_server)
    web_thread.daemon = True  # Permite que o programa termine se apenas esta thread estiver rodando
    web_thread.start()
    print("✅ SERVIDOR WEB INICIADO EM BACKGROUND!")
    
    # Esperar um pouco para o servidor iniciar
    time.sleep(2)
    
    # Segundo: iniciar o bot principal na thread PRINCIPAL
    print("🤖 INICIANDO BOT PRINCIPAL...")
    iniciar_bot_principal()
