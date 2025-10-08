from flask import Flask
import threading
import os
import requests
import schedule
import time
from datetime import datetime
import pytz

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
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHANNEL_ID = os.environ.get('TELEGRAM_CHANNEL_ID', '')

# Configurar fuso horário de São Paulo
timezone_brasil = pytz.timezone('America/Sao_Paulo')

esses aqui são os ativos e sinais! atualize o código!!!

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

def get_horario_brasilia():
    """Retorna o horário atual de Brasília"""
    return datetime.now(timezone_brasil)

def enviar_foto_sessao(url_foto, mensagem):
    """Envia foto da sessão para o Telegram"""
    try:
        print(f"📸 Enviando foto da sessão: {url_foto}")
        
        # Primeiro enviar a foto
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        payload = {
            "chat_id": TELEGRAM_CHANNEL_ID,
            "photo": url_foto,
            "caption": mensagem,
            "parse_mode": "Markdown"
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"✅ Foto enviada com sucesso!")
        else:
            print(f"❌ Erro ao enviar foto: {response.text}")
                
    except Exception as e:
        print(f"❌ Erro ao enviar foto: {e}")

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
🎯 *SINAL CONFIRMADO - FOREX* 🎯

💰 *Par: {sinal['ativo']}*
📊 *Direção: {sinal['direcao']}* {emoji}
⏰ *Horário: {horario}*
🎰 *Probabilidade: {sinal['prob']}%*

⚡ *ENTRADA IMEDIATA*
🎯 *Take Profit: 3-5 pips*
🛑 *Stop Loss: 1-2 pips*

🔄 *GALE 1: {segunda_chance}*
🔄 *GALE 2: {terceira_chance}*

📈 *MARTINGALE RECOMENDADO*

⚠️ *ALERTA DE RISCO: Opere com responsabilidade!*
🤖 *Sinal automático - DeepTrader Pro*
            """
            
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": TELEGRAM_CHANNEL_ID,
                "text": mensagem,
                "parse_mode": "Markdown"
            }
            
            print(f"📤 Tentando enviar sinal {horario}...")
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                hora_brasilia = get_horario_brasilia().strftime('%H:%M')
                print(f"✅ {hora_brasilia} - Sinal {horario} enviado com sucesso!")
            else:
                print(f"❌ Erro ao enviar sinal {horario}: {response.status_code} - {response.text}")
                
    except Exception as e:
        print(f"❌ Erro geral em {horario}: {e}")

def agendar_sinais():
    """Agenda todos os sinais do dia"""
    for horario in SINAIS_DIA.keys():
        schedule.every().day.at(horario).do(enviar_sinal_telegram, horario)
    print(f"⏰ {len(SINAIS_DIA)} sinais agendados!")
    
    # Mostrar próximos sinais
    hora_brasilia = get_horario_brasilia()
    print(f"🕐 Horário atual Brasília: {hora_brasilia.strftime('%H:%M')}")
    
    for horario in sorted(SINAIS_DIA.keys()):
        print(f"   📍 {horario} - {SINAIS_DIA[horario]['ativo']}")

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

def teste_conexao_telegram():
    """Testa a conexão com o Telegram"""
    print("🔍 Testando conexão com Telegram...")
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
        response = requests.get(url)
        
        if response.status_code == 200:
            print("✅ Conexão com Telegram: OK")
            return True
        else:
            print(f"❌ Erro na conexão Telegram: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no teste de conexão: {e}")
        return False

def enviar_mensagem_inicial():
    """Envia mensagem de inicialização"""
    try:
        hora_brasilia = get_horario_brasilia().strftime('%H:%M')
        mensagem = f"""🚀 *DEEPTRADER PRO ATIVADO!* 🚀

✅ *Sistema de Sinais Forex 24/7*
⏰ *Horário Brasília: {hora_brasilia}*
📊 *{len(SINAIS_DIA)} Sinais Diários*
💎 *Probabilidade 91-99%*

🎯 _Sistema configurado no fuso horário de São Paulo_
🤖 _DeepTrader Pro - Online 24/7_"""
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHANNEL_ID,
            "text": mensagem,
            "parse_mode": "Markdown"
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Mensagem inicial enviada com sucesso!")
        else:
            print(f"❌ Erro ao enviar mensagem inicial: {response.text}")
    except Exception as e:
        print(f"❌ Erro no envio inicial: {e}")

def main():
    print("🤖 DEEPTRADER PRO BOT INICIADO NO RENDER!")
    print(f"📊 {len(SINAIS_DIA)} sinais/dia - FOREX 24H")
    
    # Mostrar horário atual
    hora_brasilia = get_horario_brasilia()
    print(f"🇧🇷 Fuso horário: Brasília - {hora_brasilia.strftime('%H:%M')}")
    
    # Testar conexão
    if teste_conexao_telegram():
        # Enviar mensagem inicial
        enviar_mensagem_inicial()
    else:
        print("❌ Não foi possível conectar ao Telegram. Verifique as variáveis de ambiente.")
    
    # Agendar tudo
    agendar_sinais()
    agendar_fotos_sessoes()
    
    print("⏰ Aguardando horários dos sinais e sessões...")
    
    # Loop principal
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)  # Verifica a cada 1 segundo para maior precisão
        except Exception as e:
            print(f"❌ Erro no loop principal: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main()
