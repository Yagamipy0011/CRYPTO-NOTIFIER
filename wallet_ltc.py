import requests
import os
from dotenv import load_dotenv

load_dotenv()
LTC_WALLET = os.getenv("LTC_WALLET_ADDRESS")

def get_ltc_balance():
    url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{LTC_WALLET}/balance"
    response = requests.get(url)
    data = response.json()
    return data.get("final_balance", 0) / 1e8  # Convert from satoshis to LTC
