import discord
from discord.ext import commands
from mcstatus import JavaServer

TOKEN = "MTUyMDkzODk1MTU4MDMxOTg4Ng.GwcBzF.mTZJvk9YczekSltYXdtkcI8ymubY29x64qlOME"

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

    try:
        server = JavaServer.lookup(f"{ip}:{port}")
        status = server.status()

        embed = discord.Embed(
            title="🎮 Minecraft Server Stats",
            color=0x00ff00
        )

        embed.add_field(name="Status", value="🟢 Online", inline=True)
        embed.add_field(
            name="Players",
            value=f"{status.players.online}/{status.players.max}",
            inline=True
        )
        embed.add_field(
            name="Ping",
            value=f"{round(status.latency)}ms",
            inline=True
        )

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send("🔴 Server is offline or unreachable.")

bot.run(TOKEN)
