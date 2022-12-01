import sys
import hashlib
import json
from datetime import datetime

# print(sys.argv)

from wallet.wallet import Owner, Transaction
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

userArray = [simon_username, jacob_username, chase_username]
userPass = [simon_hash, jacob_hash, chase_hash]
userWallets = [simon_wallet, jacob_wallet, chase_wallet]
# array = [sys.argv[1], sys.argv[2]]
# print(array)

# print(f"you are now logged in as {usernameConsole}")
# print(f"{hash_pass.digest()} {chase_hash.digest()}")
# print(f"sh:  {simon_hash}  jh:  {jacob_hash}  ch:   {chase_hash}")

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
            inputs.append(json.loads(inputStrings))

        for outputString in outputsString:
            outputs.append(json.loads(outputString))

        prev_block = most_recent_block.previous_block
        inputBy = False
        for i in inputs:
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

        #if containsUser:
            #print("Username Found")

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
while True:
    print(f"Welcome {userArray[loggedUser].capitalize()}")
    print("\tMenu")
    print("\t\tPress 1 to log into a different user")
    print("\t\tPress 2 to check current balance")
    print("\t\tPress 3 to see transaction history")
    print("\t\tPress 4 to perform a transaction")
    userInput = input("Your choice: ")

    if userInput == "1":
        loggedUser = login()

    elif userInput == "2":
        loggedUsersWallet.calculate_balance(blockchain())
        print(f"Current Balance: {loggedUsersWallet.balance} NaS Coin")
        print()
    elif userInput == "3":
        print("Transaction History:")
        get_ledger(blockchain(), loggedUsersWallet.owner.public_key_hash)
        print()
    elif userInput == "4":
        print("Perform a Transaction:")

    else:
        print("Not a valid option")
