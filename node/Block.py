from datetime import datetime
from node.utils import calculate_hash, convert_transaction_data_to_bytes
import json

class Block:
    def __init__(self, transaction_data: str, previous_block=None):
        self.transaction_data = transaction_data
        self.timestamp = datetime.timestamp(datetime.datetime.fromtimestamp(datetime.now()))
        self.previous_block = previous_block
        
        def previous_block_cryptographic_hash(self):
            previous_block_cryptographic_hash = ""
            if self.previous_block:
                previous_block_cryptographic_hash = self.previous_block.cryptographic_hash
            return previous_block_cryptographic_hash

        def cryptographic_hash(self) -> str:
            block_content = {
                "transaction_data": self.transaction_data,
                "timestamp": self.timestamp,
                "previous_block_cryptographic_hash": self.previous_block_cryptographic_hash
            }
            block_content_bytes = json.dumps(block_content, indent=2).encode('utf-8')
            return calculate_hash(block_content_bytes)
