import binascii

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import json
import requests

from common.utils import calculate_hash
from common.transaction_input import TransactionInput
from common.transaction_output import TransactionOutput
from node.Block import Block

# a user's Owner


class Owner:
    def __init__(self, private_key: str = ""):
        if private_key:
            self.private_key = RSA.importKey(private_key)
        else:
            self.private_key = RSA.generate(2048)
        public_key = self.private_key.publickey().export_key("DER")
        self.public_key_hex = binascii.hexlify(public_key).decode("utf-8")
        self.public_key_hash = calculate_hash(
            calculate_hash(self.public_key_hex),
        )


# initializes a wallet object using a randomly generated key pair
def initialize_owner():
    private_key = RSA.generate(2048)
    public_key = private_key.publickey().export_key("DER")
    public_key_hex = binascii.hexlify(public_key).decode("utf-8")
    public_key_hash = calculate_hash(
        calculate_hash(public_key_hex, func="sh256"), func="ripemd160"
    )
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
            "inputs": [t.to_json(with_unlocking_script=False) for t in self.inputs],
            "outputs": [t.to_json() for t in self.outputs],
        }
        tx_bytes = json.dumps(tx_dict, indent=2).encode("utf-8")
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
            "outputs": [i.to_json() for i in self.outputs],
        }
        

class Node:
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
        self.balance = 0

    def process_transaction( self, inputs: list[TransactionInput], outputs: list[TransactionOutput] ) -> requests.Response:
        transaction = Transaction(self.owner, inputs, outputs)
        transaction.sign()
        return self.node.send({"transaction": transaction.transaction_data})

    def calculate_balance(self, block: Block):
        self.balance = 0

        while block is not None:

            outputsString = block.transaction_data["outputs"]
            inputsStrings = block.transaction_data["inputs"]

            outputs = []
            inputs = []

            for inputStrings in inputsStrings:
                inputs.append(inputStrings)

            for outputString in outputsString:
                outputs.append(outputString)

            prev_block = block.previous_block
            inputBy = False
            for i in inputs:
                while prev_block is not None:
                    if isinstance(i, TransactionInput): i = i.to_json()
                    if not isinstance(i, dict): i = json.loads(i)
                    if prev_block.transaction_hash == i["transaction_hash"]:
                        outputsPreviousStrings = prev_block.transaction_data["outputs"]

                        outputsPrevious = []

                        for outputPreviousStrings in outputsPreviousStrings:
                            outputsPrevious.append(json.loads(outputPreviousStrings))

                        if self.owner.public_key_hash == outputsPrevious[i["output_index"]]["public_key_hash"]:
                            self.balance -= outputsPrevious[i["output_index"]]["amount"]
                            inputBy = True
                        break
                    else: prev_block = prev_block.previous_block
                if not inputBy: break

            for output in outputs:
                if self.owner.public_key_hash == json.loads(output)["public_key_hash"]:
                    self.balance += json.loads(output)["amount"]

            block = block.previous_block


class Node:
    def __init__(self):
        ip = "127.0.0.1"
        port = 5000
        self.base_url = f"http://{ip}:{port}/"

    def send(self, transaction_data: dict) -> requests.Response:
        url = f"{self.base_url}transactions"
        req_return = requests.post(url, json=transaction_data)
        req_return.raise_for_status()
        return req_return