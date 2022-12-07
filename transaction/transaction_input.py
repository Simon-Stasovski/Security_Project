import json

# defines inputs for transactions, i.e. who's sending & how much they're sending
class TransactionInput:
    # takes
    # transaction_hash - the previous transaction's hash
    # output_index - index in the UTXO
    # unlocking_script - script that must be run to unlock the transaction funds
    def __init__( self, transaction_hash: str, output_index: int, unlocking_script: str = "" ):
        self.transaction_hash = transaction_hash
        self.output_index = output_index
        self.unlocking_script = unlocking_script

    # converts the transaction input into a json string
    def to_json(self, with_unlocking_script: bool = True) -> str:
        opt = {
            "transaction_hash": self.transaction_hash,
            "output_index": self.output_index,
        }
        if with_unlocking_script:
            opt["unlocking_script"] = self.unlocking_script
        return json.dumps(opt)
