"""Worker helper: write an image hash to the deployed contract."""
import json
from pathlib import Path
from web3 import Web3

ROOT = Path(__file__).resolve().parents[2]
info = json.loads((ROOT / "blockchain/scripts/contract_info.json").read_text())
CHAIN_URL = "http://172.20.10.5:8545"
w3 = Web3(Web3.HTTPProvider(CHAIN_URL))
w3.eth.default_account = w3.eth.accounts[0]
contract = w3.eth.contract(address=info["address"], abi=info["abi"])

def record_hash_to_chain(h: str) -> None:
    tx = contract.functions.logImage(h).transact()
    w3.eth.wait_for_transaction_receipt(tx)
    print("🔗  Logged", h[:10], "…")
