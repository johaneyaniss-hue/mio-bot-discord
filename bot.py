import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# Incolla qui la chiave presa da OpenRouter (inizia con sk-or-v1-...)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot IA online come {bot.user}! 🚀")

@bot.event
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if not message.content.startswith("!"):
            async with message.channel.typing():
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.post(
                            "https://openrouter.ai/api/v1/chat/completions",
                            headers={
                                "Authorization": f"Bearer {OPENROUTER_KEY}",
                                "Content-Type": "application/json",
                                "HTTP-Referer": "https://github.com",
                                "X-Title": "MioBotDiscord"
                            },
                            json={
                                "model": "openai/gpt-4o-mini",
                                "messages": [
                                    {"role": "user", "content": message.content}
                                ]
                            }
                        ) as response:
                            data = await response.json()

                    if "choices" in data and len(data["choices"]) > 0:
                        testo = data["choices"][0]["message"]["content"]
                        for i in range(0, len(testo), 1900):
                            await message.channel.send(testo[i:i+1900])
                    else:
                        print("Errore OpenRouter:", data)
                        await message.channel.send("Ops, errore nella risposta dall'IA.")
                except Exception as e:
                    await message.channel.send("Ops, c'è stato un errore nel codice!")
                    print(f"Errore preciso: {e}")


    await bot.process_commands(message)

# Il tuo Token Discord in fondo
# Comando per cancellare i messaggi (Moderazione)
# Comando per cancellare i messaggi (Moderazione)
@bot.command()
@commands.has_permissions(manage_messages=True)
async def pulisci(ctx, quantita: int = 5):
    await ctx.channel.purge(limit=quantita + 1)
    await ctx.send(f"Eliminati {quantita} messaggi!", delete_after=3)

# Comando di presentazione del Bot (Professionalità)
@bot.command()
async def info(ctx):
    embed = discord.Embed(
        title="🤖 Assistente IA Personalizzato",
        description="Bot integrato con Intelligenza Artificiale e strumenti di moderazione.",
        color=discord.Color.blue()
    )
    embed.add_field(name="Funzionalità", value="• Risposte IA automatiche\n• Moderazione canali (!pulisci)\n• Supporto h24", inline=False)
    embed.add_field(name="Sviluppatore", value="Progetto Custom Python", inline=False)
    await ctx.send(embed=embed)

bot.run(DISCORD_TOKEN)