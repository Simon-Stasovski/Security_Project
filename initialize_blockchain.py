from datetime import datetime

from simon import private_key as simon_private_key
from jacob import private_key as jacob_private_key
from chase import private_key as chase_private_key
from common.transaction_input import TransactionInput
from common.transaction_output import TransactionOutput
from node.Block import Block
from wallet.wallet import Owner

simon_wallet = Owner(private_key=simon_private_key)
jacob_wallet = Owner(private_key=jacob_private_key)
chase_wallet = Owner(private_key=chase_private_key)


def blockchain():
    timestamp_0 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))
    input_0 = TransactionInput(transaction_hash="abcd1234",
                               output_index=0)
    output_0 = TransactionOutput(public_key_hash=b"Albert",
                                 amount=40)
    inputs = [input_0.to_json()]
    outputs = [output_0.to_json()]
    block_0 = Block(
        transaction_data={"inputs": inputs, "outputs": outputs},
        timestamp=timestamp_0
    )

    timestamp_1 = datetime.timestamp(datetime.fromisoformat('2011-11-30 00:05:23.111'))
    input_0 = TransactionInput(transaction_hash=block_0.transaction_hash,
                               output_index=0)
    output_0 = TransactionOutput(public_key_hash=jacob_wallet.public_key_hash,
                                 amount=30)
    output_1 = TransactionOutput(public_key_hash=simon_wallet.public_key_hash,
                                 amount=10)
    inputs = [input_0.to_json()]
    outputs = [output_0.to_json(), output_1.to_json()]

    block_1 = Block(
        transaction_data={"inputs": inputs, "outputs": outputs},
        timestamp=timestamp_1,
        previous_block=block_0
    )

    timestamp_2 = datetime.timestamp(datetime.fromisoformat('2011-11-30 00:05:13.222'))
    input_0 = TransactionInput(transaction_hash=block_1.transaction_hash,
                               output_index=1)
    output_0 = TransactionOutput(public_key_hash=chase_wallet.public_key_hash,
                                 amount=10)
    inputs = [input_0.to_json()]
    outputs = [output_0.to_json()]
    block_2 = Block(
        transaction_data={"inputs": inputs, "outputs": outputs},
        timestamp=timestamp_2,
        previous_block=block_1
    )

    timestamp_3 = datetime.timestamp(datetime.fromisoformat('2011-11-30 00:11:13.333'))
    input_0 = TransactionInput(transaction_hash=block_1.transaction_hash,
                               output_index=0)
    output_0 = TransactionOutput(public_key_hash=chase_wallet.public_key_hash,
                                 amount=5)
    output_1 = TransactionOutput(public_key_hash=jacob_wallet.public_key_hash,
                                 amount=25)
    inputs = [input_0.to_json()]
    outputs = [output_0.to_json(), output_1.to_json()]
    block_3 = Block(
        transaction_data={"inputs": inputs, "outputs": outputs},
        timestamp=timestamp_3,
        previous_block=block_2
    )
    return block_3