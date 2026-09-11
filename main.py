import os
import discord
from flask import Flask
from threading import Thread

# ==========================================
# 1. SISTEMA WEB PARA MANTER O BOT ACORDADO
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "Bot Reenvio está online!"

def run_server():
    # O Render usa a porta 8080 por padrão se configurado nas variáveis
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_server)
    t.daemon = True  # Garante que a thread feche se o bot fechar
    t.start()

# ==========================================
# 2. CONFIGURAÇÃO E LÓGICA DO BOT DISCORD
# ==========================================
TOKEN = os.getenv("DISCORD_TOKEN")
DEFAULT_GIF_URL = "https://tenor.com/view/guy-punches-sunflowers-pvz-plants-vs-zombies-gif-6137659021579759562"
GIF_URL = os.getenv("GIF_URL", DEFAULT_GIF_URL).strip()
NORMAL_MARKER = os.getenv("NORMAL_MARKER", "-testar-")
WEBHOOK_MARKER = os.getenv("WEBHOOK_MARKER", "-testarw-")
WEBHOOK_NAME = "Reenvio"

if not TOKEN:
    raise RuntimeError(
        "A variável DISCORD_TOKEN não foi configurada. "
        "Adicione-a nas Environment Variables do Render ou do Pydroid."
    )

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready() -> None:
    print(f"Bot conectado como {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == bot.user:
        return

    marker = WEBHOOK_MARKER if message.webhook_id else NORMAL_MARKER
    if marker not in message.content:
        return

    conteudo = message.content.replace(marker, "", 1).strip()
    nome = message.author.name
    avatar_url = message.author.display_avatar.url
    canal = message.channel

    try:
        await message.delete()
    except discord.Forbidden:
        print("Sem permissão para apagar mensagens neste canal.")
        return
    except discord.HTTPException as error:
        print(f"Não foi possível apagar a mensagem: {error}")
        return

    try:
        webhooks = await canal.webhooks()
        webhook = discord.utils.get(webhooks, name=WEBHOOK_NAME)

        if webhook is None:
            webhook = await canal.create_webhook(name=WEBHOOK_NAME)

        partes = [conteudo] if conteudo else []
        if GIF_URL:
            partes.append(GIF_URL)

        await webhook.send(
            content="\n".join(partes),
            username=nome[:80],
            avatar_url=avatar_url,
            wait=False,
        )
    except discord.Forbidden:
        print("Sem permissão para listar/criar webhooks ou enviar mensagens neste canal.")
    except discord.HTTPException as error:
        print(f"Erro da API do Discord ao reenviar a mensagem: {error}")

# ==========================================
# 3. INICIALIZAÇÃO DO SISTEMA
# ==========================================
if __name__ == "__main__":
    keep_alive()  # Liga o servidor Flask em segundo plano
    bot.run(TOKEN)  # Inicia o bot usando a variável segura
