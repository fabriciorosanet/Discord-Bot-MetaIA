import discord
from discord.ext import commands
from dotenv import load_dotenv
from meta_ai_api import MetaAI
import os

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

meta_ai = MetaAI()

def generate_meta_ai_response(prompt):
    try:
        response = meta_ai.prompt(message=prompt)
        return response.get('message', "Erro: resposta vazia")
    except Exception as e:
        return f"Erro ao gerar resposta: {e}"

def format_response(text):

    formatted_text = text

    # Regras de formatação: Adiciona negrito a títulos e cria listas
    # Converte linhas que parecem listas (ex: "- item") para marcadores do Discord
    lines = formatted_text.split("\n")
    for i, line in enumerate(lines):
        # Adiciona negrito para linhas que terminam com ":"
        if line.endswith(":"):
            lines[i] = f"**{line}**"
        # Adiciona marcador para listas começando com "-"
        elif line.strip().startswith("-"):
            lines[i] = f"- {line.strip()[1:].strip()}"
    formatted_text = "\n".join(lines)

    # Quebras de linha para melhor leitura
    formatted_text = formatted_text.replace("\n\n", "\n")  # Ajusta espaços em branco duplos
    return formatted_text

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mention in message.content:
        prompt = message.content.replace(bot.user.mention, "").strip()
        response = generate_meta_ai_response(prompt)

        formatted_response = format_response(response)

        for i in range(0, len(formatted_response), 2000):
            await message.channel.send(formatted_response[i:i + 2000])

bot.run(DISCORD_TOKEN)
