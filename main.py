import discord
from discord.ext import commands
from mcstatus import JavaServer
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

print("Token loaded:", TOKEN is not None)
print("Length:", len(TOKEN) if TOKEN else 0)
print("Starts with:", TOKEN[:10] if TOKEN else "None")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def serverstats(ctx):
    ip = "EternalCoreSMP.aternos.me"
    port = 25565

    loading = await ctx.send("⏳ Checking Eternal Core status...")

    server = JavaServer.lookup(f"{ip}:{port}")

    try:
        # Fast check (best for Aternos)
        ping = await asyncio.wait_for(
            asyncio.to_thread(server.ping),
            timeout=3
        )

        embed = discord.Embed(
            title="🎮 Minecraft Server Stats",
            color=0x00ff00
        )

        embed.add_field(name="Status", value="🟢 Online", inline=True)
        embed.add_field(name="Ping", value=f"{round(ping)}ms", inline=True)

    except asyncio.TimeoutError:
        embed = discord.Embed(
            title="🎮 Minecraft Server Stats",
            color=0xff0000
        )
        embed.add_field(name="Status", value="🔴 Offline (timeout)", inline=True)
        embed.add_field(name="Ping", value="N/A", inline=True)

    except Exception:
        embed = discord.Embed(
            title="🎮 Minecraft Server Stats",
            color=0xff0000
        )
        embed.add_field(name="Status", value="🔴 Offline", inline=True)
        embed.add_field(name="Ping", value="N/A", inline=True)

    await loading.edit(content=None, embed=embed)


bot.run(TOKEN)
