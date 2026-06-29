import discord
from discord.ext import commands
import minecraft_status

TOKEN = "YOUR_BOT_TOKEN"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def serverstats(ctx):
    ip = "YOUR_SERVER_IP"
    port = 25565

    try:
        status = minecraft_status.get_status(ip, port)

        embed = discord.Embed(
            title="🎮 Minecraft Server Stats",
            color=0x00ff00
        )

        embed.add_field(name="Status", value="🟢 Online", inline=True)
        embed.add_field(name="Players", value=f"{status['players']['online']}/{status['players']['max']}", inline=True)
        embed.add_field(name="Ping", value=f"{status['latency']}ms", inline=True)
        embed.add_field(name="Version", value=status["version"], inline=True)

        await ctx.send(embed=embed)

    except:
        await ctx.send("🔴 Server is offline or unreachable. you may need to ping a Server Starter to start the server")


bot.run(TOKEN)
