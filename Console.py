text = input("prompt")
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

array = [sys.argv[1], sys.argv[2]]
print(array)
while True:
    userArray = [simon_username, jacob_username, chase_username]
    userPass = [simon_hash, jacob_hash, chase_hash]

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

    # print(f"you are now logged in as {usernameConsole}")
    # print(f"{hash_pass.digest()} {chase_hash.digest()}")
    # print(f"sh:  {simon_hash}  jh:  {jacob_hash}  ch:   {chase_hash}")
