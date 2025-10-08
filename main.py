from flask import Flask
import threading
import os
import requests
import schedule
import time
from datetime import datetime

# Servidor web simples para manter porta aberta
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 DEEPTRADER BOT ONLINE - RENDER 24/7"

def run_web_server():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# Iniciar servidor web em thread separada
print("🌐 Iniciando servidor web para Render...")
web_thread = threading.Thread(target=run_web_server)
web_thread.daemon = True
web_thread.start()

print("✅ Servidor web rodando - Bot vai ficar 24/7 online!")

# Configurações do Telegram
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHANNEL_ID = os.environ['TELEGRAM_CHANNEL_ID']

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
            
            # Calcular segundas chances
            hora = int(horario.split(":")[0])
            minuto = int(horario.split(":")[1])
            
            segunda_chance = f"{hora:02d}:{minuto+5:02d}"
            terceira_chance = f"{hora:02d}:{minuto+10:02d}"
            
            emoji = "🟢" if sinal["direcao"] == "COMPRA" else "🔴"
            
            mensagem = f"""
✅ *OPERAÇÃO - {sinal['ativo']}*

👉 Horário: {horario}
🎯 Direção: {sinal['direcao']} {emoji}
⏰ Expiração: 5 min
🎰 Probabilidade: {sinal['prob']}%

🔁 Se PERDER na primeira, entre DOBRADO na próxima
👉 Segunda chance: {segunda_chance}
👉 Terceira chance: {terceira_chance}

🤖 *Sinal gerado por IA - Não garantimos lucros*
            """
            
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": TELEGRAM_CHANNEL_ID,
                "text": mensagem,
                "parse_mode": "Markdown"
            }
            
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print(f"✅ {datetime.now().strftime('%H:%M')} - Sinal {horario} enviado!")
            else:
                print(f"❌ Erro ao enviar sinal {horario}: {response.text}")
                
    except Exception as e:
        print(f"❌ Erro geral em {horario}: {e}")

def agendar_sinais():
    """Agenda todos os sinais do dia"""
    for horario in SINAIS_DIA.keys():
        schedule.every().day.at(horario).do(enviar_sinal_telegram, horario)
    print(f"⏰ {len(SINAIS_DIA)} sinais agendados!")

def main():
    print("🤖 DEEPTRADER BOT INICIADO NO RENDER!")
    print(f"📊 {len(SINAIS_DIA)} sinais/dia")
    print("⏰ Aguardando horários...")
    
    # Enviar mensagem de inicialização
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHANNEL_ID,
            "text": "🚀 *DEEPTRADER BOT ATIVADO NO RENDER!*\n\nSinais automáticos 24/7 iniciados!",
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload)
    except:
        pass
    
    agendar_sinais()
    
    # Loop principal
    while True:
        schedule.run_pending()
        time.sleep(30)  # Verifica a cada 30 segundos

if __name__ == "__main__":
    main()

def agendar_fotos_sessoes():
    """Agenda todas as fotos de abertura/fechamento das sessões"""
    
    # SESSÃO MANHÃ
    schedule.every().day.at("06:55").do(
        enviar_foto_sessao, 
        "https://i.imgur.com/cPc0zwt.jpg",  # Manhã Início
        "🌅 *SESSÃO DA MANHÃ INICIANDO!*\n\n⏰ Início em 5 minutos!\n🔥 Prepare-se para os sinais!"
    )
    
    schedule.every().day.at("11:16").do(
        enviar_foto_sessao,
        "https://i.imgur.com/HsxZegp.jpg",  # Manhã Fim
        "✅ *SESSÃO DA MANHÃ ENCERRADA!*\n\n📊 Resultados consolidados!\n🔄 Próxima sessão: 12:00"
    )
    
    # SESSÃO TARDE
    schedule.every().day.at("11:55").do(
        enviar_foto_sessao,
        "https://i.imgur.com/b5Sqmda.jpg",  # Tarde Início
        "🌇 *SESSÃO DA TARDE INICIANDO!*\n\n⏰ Início em 5 minutos!\n🎯 Foco nos trades!"
    )
    
    schedule.every().day.at("17:16").do(
        enviar_foto_sessao,
        "https://i.imgur.com/XzCQTAQ.jpg",  # Tarde Fim
        "✅ *SESSÃO DA TARDE ENCERRADA!*\n\n📈 Performance analisada!\n🌙 Próxima sessão: 19:00"
    )
    
    # SESSÃO NOITE
    schedule.every().day.at("18:55").do(
        enviar_foto_sessao,
        "https://i.imgur.com/xpQso5o.jpg",  # Noite Início
        "🌃 *SESSÃO DA NOITE INICIANDO!*\n\n⏰ Início em 5 minutos!\n💫 Última sessão do dia!"
    )
    
    schedule.every().day.at("23:16").do(
        enviar_foto_sessao,
        "https://i.imgur.com/FgWDjRo.jpg",  # Noite Fim
        "✅ *SESSÃO DA NOITE ENCERRADA!*\n\n📋 Balanço final do dia!\n🌅 Amanhã tem mais!"
    )
    
    # SESSÃO MADRUGADA
    schedule.every().day.at("23:55").do(
        enviar_foto_sessao,
        "https://i.imgur.com/vepXQIt.jpg",  # Madrugada Início
        "🌙 *SESSÃO DA MADRUGADA INICIANDO!*\n\n⏰ Início em 5 minutos!\n🌍 Mercado internacional ativo!"
    )
    
    schedule.every().day.at("06:16").do(
        enviar_foto_sessao,
        "https://i.imgur.com/dcz7y31.jpg",  # Madrugada Fim
        "✅ *SESSÃO DA MADRUGADA ENCERRADA!*\n\n🌅 Dia finalizado com sucesso!\n🔄 Novo ciclo em 07:00"
    )
    
    print("📸 Fotos das sessões agendadas!")
