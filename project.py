import hashlib

class SBFCoinBlock:
    def __init__(self, previousBlockHash, transaction_list):
        self.previousBlockHash = previousBlockHash
        self.transaction_list = transaction_list
        
        self.block_data = "-".join(transaction_list) + '-' + previousBlockHash
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()


