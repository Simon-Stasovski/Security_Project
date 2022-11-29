import json

# defines outputs for transactions, i.e. how much each address received
    ## if B receives 40 from A, then output is B=40 A=0
    ## B then sends 30 to C from the previous output, creating new outputs of B=10 C=30
class TransactionOutput:
    # takes
        # public_key_hash - hash of the user's public key
        # amount - amount received
    def __init__(self, public_key_hash : bytes, amount : int):
        self.amount = amount
        # based on Bitcoin's verification script. Bitcoin's script is written in the Script language, which will be kind of emulated here
            # to unlock the amount from a UTXO, the unlocking script (from txInput) is concatenated to the locking script. orders are then added to an empty Stack,
            # and run in pop() order (unlocking script in defined as "<signature> <publicKey (unhashed)>")
                # signature is added to Stack
                # unhashed pubK is added to Stack
                # OP_DUP duplicates the top Stack item (pubK)
                # OP_HASH_160 hashes the top Stack item, through Sh256 then RIPEMD160
                # hashed pubK is added to Stack
                # OP_EQUAL_VERIFY checks if the last 2 items match, fails otherwise
                # OP_CHECK_SIG hashes the tx's outputs, inputs, and script, then validates to the provided signature
        self.locking_script = f"OP_DUP OP_HASH160 {public_key_hash} OP_EQUAL_VERIFY OP_CHECKSIG"
    
    # converts the transaction output into a json string
    def to_json(self) -> str:
        return json.dumps({ "amount": self.amount, "locking_script": self.locking_script })