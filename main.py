import os
import discord

# ==========================================
# CONFIGURAÇÃO E LÓGICA DO BOT DISCORD
# ==========================================
TOKEN = os.getenv("DISCORD_TOKEN")
DEFAULT_GIF_URL = "https://tenor.com/view/fernos6-ferno-la-lechuga-cursed-gif-20864361"
GIF_URL = os.getenv("GIF_URL", DEFAULT_GIF_URL).strip()

# Dicionário de comandos -> GIFs
# Para cada comando abaixo, são reconhecidas duas marcas:
# - -<comando>-   (para mensagens normais de usuários)
# - -<comando>w-  (para mensagens que vieram de webhooks)
# A variação com 'w' só é considerada quando message.webhook_id for verdadeiro.
COMMAND_GIFS = {
    "brolysoco": "https://klipy.com/gifs/punch-smash-1",
    "kokusen": "https://klipy.com/gifs/jjk-jjk-s2-12",
    "garpsoco": "https://klipy.com/gifs/monkey-d-garp-garp-the-fist-2",
    "muiesoco": "https://klipy.com/gifs/anime-punch-14",
    "makicounter": "https://klipy.com/gifs/maki-maki-zenin-13",
    "sendosoco": "https://klipy.com/gifs/sendo-ippo-5",
    "yujisoco": "https://klipy.com/gifs/yuji-itadori-yuji-1",
    "dekubarrage": "https://klipy.com/gifs/mha-memes-metal-gear-rising",
    "jolybarrage": "https://klipy.com/gifs/jolyne-kujo-jojo",
    "spbarrage": "https://klipy.com/gifs/star-platinum-the-world-jojo",
    "spzumbis": "https://klipy.com/gifs/star-platinum-jotaro-2",
    "sptaca": "https://klipy.com/gifs/star-platinum-jojos-3",
    "bestialtaca": "https://klipy.com/gifs/beast-titan-titan-bestial",
}

WEBHOOK_SUFFIX = "w"  # sufixo para a variação focada em webhooks
WEBHOOK_NAME = "Reenvio"

if not TOKEN:
    raise RuntimeError(
        "A variável DISCORD_TOKEN não foi configurada. "
        "Adicione-a nas variáveis de inicialização (Startup) do painel."
    )

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)


def _build_markers_for_message(is_webhook: bool):
    """
    Retorna um dict mapping marcador -> comando para o tipo de mensagem atual.
    Se is_webhook for True, retornará marcadores com o sufixo 'w' (webhook-only).
    Caso contrário, retornará marcadores sem o sufixo (normal text).
    """
    markers = {}
    for cmd in COMMAND_GIFS.keys():
        if is_webhook:
            marker = f"-{cmd}{WEBHOOK_SUFFIX}-"
        else:
            marker = f"-{cmd}-"
        markers[marker] = cmd
    return markers


@bot.event
async def on_ready() -> None:
    print(f"Bot conectado como {bot.user} (ID: {bot.user.id})")


@bot.event
async def on_message(message: discord.Message) -> None:
    # Nunca processe mensagens enviadas pelo próprio bot.
    if message.author == bot.user:
        return

    # Determina se a mensagem veio originalmente de um webhook.
    is_webhook_message = bool(message.webhook_id)
    # Constrói os marcadores válidos para esse tipo de mensagem
    valid_markers = _build_markers_for_message(is_webhook_message)

    # Procura o primeiro marcador válido presente na mensagem.
    found_marker = None
    found_command = None
    for marker, cmd in valid_markers.items():
        if marker in message.content:
            found_marker = marker
            found_command = cmd
            break

    # Se não houver marcador, nada a fazer.
    if not found_marker:
        return

    # Extrai o conteúdo removendo somente a primeira ocorrência do marcador.
    conteudo = message.content.replace(found_marker, "", 1).strip()

    # Dados do autor (nome/avatar) para repost via webhook
    nome = message.author.name
    # Alguns webhooks podem não expor avatar do author da forma esperada; usamos fallback quando necessário.
    avatar_url = None
    try:
        avatar_url = message.author.display_avatar.url
    except Exception:
        avatar_url = None

    canal = message.channel

    # Tenta apagar a mensagem original.
    try:
        await message.delete()
    except discord.Forbidden:
        print("Sem permissão para apagar mensagens neste canal.")
        return
    except discord.HTTPException as error:
        print(f"Não foi possível apagar a mensagem: {error}")
        return

    # Prepara o GIF para envio (usa o do comando, se houver; senão o DEFAULT_GIF_URL)
    gif_for_command = COMMAND_GIFS.get(found_command) or DEFAULT_GIF_URL

    try:
        webhooks = await canal.webhooks()
        webhook = discord.utils.get(webhooks, name=WEBHOOK_NAME)

        if webhook is None:
            webhook = await canal.create_webhook(name=WEBHOOK_NAME)

        partes = [conteudo] if conteudo else []
        if gif_for_command:
            partes.append(gif_for_command)

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
