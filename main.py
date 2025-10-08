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

# Estratégia de Sinais - 24H - HORÁRIOS UTC (Render)
SINAIS_DIA = {
    # MANHÃ - UTC (Brasília -3h)
    "13:00": {"ativo": "ETH/USDT", "direcao": "VENDA", "prob": 84},  # 10:00 BR
    "14:00": {"ativo": "XRP/USDT", "direcao": "COMPRA", "prob": 91}, # 11:00 BR
    "15:00": {"ativo": "BTC/USDT", "direcao": "VENDA", "prob": 86},  # 12:00 BR
    "16:00": {"ativo": "ETH/USDT", "direcao": "COMPRA", "prob": 94}, # 13:00 BR
    
    # TARDE - UTC
    "17:00": {"ativo": "XRP/USDT", "direcao": "VENDA", "prob": 87},  # 14:00 BR
    "18:00": {"ativo": "BTC/USDT", "direcao": "COMPRA", "prob": 92}, # 15:00 BR
    "19:00": {"ativo": "ETH/USDT", "direcao": "VENDA", "prob": 84},  # 16:00 BR
    "20:00": {"ativo": "XRP/USDT", "direcao": "COMPRA", "prob": 89}, # 17:00 BR
    "21:00": {"ativo": "BTC/USDT", "direcao": "VENDA", "prob": 91},  # 18:00 BR
    "22:00": {"ativo": "ETH/USDT", "direcao": "COMPRA", "prob": 93}, # 19:00 BR
    
    # NOITE - UTC
    "00:00": {"ativo": "XRP/USDT", "direcao": "COMPRA", "prob": 88}, # 21:00 BR
    "01:00": {"ativo": "BTC/USDT", "direcao": "COMPRA", "prob": 85}, # 22:00 BR
    "02:00": {"ativo": "ETH/USDT", "direcao": "COMPRA", "prob": 90}, # 23:00 BR
    "03:00": {"ativo": "XRP/USDT", "direcao": "VENDA", "prob": 86},  # 00:00 BR
    
    # MADRUGADA - UTC
    "04:00": {"ativo": "BTC/USDT", "direcao": "VENDA", "prob": 82},  # 01:00 BR
    "05:00": {"ativo": "ETH/USDT", "direcao": "COMPRA", "prob": 83}, # 02:00 BR
    "06:00": {"ativo": "XRP/USDT", "direcao": "VENDA", "prob": 81},  # 03:00 BR
    "07:00": {"ativo": "BTC/USDT", "direcao": "COMPRA", "prob": 84}, # 04:00 BR
    "08:00": {"ativo": "ETH/USDT", "direcao": "VENDA", "prob": 82},  # 05:00 BR
    "09:00": {"ativo": "XRP/USDT", "direcao": "COMPRA", "prob": 83}, # 06:00 BR
    "12:00": {"ativo": "BTC/USDT", "direcao": "COMPRA", "prob": 92}, # 09:00 BR
}

def enviar_sinal_telegram(horario):
    """Envia sinal para o Telegram - NOVO FORMATO"""
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
            
            # ✅ NOVO FORMATO SOLICITADO
            mensagem = f"""✅ ATIVO {sinal['ativo']}
🕒 Horário: {horario}
🎯 Direção: {sinal['direcao']} {emoji}
⏰ Expiração: 5 min
📈 Probabilidade: {sinal['prob']}%

🕒 OP 2: {op2}
🕒 OP 3: {op3}"""
            
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

# 🚀 INICIAR TUDO CORRETAMENTE - VERSÃO DEFINITIVA
if __name__ == "__main__":
    print("🚀 INICIANDO SISTEMA COMPLETO...")
    
    # INICIAR BOT PRINCIPAL PRIMEIRO (na thread principal)
    print("🤖 INICIANDO BOT PRINCIPAL...")
    bot_thread = threading.Thread(target=iniciar_bot_principal)
    bot_thread.daemon = True
    bot_thread.start()
    print("✅ BOT PRINCIPAL INICIADO EM THREAD SEPARADA!")
    
    # Esperar 2 segundos para o bot estabilizar
    time.sleep(2)
    
    # DEPOIS iniciar servidor web (em outra thread)
    print("🌐 INICIANDO SERVIDOR WEB EM BACKGROUND...")
    web_thread = threading.Thread(target=run_web_server)
    web_thread.daemon = True
    web_thread.start()
    print("✅ SERVIDOR WEB INICIADO EM BACKGROUND!")
    
    print("🎉 SISTEMA COMPLETO INICIADO - AGUARDANDO SINAIS...")
    
    # Manter a thread principal viva
    try:
        while True:
            time.sleep(30)
            hora = get_horario_brasilia().strftime('%H:%M:%S')
            print(f"💓 Sistema ativo - {hora}")
    except KeyboardInterrupt:
        print("🛑 Sistema interrompido")
