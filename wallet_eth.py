from dotenv import load_dotenv
import os
from web3 import Web3

load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
ETH_WALLET = os.getenv("ETH_WALLET_ADDRESS")

if not ETH_WALLET:
    raise ValueError("ETH_WALLET_ADDRESS missing in .env")

w3 = Web3(Web3.HTTPProvider(INFURA_URL))
ETH_WALLET = Web3.to_checksum_address(ETH_WALLET)

def get_eth_balance():
    return w3.eth.get_balance(ETH_WALLET)

def eth_to_ether(wei_amount):
    return w3.from_wei(wei_amount, 'ether')
