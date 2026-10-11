import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

# Inizializza il client di OpenRouter tramite la libreria OpenAI
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_KEY,
)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot IA online come {bot.user}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Se il messaggio NON inizia con !, risponde l'IA
    if not message.content.startswith("!"):
        async with message.channel.typing():
            try:
                # Chiamata pulita e ufficiale tramite la libreria openai
                completion = client.chat.completions.create(
                    model="openai/gpt-4o-mini",
                    messages=[
                        {"role": "user", "content": message.content}
                    ]
                )
                
                testo = completion.choices[0].message.content

                # Invia la risposta spezzandola se supera i 1900 caratteri
                for i in range(0, len(testo), 1900):
                    await message.channel.send(testo[i:i+1900])
                    
            except Exception as e:
                await message.channel.send("Ops, c'è stato un errore con l'IA!")
                print(f"Errore preciso: {e}")

    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def pulisci(ctx, quantita: int = 5):
    await ctx.channel.purge(limit=quantita + 1)
    await ctx.send(f"Eliminati {quantita} messaggi!", delete_after=3)

@bot.command()
async def info(ctx):
    embed = discord.Embed(
        title="Assistente IA Personalizzato",
        description="Bot integrato con Intelligenza Artificiale e strumenti di moderazione.",
        color=discord.Color.blue()
    )
    embed.add_field(name="Funzionalità", value="• Risposte IA automatiche\n• Moderazione canali (!pulisci)\n• Supporto h24", inline=False)
    embed.add_field(name="Sviluppatore", value="Progetto Custom Python", inline=False)
    await ctx.send(embed=embed)

bot.run(DISCORD_TOKEN)