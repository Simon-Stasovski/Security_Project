import binascii
import json

from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from transaction_input import TransactionInput
from transaction_output import TransactionOutput

from Block import Block
from script import StackScript
from wallet import Owner


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

class TransactionValidation:
    def __init__(self, blockchain: Block):
        self.blockchain = blockchain
        self.transaction_data = ""
        self.inputs = ""
        self.outputs = ""
    
    # receives a given transaction, saving the inputs and outputs to backing fields
    def receive(self, transaction : Transaction):
        self.transaction_data = transaction
        self.inputs = transaction.inputs
        self.outputs = transaction.outputs

    # add all totals from tx inputs and validate that they match the amount in the tx output
    def validate_funds(self):
        return self.get_total_amount_in_inputs() == self.get_total_amount_in_outputs()
    
    # calculates the total amount of the inputs
    def get_total_amount_in_inputs(self) -> int:
        total_in = 0
        for ti in self.inputs:
            transaction_data = self.get_transaction_from_utxo(ti.transaction_hash)
            utxo_amount = json.loads(transaction_data["outputs"][ti.output_index])["amount"]
            total_in += utxo_amount
        return total_in

    # calculates the total amount of the outputs
    def get_total_amount_in_outputs(self) -> int:
        total_out = 0
        for to in self.outputs:
            out_dict = to
            amount = out_dict.amount
            total_out += amount
        return total_out
    
    # gets a transaction from a given utxo
    def get_transaction_from_utxo(self, utxo_hash : str) -> dict:
        current_block = self.blockchain
        while current_block:
            if utxo_hash == current_block.transaction_hash:
                return current_block.transaction_data
            current_block = current_block.previous_block
    
    # validates a transaction's validity
    def validate(self):
        for ti in self.inputs:
            in_dict = ti
            ls = self.get_locking_script_from_utxo(in_dict.transaction_hash, in_dict.output_index)
            self.execute_script(in_dict.unlocking_script, ls)
            ti.unlocking_script = ""
    
    # gets the locking script from a given utxo
    def get_locking_script_from_utxo(self, utxo_hash : str, utxo_index : int):
        transaction_data = self.get_transaction_from_utxo(utxo_hash)
        return json.loads(transaction_data["outputs"][utxo_index])["locking_script"]
    
    # executes the unlocking/locking script to verify transaction validity - blindly calls the methods specified in the scripts
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
    
    def find_unspent_outputs(self, public_key):
        curr_block = self.blockchain
        inputs = {}
        outputs = []
        while curr_block != None:
            for i in curr_block.transaction_data["inputs"]:
                i = json.loads(i)
                if i["transaction_hash"] not in inputs: inputs[i["transaction_hash"]] = []
                inputs[i["transaction_hash"]].append(i)

            for o in range(0, len(curr_block.transaction_data['outputs'])):
                validOutput = True
                if curr_block.transaction_hash in inputs:
                    for i in inputs[curr_block.transaction_hash]:
                        if i['output_index'] == o:
                            inputs[curr_block.transaction_hash].remove(i)
                            validOutput = False
                            break

                if validOutput and json.loads(curr_block.transaction_data['outputs'][o])["public_key_hash"] == public_key:
                    outputs.append({
                        "hash": curr_block.transaction_hash,
                        "amount": json.loads(curr_block.transaction_data['outputs'][o])["amount"],
                        "index": o })
            
            curr_block = curr_block.previous_block
        
        return outputs