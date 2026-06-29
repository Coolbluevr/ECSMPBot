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

    loading = await ctx.send("⏳ Eternal Core is gathering stats...")

    server = JavaServer.lookup(f"{ip}:{port}")

    try:
        status = await asyncio.to_thread(server.status)
        data = status.raw

        # safer player handling (Aternos fix)
        players = data.get("players", {})

        online = players.get("online", 0)

        # Aternos often does NOT send max
        max_players = players.get("max")
        if max_players is None:
            max_players = 20  # fallback value

        embed = discord.Embed(
            title="🎮 Minecraft Server Stats",
            color=0x00ff00
        )

        embed.add_field(name="Status", value="🟢 Online", inline=True)
        embed.add_field(name="Players", value=f"{online}/{max_players}", inline=True)

        # latency safe handling
        ping = getattr(status, "latency", None)
        embed.add_field(
            name="Ping",
            value=f"{round(ping)}ms" if ping else "N/A",
            inline=True
        )

        await loading.edit(content=None, embed=embed)
        return

    except:
        try:
            ping = await asyncio.to_thread(server.ping)

            embed = discord.Embed(
                title="🎮 Minecraft Server Stats",
                color=0x00ff00
            )

            embed.add_field(name="Status", value="🟢 Online", inline=True)
            embed.add_field(name="Ping", value=f"{round(ping)}ms", inline=True)
            embed.add_field(name="Players", value="0/?", inline=True)

            await loading.edit(content=None, embed=embed)

        except:
            embed = discord.Embed(
                title="🎮 Minecraft Server Stats",
                color=0xff0000
            )

            embed.add_field(name="Status", value="🔴 Offline", inline=True)

            await loading.edit(content=None, embed=embed)


bot.run(TOKEN)
