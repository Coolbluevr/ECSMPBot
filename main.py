import discord
from discord.ext import commands
from mcstatus import JavaServer
import os
from dotenv import load_dotenv

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
status = server.status()
data = status.raw

online = data.get("players", {}).get("online", 0)
max_players = data.get("players", {}).get("max", "?")

        embed = discord.Embed(
            title="🎮 Minecraft Server Stats",
            color=0x00ff00
        )

        embed.add_field(name="Status", value="🟢 Online", inline=True)
        embed.add_field(
            name="Players",
            value=f"{online}/{max_players}",
            inline=True
        )
        embed.add_field(
            name="Ping",
            value=f"{round(status.latency)}ms",
            inline=True
        )

        await loading.edit(content=None, embed=embed)
        return

    except:
        pass

    try:
        ping = server.ping()

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
