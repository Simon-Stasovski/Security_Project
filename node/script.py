import json
import binascii
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

from common.utils import calculate_hash

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
    def __init__(self, transaction_data : dict):
        super().__init__()
        for count, ti in enumerate(transaction_data["inputs"]):
            ti_dict = json.loads(ti)
            ti_dict.pop("unlocking_script")
            transaction_data["inputs"][count] = json.dumps(ti_dict)
        self.transaction_data = transaction_data
    
    # duplicate top item (which will be public key)
    def op_dup(self):
        pubK = self.pop()
        self.push(pubK)
        self.push(pubK)

    # hash top item using SHA256 and RIPEMD160
    def op_hash160(self):
        pubK = self.pop()
        self.push(calculate_hash(calculate_hash(pubK, hash_function = "sha256"), hash_function = "ripemd160"))

    # verify the top two items are equal
    def op_equalverify(self):
        last_elem_1 = self.pop()
        last_elem_2 = self.pop()
        assert last_elem_1 == last_elem_2

    # check that unlocking script signature is valid
    def op_checksig(self):
        pubK = self.pop()
        sig = self.pop()
        sig_decoded = binascii.unhexlify(sig.encode('utf-8'))
        pubK_object = RSA.import_key(binascii.unhexlify(pubK.encode('utf-8')))
        transaction_hash = SHA256.new(json.dumps(self.transaction_data, indent = 2).encode('utf-8'))
        pkcs1_15.new(pubK_object).verify(transaction_hash, sig_decoded)