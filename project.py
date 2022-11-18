import hashlib
import time

class SBFCoinBlock:
    def __init__(self, previous_hash, proof, index, data, timestamp = None):
        self.previous_hash = previous_hash      # hash of the previous block
        self.data = data                        # transaction list
        
        # full transaction list (including previous hash)
            ## fairly certain we don't need this, replaced with self.data
        #self.block_data = "-".join(transaction_list) + '-' + previous_hash

        self.timestamp = timestamp or time.time()       # timestamp of when the block was created
        self.index = index                              # index in the chain
        self.proof = proof                              # number created during block creation (mining)
        
        # this block's hash
        self.block_hash = self.calculate_hash() #hashlib.sha256(self.block_data.encode()).hexdigest()
    
    # calculate this block's hash
    def calculate_hash(self):
        string_block = "{}{}{}{}".format(self.index, self.proof, self.previous_hash, self.data, self.timestamp)
        return hashlib.sha256(string_block.encode()).hexdigest()
    
    # ToString
    def __repr__(self):
        return "{} - {} - {} - {} - {} - {}".format(self.index, self.proof, self.previous_hash, self.data, self.block_hash, self.timestamp)


class BlockChain:
    def __init__(self):
        self.chain = []             # stores the blocks
        self.current_data = []      # stores completed transactions not yet allocated to a block
        self.nodes = set()
        self.construct_genesis()
    
    # creates an initial block
    def construct_genesis(self):
        self.construct_block(proof_no = 0, prev_hash = 0)
    
    # creates a new block and adds it to the chain
        # self.current_data is transferred to a block, then wiped from the blockchain
    def construct_block(self, proof_no, prev_hash):
        block = SBFCoinBlock(
            previous_hash = prev_hash,
            data = self.current_data,
            proof = proof_no,
            index = len(self.chain)
        )

        self.current_data = []
        self.chain.append(block)
        return block
    
    # verifies that two chained blocks are valid (no tampering)
    @staticmethod
    def check_validity(block, prev_block):
        if prev_block.index + 1 != block.index:
            return False
        elif prev_block.block_hash != block.previous_hash:
            return False
        elif not BlockChain.verifying_proof(block.proof, prev_block.proof):
            return False
        elif block.timestamp <= prev_block.timestamp:
            return False
        
        return True
    
    # adds new transaction data to the blockchain list
    def new_data(self, sender, recipient, quantity):
        self.current_data.append({
            'sender': sender,
            'recipient': recipient,
            'quantity': quantity
        })
        return True
    
    # math to make it harder (computing-wise) to create/mine blocks, discouraging tampering with the blockchain
        # identifies a number g so that hash(fg) contains 4 leading zeroes
            # f is the previous g
            # g is the new proof
    @staticmethod
    def proof_of_work(last_proof):
        proof = 0
        while BlockChain.verifying_proof(proof, last_proof) is False:
            proof += 1
        
        return proof
    
    # calculates whether or not hash(gf) has 4 leading zeroes (see BlockChain:proof_of_work)
    @staticmethod
    def verifying_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'
    
    # return newest block
    @property
    def latest_block(self):
        return self.chain[-1]


    # MINING METHODS
    def block_mining(self, details_miner):
        self.new_data(
            sender = "0",                   # ie this node has created a new block
            receiver = details_miner,
            quantity = 1                    # creating a new block (identifying the proof number) is awarded 1 SBFCoin
        )

        last_block = self.latest_block
        last_proof = last_block.proof
        proof = self.proof_of_work(last_proof)

        last_hash = last_block.block_hash
        block = self.construct_block(proof, last_hash)

        return vars(block)
    
    # not sure what these two are for, but they were included in the resource i was using so i'm leaving them in
    def create_node(self, address):
        self.nodes.add(address)
        return True
    
    @staticmethod
    def obtain_block_object(block_data):
        return SBFCoinBlock(
            block_data['index'],
            block_data['proof'],
            block_data['previous_hash'],
            block_data['data'],
            timestamp = block_data['timestamp'])



# test code to verify correct implementation
blockchain = BlockChain()

print("=== Mining SBFCoin ===")
print(blockchain.chain)

last_block = blockchain.latest_block
last_proof = last_block.proof
proof = blockchain.proof_of_work(last_proof)

blockchain.new_data(
    sender = "0",
    recipient = "Jane Doe",
    quantity = 1
)

last_hash = last_block.block_hash
block = blockchain.construct_block(proof, last_hash)

print("=== Mining SBFCoin successful ===")
print(blockchain.chain)