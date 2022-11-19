from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import binascii
import json
import copy

from node.Block import Block
from transaction.transaction_input import TransactionInput
from transaction.transaction_output import TransactionOutput
from node.utils import calculate_hash
from node.script import StackScript

class NodeTransaction:
    def __init__(self, blockchain: Block):
        self.blockchain = blockchain
        self.transaction_data = ""
        self.signature = ""

    # validate each of the input's signatures
    def validate_signature(self):
        transaction_data = copy.deepcopy(self.transaction_data)
        for count, ti in enumerate(transaction_data["inputs"]):
            ti_dict = json.loads(ti)
            public_key = ti_dict.pop("public_key")
            sig = ti_dict.pop("signature")
            transaction_data["inputs"][count] = json.dumps(ti_dict)
            sig_decoded = binascii.unhexlify(sig.encode("utf-8"))
            public_key_bytes = public_key.encode("utf-8")
            public_key_object = RSA.import_key(binascii.unhexlify(public_key_bytes))
            transaction_bytes = json.dumps(transaction_data, indent = 2).encode('utf-8')
            transaction_hash = SHA256.new(transaction_bytes)
            pkcs1_15.new(public_key_object).verify(transaction_hash, sig_decoded)

    # add all totals from UTXOs and validate that they match the amount in the tx output
    def validate_funds(self):
        assert self.get_total_amount_in_inputs() == self.get_total_amount_in_outputs()
    
    def get_total_amount_in_inputs(self) -> int:
        total_in = 0
        for ti in self.inputs:
            in_dict = json.loads(ti)
            transaction_data = self.get_transaction_from_utxo(in_dict["transaction_hash"])
            utxo_amount = json.loads(transaction_data["outputs"][in_dict["output_index"]])["amount"]
            total_in += utxo_amount
        return total_in

    def get_total_amount_in_outputs(self) -> int:
        total_out = 0
        for to in self.outputs:
            out_dict = json.loads(to)
            amount = out_dict["amount"]
            total_out += amount
        return total_out

    # verify that UTXO's receiver address matches the sender's public key
    def validate_funds_are_owned_by_sender(self):
        for ti in self.inputs:
            in_dict = json.loads(ti)
            public_key = in_dict["public_key"]
            sender_public_key_hash = calculate_hash(calculate_hash(public_key, hash_function="sha256"), hash_function="ripemd160")
            transaction_data = self.get_transaction_from_utxo(in_dict["transaction_hash"])
            public_key_hash = json.loads(transaction_data["outputs"][in_dict["output_index"]])["public_key_hash"]
            # will throw AssertionError if false
            assert public_key_hash == sender_public_key_hash
    
    def get_transaction_from_utxo(self, utxo_hash : str) -> dict:
        current_block = self.blockchain
        while current_block:
            if utxo_hash == current_block.transaction_hash:
                return current_block.transaction_data
            current_block = current_block.previous_block
        
    def validate(self):
        for ti in self.inputs:
            in_dict = json.loads(ti)
            ls = self.get_locking_script_utxo(in_dict["transaction_hash"], in_dict["output_index"])
            self.execute_script(in_dict["unlocking_script"], ls)
    
    def get_locking_script_from_utxo(self, utxo_hash : str, utxo_index : int):
        transaction_data = self.get_transaction_from_utxo(utxo_hash)
        return json.loads(transaction_data["outputs"][utxo_index])["locking_script"]
    
    def execute_script(self, unlocking_script : str, locking_script : str):
        script_list = unlocking_script.split(" ")
        script_list.extend(locking_script.split(" "))
        stack_script = StackScript(self.transaction_data)
        for elem in script_list:
            if elem.startswith("OP"):
                class_method = getattr(StackScript, elem.lower())
                class_method(stack_script)
            else:
                stack_script.push(elem)