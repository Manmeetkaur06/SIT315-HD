from pathlib import Path
import json
from solcx import compile_source
from web3 import Web3

SOLC = "/snap/bin/solc"
ROOT = Path(__file__).resolve().parents[2]

w3 = Web3(Web3.HTTPProvider("http://172.20.10.5:8545"))
w3.eth.default_account = w3.eth.accounts[0]       

source = (ROOT / "blockchain/contracts/ImageLog.sol").read_text()
compiled = compile_source(source, output_values=["abi", "bin"], solc_binary=SOLC, evm_version="london")
_, contract = compiled.popitem()

ImageLog = w3.eth.contract(abi=contract["abi"],
                           bytecode=contract["bin"])
tx_hash = ImageLog.constructor().transact()
address = w3.eth.wait_for_transaction_receipt(tx_hash).contractAddress
print("✅  ImageLog deployed at", address)

(ROOT / "blockchain/scripts/contract_info.json").write_text(
    json.dumps({"abi": contract["abi"], "address": address}, indent=2)
)
