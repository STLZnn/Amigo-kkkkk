import os
import discord

# ==========================================
# CONFIGURAÇÃO E LÓGICA DO BOT DISCORD
# ==========================================
TOKEN = os.getenv("DISCORD_TOKEN")
DEFAULT_GIF_URL = "https://tenor.com/view/fernos6-ferno-la-lechuga-cursed-gif-20864361"
GIF_URL = os.getenv("GIF_URL", DEFAULT_GIF_URL).strip()
NORMAL_MARKER = os.getenv("NORMAL_MARKER", "-testar-")
WEBHOOK_MARKER = os.getenv("WEBHOOK_MARKER", "-testarw-")
WEBHOOK_NAME = "Reenvio"

if not TOKEN:
    raise RuntimeError(
        "A variável DISCORD_TOKEN não foi configurada. "
        "Adicione-a nas variáveis de inicialização (Startup) do painel."
    )

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready() -> None:
    print(f"Bot conectado como {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_message(message: discord.Message) -> None:
    # Nunca processe mensagens enviadas pelo próprio bot.
    if message.author == bot.user:
        return

    # Mensagens normais usam -testar-; mensagens de webhook usam -testarw-.
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
        print(
            "Sem permissão para listar/criar webhooks ou enviar mensagens "
            "neste canal."
        )
    except discord.HTTPException as error:
        print(f"Erro da API do Discord ao reenviar a mensagem: {error}")

# ==========================================
# INICIALIZAÇÃO DO BOT
# ==========================================
if __name__ == "__main__":
    bot.run(TOKEN)
