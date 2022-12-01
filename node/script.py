import json
import binascii
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
import copy

from common.utils import calculate_hash
from wallet.wallet import Transaction

# normal Stack class
class Stack:
    def __init__(self):
        self.elements = []
    
    def push(self, element):
        self.elements.append(element)
    
    def pop(self):
        return self.elements.pop()

# Stack created for use with transaction scripts.
    # Modeled after the Script language used by Bitcoin
class StackScript(Stack):
    # constructor; stores the current transaction data
    def __init__(self, transaction_data : Transaction):
        super().__init__()
        self.transaction_data = transaction_data
    
    # duplicate top item (which will be public key)
    def op_dup(self):
        pubK = self.pop()
        self.push(pubK)
        self.push(pubK)

    # hash top item using SHA256 and RIPEMD160
    def op_hash160(self):
        pubK = self.pop()
        self.push(calculate_hash(calculate_hash(pubK, func = "sha256"), func = "ripemd160"))

    # verify the top two items are equal
    def op_equal_verify(self):
        last_elem_1 = self.pop()
        last_elem_2 = self.pop()
        assert last_elem_1 == last_elem_2

    # check that unlocking script signature is valid
    def op_checksig(self):
        pubK = self.pop()
        sig = self.pop()
        sig_decoded = binascii.unhexlify(sig.encode('utf-8'))
        pubK_object = RSA.import_key(binascii.unhexlify(pubK.encode('utf-8')))
        transaction_hash = SHA256.new(json.dumps({
            "inputs": [i.to_json(with_unlocking_script=False) for i in self.transaction_data.inputs], "outputs": [o.to_json() for o in self.transaction_data.outputs]
            }, indent = 2).encode('utf-8'))
        pkcs1_15.new(pubK_object).verify(transaction_hash, sig_decoded)