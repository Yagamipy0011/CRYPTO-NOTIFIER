import discord
import asyncio
import os
from dotenv import load_dotenv

from wallet_eth import get_eth_balance, eth_to_ether
from wallet_ltc import get_ltc_balance
from wallet_btc import get_btc_balance
from price_fetcher import get_price

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

eth_last = None
ltc_last = None
btc_last = None

@bot.event
async def on_ready():
    global eth_last, ltc_last, btc_last
    print(f"✅ Bot is ready as {bot.user}")

    eth_last = get_eth_balance()
    ltc_last = get_ltc_balance()
    btc_last = get_btc_balance()

    bot.loop.create_task(monitor_eth_wallet())
    bot.loop.create_task(monitor_ltc_wallet())
    bot.loop.create_task(monitor_btc_wallet())

# --- ETH Monitor ---
async def monitor_eth_wallet():
    global eth_last
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print(f"[ETH Error] Channel ID {CHANNEL_ID} not found or bot lacks access.")
        return
    while True:
        try:
            curr = get_eth_balance()
            if curr > eth_last:
                diff = curr - eth_last
                eth_last = curr
                ether = eth_to_ether(diff)
                usd_price = get_price("ethereum")
                usd_value = float(ether) * usd_price if usd_price else "?"
                await channel.send(f"💸 Received {ether:.6f} ETH (~${usd_value:.2f} USD)")
        except Exception as e:
            print("[ETH Error]", e)
        await asyncio.sleep(20)

# --- LTC Monitor ---
async def monitor_ltc_wallet():
    global ltc_last
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print(f"[LTC Error] Channel ID {CHANNEL_ID} not found or bot lacks access.")
        return
    if ltc_last is None:
        ltc_last = get_ltc_balance()
    while True:
        try:
            curr = get_ltc_balance()
            if curr > ltc_last:
                diff = curr - ltc_last
                ltc_last = curr
                usd_price = get_price("litecoin")
                usd_value = float(diff) * usd_price if usd_price else "?"
                await channel.send(f"💰 Received {diff:.6f} LTC (~${usd_value:.2f} USD)")
        except Exception as e:
            print("[LTC Error]", e)
        await asyncio.sleep(30)

# --- BTC Monitor ---
async def monitor_btc_wallet():
    global btc_last
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print(f"[BTC Error] Channel ID {CHANNEL_ID} not found or bot lacks access.")
        return
    if btc_last is None:
        btc_last = get_btc_balance()
    while True:
        try:
            curr = get_btc_balance()
            if curr > btc_last:
                diff = curr - btc_last
                btc_last = curr
                usd_price = get_price("bitcoin")
                usd_value = float(diff) * usd_price if usd_price else "?"
                await channel.send(f"🟡 Received {diff:.6f} BTC (~${usd_value:.2f} USD)")
        except Exception as e:
            print("[BTC Error]", e)
        await asyncio.sleep(30)

bot.run(TOKEN)
