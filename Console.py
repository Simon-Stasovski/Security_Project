import sys
import hashlib

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


def login():
    login = False
    while login is False:

        usernameConsole = input("Please enter Username ")
        passwordConsole = input("Please enter Password ")

        containsUser = False
        index = -1
        for i in userArray:
            index += 1
            if usernameConsole.lower() == i:
                containsUser = True

        if containsUser:
            print("Username Found")

        byte_input = passwordConsole.encode()
        hash_pass = hashlib.sha256(byte_input)
        containsPass = False
        for j in userPass:
            if hash_pass.digest() == j.digest():
                containsPass = True

        if containsPass:
            print("Password Found")
        else:
            print("Password not found")

        if containsUser and containsPass:
            login = True

        if login:
            print(f"you are now logged in as {usernameConsole}")
            return index


loggedUser = login()
loggedUsersWallet = userWallets[loggedUser]
while True:
    print(f" Welcome {userArray[loggedUser]}")
    print("         Menu:        ")
    print(" Press 1 to log into a different user")
    print(" Press 2 to check current balance")
    print(" Press 3 to see transaction history")
    print(" Press 4 to perform a transaction")
    userInput = input("Your choice: ")

    if userInput == "1":
        loggedUser = login()

    elif userInput == "2":
        print("current balance")
        loggedUsersWallet.calculate_balance(blockchain())
        print(f"{loggedUsersWallet.balance}")

    elif userInput == "3":
        print("transaction history")

    elif userInput == "4":
        print("perform a transaction")

    else:
        print("Not a valid option")

# def get_ledger(most_recent_block : Block):
