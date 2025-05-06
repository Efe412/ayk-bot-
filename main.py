import os
import discord
from discord.ext import commands
from discord import app_commands
from z_keep_alive import keep_alive
from dotenv import load_dotenv

load_dotenv()

TOKEN1 = os.getenv("TOKEN1")
TOKEN2 = os.getenv("TOKEN2")

LOG_CHANNEL_ID = 1363550415492481034
VOICE_CHANNEL_ID = 1362853864956629082

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True
intents.guilds = True

# İki botu da oluştur
bot1 = commands.Bot(command_prefix="!", intents=intents)
bot2 = commands.Bot(command_prefix="?", intents=intents)


# Ortak log fonksiyonu
async def log_command(bot,
                      interaction: discord.Interaction,
                      komut_adi: str,
                      extra: str = ""):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(
            title="📥 Yeni Komut Kullanımı",
            description=
            f"**{interaction.user.mention}** adlı kullanıcı bir komut kullandı!",
            color=discord.Color.gold(),
            timestamp=discord.utils.utcnow())
        embed.add_field(name="🧾 Komut", value=f"`{komut_adi}`", inline=False)
        if extra:
            embed.add_field(name="📄 Detaylar", value=extra, inline=False)
        embed.add_field(name="👤 Kullanıcı",
                        value=f"{interaction.user} (`{interaction.user.id}`)",
                        inline=False)
        embed.set_footer(text="JGK | Denetim Log Sistemi")
        await log_channel.send(embed=embed)


# BOT 1 ——————————————————————
@bot1.event
async def on_ready():
    print(f"[BOT 1] {bot1.user} olarak giriş yapıldı!")
    try:
        synced = await bot1.tree.sync()
        print(f"[BOT 1] {len(synced)} slash komutu senkronize edildi.")
    except Exception as e:
        print(f"[BOT 1] Sync hatası: {e}")

    channel = bot1.get_channel(VOICE_CHANNEL_ID)
    if channel:
        try:
            await channel.connect()
            print("[BOT 1] 🔊 Ses kanalına bağlanıldı.")
        except:
            print("[BOT 1] ❗ Zaten bağlı veya kanal hatalı.")
    else:
        print("[BOT 1] ❌ Ses kanalı bulunamadı.")


@bot1.tree.command(name="ping", description="Botun tepki süresini gösterir.")
async def ping(interaction: discord.Interaction):
    latency = bot1.latency * 1000
    embed = discord.Embed(title="🏓 Ping",
                          description=f"Gecikme: `{latency:.2f}ms`",
                          color=discord.Color.blue())
    await interaction.response.send_message(embed=embed, delete_after=5)


# BOT 2 ——————————————————————
@bot2.event
async def on_ready():
    print(f"[BOT 2] {bot2.user} olarak giriş yapıldı!")
    try:
        synced = await bot2.tree.sync()
        print(f"[BOT 2] {len(synced)} slash komutu senkronize edildi.")
    except Exception as e:
        print(f"[BOT 2] Sync hatası: {e}")


@bot2.tree.command(name="ping", description="Bot 2'nin ping komutu.")
async def ping2(interaction: discord.Interaction):
    latency = bot2.latency * 1000
    embed = discord.Embed(title="🏓 Ping 2",
                          description=f"Gecikme: `{latency:.2f}ms`",
                          color=discord.Color.green())
    await interaction.response.send_message(embed=embed)


# Keep alive ve botları başlat
keep_alive()
import asyncio

import os
bot.run(os.getenv("TOKEN"))
