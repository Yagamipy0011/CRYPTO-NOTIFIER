import requests
import os
from dotenv import load_dotenv

load_dotenv()
BTC_WALLET = os.getenv("BTC_WALLET_ADDRESS")

def get_btc_balance():
    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{BTC_WALLET}/balance"
    response = requests.get(url)
    data = response.json()
    return data.get("final_balance", 0) / 1e8  # Convert from satoshis to BTC
