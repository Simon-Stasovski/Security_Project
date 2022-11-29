import json

from node.Block import Block
from node.script import StackScript

class NodeTransaction:
    def __init__(self, blockchain: Block):
        self.blockchain = blockchain
        self.transaction_data = ""
        self.inputs = ""
        self.outputs = ""
    
    # receives a given transaction, saving the inputs and outputs to backing fields
    def receive(self, transaction : dict):
        self.transaction_data = transaction
        self.inputs = transaction["inputs"]
        self.outputs = transaction["outputs"]

    # add all totals from tx inputs and validate that they match the amount in the tx output
    def validate_funds(self):
        assert self.get_total_amount_in_inputs() == self.get_total_amount_in_outputs()
    
    # calculates the total amount of the inputs
    def get_total_amount_in_inputs(self) -> int:
        total_in = 0
        for ti in self.inputs:
            in_dict = json.loads(ti)
            transaction_data = self.get_transaction_from_utxo(in_dict["transaction_hash"])
            utxo_amount = json.loads(transaction_data["outputs"][in_dict["output_index"]])["amount"]
            total_in += utxo_amount
        return total_in

    # calculates the total amount of the outputs
    def get_total_amount_in_outputs(self) -> int:
        total_out = 0
        for to in self.outputs:
            out_dict = json.loads(to)
            amount = out_dict["amount"]
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
            in_dict = json.loads(ti)
            ls = self.get_locking_script_from_utxo(in_dict["transaction_hash"], in_dict["output_index"])
            self.execute_script(in_dict["unlocking_script"], ls)
    
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