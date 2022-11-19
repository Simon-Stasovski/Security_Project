import binascii

import base58
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import json

from wallet.utils import generate_transaction_data, convert_transaction_data_to_bytes, calculate_hash
from transaction.transaction_input import TransactionInput
from transaction.transaction_output import TransactionOutput


class Owner:
    def __init__(self, private_key: RSA.RsaKey, public_key: bytes, address: bytes):
        self.private_key = private_key
        self.public_key = public_key
        self.address = address


def initialize_wallet():
    private_key = RSA.generate(2048)
    public_key = private_key.publickey().export_key()
    hash_1 = calculate_hash(public_key, hash_function="sha256")
    hash_2 = calculate_hash(hash_1, hash_function="ripemd160")
    address = base58.b58encode(hash_2)
    return Owner(private_key, public_key, address)


class Transaction:
    def __init__(self, owner: Owner, inputs: list[TransactionInput], outputs: list[TransactionOutput]):
        self.owner = owner
        self.inputs = inputs
        self.outputs = outputs
    
    def sign_transaction_data(self):
        transaction_dict = {
            "inputs": [t.to_json(with_signature_and_public_key = False) for t in self.inputs],
            "outputs": [t.to_json() for t in self.outputs]
        }
        transaction_bytes = json.dumps(transaction_dict, indent = 2).encode('utf-8')
        hash_object = SHA256.new(transaction_bytes)
        sig = pkcs1_15.new(self.owner.private_key).sign(hash_object)
        return sig

    def sign(self):
        sig_hex = binascii.hexlify(self.sign_transaction_data()).decode("utf-8")
        for ti in self.inputs:
            ti.signature = sig_hex
            ti.public_key = self.owner.public_key_hex

    def send_to_nodes(self):
        return {
            "sender_address": self.owner.address,
            "receiver_address": self.receiver_address,
            "amount": self.amount,
            "signature": self.signature
        }

# for A to send 5 to B:
    # UTXO means "unspent transaction outputs"
"""
utxo_0 = TransactionInput(transaction_hash = blockchain.transaction_hash, output_index = 0)
output_0 = TransactionOutput(public_key_hash = B_wallet.public_key_hash, amount = 5)
transaction = Transaction(A_wallet, inputs = [utxo_0], outputs = [output_0])
transaction.sign
"""