#https://pypi.org/project/discord-py-interactions/
import os
from interactions import Client, slash_command, ContextMenu
from dotenv import load_dotenv
from parseador import limpiar_html, split_text
from quran_patched import Quran
import asyncio
from interactions import OptionType

qur = Quran()

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = Client(token=TOKEN, prefix="/", sync_interactions=True, test_guilds=["1365328327505739918"])


@bot.event
async def on_ready():
    print(f"Conectado como {bot.me.name}")
    await bot.sync_commands()  # fuerza que los comandos se registren

@slash_command(name="latencia", description="te da una latencia")
async def ping(ctx):
    """
    Te dice la latencia del bot
    """
    await ctx.send(f"🏓 Pong con latencia: {bot.latency}")
@slash_command(
    name="capitulo_coran",
    description="Te da un versiculo del coran como respuesta",
    options=[
        {
            "name": "capitulo",
            "description": "Número del capítulo (1-114)",
            "type": OptionType.INTEGER,
            "required": True,
            "min_value": 1,
            "max_value": 114
        }
    ]
)
async def capitulo(ctx, capitulo: int):
    texto = await asyncio.to_thread(qur.get_chapter, capitulo)
    texto = limpiar_html(texto)
    
    partes = split_text(texto)
    
    # Envía la primera parte como respuesta inicial
    await ctx.send(partes[0])
    
    # Envía las partes restantes como mensajes separados (con un pequeño delay para evitar spam)
    for parte in partes[1:]:
        await ctx.send(parte)

@slash_command(
    name="capitulo_coran_español",
    description="Te da un versiculo del coran como respuesta",
    options=[
        {
            "name": "capitulo",
            "description": "Número del capítulo (1-114)",
            "type": OptionType.INTEGER,
            "required": True,
            "min_value": 1,
            "max_value": 114
        }
    ]
)
async def capituloEsp(ctx, capitulo:int):
    from translate import Translator

    await ctx.defer()

    texto = await asyncio.to_thread(qur.get_chapter, capitulo)
    texto = limpiar_html(texto)

    translator = Translator(from_lang="arabic", to_lang="spanish")
    texto = translator.translate(text=texto)
    
    partes = split_text(texto)
    
    # Envía la primera parte como respuesta inicial
    await ctx.send(partes[0])
    
    # Envía las partes restantes como mensajes separados (con un pequeño delay para evitar spam)
    for parte in partes[1:]:
        await ctx.send(parte)

asyncio.run(bot.start())