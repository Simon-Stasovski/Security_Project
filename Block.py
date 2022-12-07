from utils import calculate_hash
import json

# each block in the chain
class Block:
    # takes
        # timestamp - time that the block was generated
        # previous_block - the previous block in the chain
        # transaction_data - transaction data stored in this block, as a string
    def __init__(self, timestamp: float, transaction_data: dict, previous_block = None):
        self.transaction_data = transaction_data
        self.previous_block = previous_block
        self.timestamp = timestamp
        
    # returns hash of this block's transaction
    @property
    def transaction_hash(self):
        transaction_bytes = json.dumps(self.transaction_data, indent=2).encode('utf-8')
        return calculate_hash(transaction_bytes)


    # returns the previous block's hash
    @property
    def previous_block_cryptographic_hash(self) -> str:
        previous_block_cryptographic_hash = ""
        if self.previous_block:
            previous_block_cryptographic_hash = self.previous_block.cryptographic_hash
        return previous_block_cryptographic_hash

    # returns the hash of this block's content
    @property
    def cryptographic_hash(self) -> str:
        block_content = {
            "transaction_data": self.transaction_data,
            "timestamp": self.timestamp,
            "previous_block_cryptographic_hash": self.previous_block_cryptographic_hash
        }
        return calculate_hash(json.dumps(block_content, indent=2).encode('utf-8'))