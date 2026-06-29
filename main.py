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
        # Try full status first (most accurate)
        status = await asyncio.wait_for(
            asyncio.to_thread(server.status),
            timeout=12
        )

        ping = getattr(status, "latency", None)

        embed = discord.Embed(
            title="🎮 Minecraft Server Stats",
            color=0x00ff00
        )
        embed.add_field(name="Status", value="🟢 Online", inline=True)
        embed.add_field(
            name="Ping",
            value=f"{round(ping)}ms" if ping else "N/A",
            inline=True
        )

    except asyncio.TimeoutError:
        # Aternos often sleeps or is starting up
        embed = discord.Embed(
            title="🎮 Minecraft Server Stats",
            color=0xffaa00
        )
        embed.add_field(
            name="Status",
            value="🟡 Starting / Sleeping",
            inline=True
        )
        embed.add_field(name="Ping", value="N/A", inline=True)

    except Exception:
        # Real failure (server offline or unreachable)
        embed = discord.Embed(
            title="🎮 Minecraft Server Stats",
            color=0xff0000
        )
        embed.add_field(name="Status", value="🔴 Offline", inline=True)
        embed.add_field(name="Ping", value="N/A", inline=True)

    await loading.edit(content=None, embed=embed)


bot.run(TOKEN)
