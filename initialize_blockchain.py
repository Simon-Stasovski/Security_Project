from datetime import datetime

from transaction.transaction_input import TransactionInput
from transaction.transaction_output import TransactionOutput
from Block import Block
from simon import user_wallet as simon_wallet
from jacob import user_wallet as jacob_wallet
from chase import user_wallet as chase_wallet

# Creates fake transactions as a usable basis for the blockchain. First creates the genesis block.
# BYPASSES VALIDATION
def blockchain():
    timestamp_0 = datetime.timestamp(datetime.fromisoformat("2011-11-04 00:05:23.111"))
    input_0 = TransactionInput(transaction_hash="abcd1234", output_index=0)
    output_0 = TransactionOutput(public_key_hash="dummy", amount=40)
    inputs = [input_0.to_json()]
    outputs = [output_0.to_json()]
    block_0 = Block(transaction_data={"inputs": inputs, "outputs": outputs}, timestamp=timestamp_0)

    timestamp_1 = datetime.timestamp(datetime.fromisoformat("2011-11-30 00:05:23.111"))
    input_0 = TransactionInput(transaction_hash=block_0.transaction_hash, output_index=0)
    output_0 = TransactionOutput(public_key_hash=jacob_wallet.owner.public_key_hash, amount=30)
    output_1 = TransactionOutput(public_key_hash=simon_wallet.owner.public_key_hash, amount=10)
    inputs = [input_0.to_json()]
    outputs = [output_0.to_json(), output_1.to_json()]

    block_1 = Block(
        transaction_data={"inputs": inputs, "outputs": outputs},
        timestamp=timestamp_1,
        previous_block=block_0,
    )

    timestamp_2 = datetime.timestamp(datetime.fromisoformat("2011-11-30 00:05:13.222"))
    input_0 = TransactionInput(transaction_hash=block_1.transaction_hash, output_index=1)
    output_0 = TransactionOutput(public_key_hash=chase_wallet.owner.public_key_hash, amount=10)
    inputs = [input_0.to_json()]
    outputs = [output_0.to_json()]
    block_2 = Block(
        transaction_data={"inputs": inputs, "outputs": outputs},
        timestamp=timestamp_2,
        previous_block=block_1,
    )

    timestamp_3 = datetime.timestamp(datetime.fromisoformat("2011-11-30 00:11:13.333"))
    input_0 = TransactionInput(transaction_hash=block_1.transaction_hash, output_index=0)
    output_0 = TransactionOutput(public_key_hash=chase_wallet.owner.public_key_hash, amount=5)
    output_1 = TransactionOutput(public_key_hash=jacob_wallet.owner.public_key_hash, amount=25)
    inputs = [input_0.to_json()]
    outputs = [output_0.to_json(), output_1.to_json()]
    block_3 = Block(
        transaction_data={"inputs": inputs, "outputs": outputs},
        timestamp=timestamp_3,
        previous_block=block_2,
    )
    return block_3
