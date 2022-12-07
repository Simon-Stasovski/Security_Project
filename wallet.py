import binascii

from Crypto.PublicKey import RSA
import json

from utils import calculate_hash
from transaction.transaction_input import TransactionInput
from transaction.transaction_output import TransactionOutput
from Block import Block

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


class Wallet:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.balance = 0

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