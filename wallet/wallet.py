import binascii

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import json
import requests

from common.utils import calculate_hash
from common.transaction_input import TransactionInput
from common.transaction_output import TransactionOutput

# a user's Owner
class Owner:
    # takes
        # private_key - the user's private key
        # public_key_hash - hash of the user's public key (works as address)
        # public_key_hex - hex value of the user's public key
    def __init__(self, private_key: RSA.RsaKey, public_key_hash, public_key_hex):
        self.private_key = private_key
        self.public_key_hash = public_key_hash
        self.public_key_hex = public_key_hex


# initializes a wallet object using a randomly generated key pair
def initialize_owner():
    private_key = RSA.generate(2048)
    public_key = private_key.publickey().export_key("DER")
    public_key_hex = binascii.hexlify(public_key).decode("utf-8")
    public_key_hash = calculate_hash(calculate_hash(public_key_hex, hash_function="sh256"), hash_function="ripemd160")
    return Owner(private_key, public_key_hash, public_key_hex)

# any given transaction
class Transaction:
    # takes
        # owner - user creating the transaction (sender)
        # inputs - list of inputs
        # outputs - list of outputs
    def __init__(self, owner: Owner, inputs: list[TransactionInput], outputs: list[TransactionOutput]):
        self.owner = owner
        self.inputs = inputs
        self.outputs = outputs
    
    # generates signature required for input unlocking script
    def sign_transaction_data(self):
        tx_dict = {
            "inputs": [t.to_json(with_unlocking_script = False) for t in self.inputs],
            "outputs": [t.to_json() for t in self.outputs]
        }
        tx_bytes = json.dumps(tx_dict, indent = 2).encode('utf-8')
        return pkcs1_15.new(self.owner.private_key).sign(SHA256.new(tx_bytes))

    # adds unlocking script to the input transactions
    def sign(self):
        sig_hex = binascii.hexlify(self.sign_transaction_data()).decode("utf-8")
        for ti in self.inputs:
            ti.unlocking_script = f"{sig_hex} {self.owner.public_key_hex}"

    # formats transaction data for sending to node
    def send_to_nodes(self):
        return {
            "inputs": [i.to_json() for i in self.inputs],
            "outputs": [i.to_json() for i in self.outputs]
        }

# wallet/wallet.pyimport requestsclass Node:
    def __init__(self):
        ip = "127.0.0.1"
        port = 5000
        self.base_url = f"http://{ip}:{port}/"

    def send(self, transaction_data: dict) -> requests.Response:
        url = f"{self.base_url}transactions"
        req_return = requests.post(url, json=transaction_data)
        req_return.raise_for_status()
        return req_return


class Wallet:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.node = Node()

    def process_transaction(self, inputs: list[TransactionInput], outputs: list[TransactionOutput]) -> requests.Response:
        transaction = Transaction(self.owner, inputs, outputs)
        transaction.sign()
        return self.node.send({"transaction": transaction.transaction_data})