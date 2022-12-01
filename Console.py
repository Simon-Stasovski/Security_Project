import hashlib
import json
from datetime import datetime

from wallet.wallet import Transaction
from simon import username as simon_username
from jacob import username as jacob_username
from chase import username as chase_username
from jacob import hash_pass as jacob_hash
from simon import hash_pass as simon_hash
from chase import hash_pass as chase_hash
from simon import user_wallet as simon_wallet
from jacob import user_wallet as jacob_wallet
from chase import user_wallet as chase_wallet
from initialize_blockchain import blockchain
from node.Block import Block
from node.node import TransactionValidation
from common.transaction_input import TransactionInput
from common.transaction_output import TransactionOutput

userArray = [simon_username, jacob_username, chase_username]
userPass = [simon_hash, jacob_hash, chase_hash]
userWallets = [simon_wallet, jacob_wallet, chase_wallet]

# visualize Transaction History
# check balance()
# perform a transaction


def get_ledger(most_recent_block: Block, public_key: str):

    messages = []

    while most_recent_block is not None:
        setTimestamp = False

        inputsStrings = most_recent_block.transaction_data["inputs"]
        outputsString = most_recent_block.transaction_data["outputs"]

        inputs = []
        outputs = []

        for inputStrings in inputsStrings:
            inputs.append(inputStrings)

        for outputString in outputsString:
            outputs.append(outputString)

        prev_block = most_recent_block.previous_block
        inputBy = False
        for i in inputs:
            if isinstance(i, TransactionInput): i = i.to_json()
            if not isinstance(i, dict): i = json.loads(i)
            while prev_block is not None:
                if prev_block.transaction_hash == i["transaction_hash"]:
                    outputsPreviousStrings = prev_block.transaction_data["outputs"]

                    outputsPrevious = []

                    for outputPreviousStrings in outputsPreviousStrings:
                        outputsPrevious.append(json.loads(outputPreviousStrings))

                    if public_key == outputsPrevious[i["output_index"]]["public_key_hash"]:
                        messages.append("You payed " + str(outputsPrevious[i["output_index"]]["amount"]) + " NS Coin(s).")
                        setTimestamp = True
                        inputBy = True
                    
                    break
                else: prev_block = prev_block.previous_block
            if not inputBy: break

        for output in outputs:
            output = json.loads(output)
            if public_key == output["public_key_hash"]:
                setTimestamp = True
                messages.append("You received " + str(output["amount"]) + " NS Coin(s).")

        if setTimestamp: messages.append("Timestamp: " + str(datetime.fromtimestamp(most_recent_block.timestamp)))
        most_recent_block = most_recent_block.previous_block
    
    for m in messages[::-1]: print("\t" + m)


def login():
    login = False
    while login is False:

        usernameConsole = input("Please enter username: ")
        passwordConsole = input("Please enter password: ")

        containsUser = False
        index = -1
        for i in userArray:
            index += 1
            if usernameConsole.lower() == i:
                containsUser = True
                break

        byte_input = passwordConsole.encode()
        hash_pass = hashlib.sha256(byte_input)
        containsPass = False
        for j in userPass:
            if hash_pass.digest() == j.digest():
                containsPass = True

        if not containsPass:
            print("Password not found")

        if containsUser and containsPass:
            login = True

        if login:
            print(f"You are now logged in as {usernameConsole}")
            return index

loggedUser = login()
loggedUsersWallet = userWallets[loggedUser]
chain = blockchain()
while True:
    print(f"Welcome {userArray[loggedUser].capitalize()}")
    print("\tMenu")
    print("\t\tPress 1 to log into a different user")
    print("\t\tPress 2 to check current balance")
    print("\t\tPress 3 to see transaction history")
    print("\t\tPress 4 to perform a transaction")
    userInput = input("Your choice: ")

    # SOMETHING WRONG HERE
    if userInput == "1":
        loggedUser = login()
    elif userInput == "2":
        loggedUsersWallet.calculate_balance(chain)
        print(f"Current Balance: {loggedUsersWallet.balance} NS Coin")
        print()
    elif userInput == "3":
        print("Transaction History:")
        get_ledger(chain, loggedUsersWallet.owner.public_key_hash)
        print()
    elif userInput == "4":
        print("Perform a Transaction:\n")
        pubK = input("Public Key of Recipient: ")
        # TODO: REMOVE
        if pubK == "simon": pubK = "8596618c5149d90896196ea16f3226ededec745f9c6593bc6a12eeb699c5a6c2"
        user_to_pay = None
        for user in userWallets:
            if pubK == user.owner.public_key_hash: user_to_pay = user

        if user_to_pay == None:
            print("Error: No user exists with that hash!")
            continue
        elif user_to_pay == loggedUsersWallet:
            print("Error: Cannot pay yourself!")
            continue
    
        value_to_pay = input("How much would you like to send: ")
        try:
            value = float(value_to_pay)
        except:
            print("Error: Please enter a number.")
            continue

        if value <= 0:
            print("Error: Coins cannot be negative!")
            continue

        validation = TransactionValidation(chain)
        utxo = validation.find_unspent_outputs(loggedUsersWallet.owner.public_key_hash)
        balance = 0
        for o in utxo: balance += o["amount"]
        if balance < value:
            print(f"Error: Insufficient funds. Current balance: {balance} NS Coins")
            continue

        balance = 0
        inputs = []
        for o in utxo:
            balance += o["amount"]
            inputs.append(TransactionInput(transaction_hash = o["hash"], output_index = o["index"]))
            if balance >= value: break
        
        print(type(inputs[0]))
        
        outputs = []
        outputs.append(TransactionOutput(pubK, value))
        if value != balance:
            outputs.append(TransactionOutput(loggedUsersWallet.owner.public_key_hash, balance - value))
        
        transaction = Transaction(loggedUsersWallet.owner, inputs, outputs)
        transaction.sign()
        try:
            validation.receive(transaction)
            validation.validate()
        except:
            print("Error: Failure accessing stored balance")
            continue
        
        if not validation.validate_funds():
            print("Error: Coins spent and coins distributed not equal.")
            continue

        chain = Block(
            timestamp = datetime.timestamp(datetime.now()),
            transaction_data = {
                "inputs": [i for i in transaction.inputs],
                "outputs": [o.to_json() for o in transaction.outputs]
                },
            previous_block = chain
        )

        print("Transaction executed successfully!")

    else:
        print("Not a valid option")
