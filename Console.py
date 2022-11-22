text = input("prompt")
import sys
import hashlib

# print(sys.argv)

from wallet.wallet import Owner, Transaction

# owner = Owner()

# print(owner.self.private_key)

array = [sys.argv[1], sys.argv[2]]
print(array)

userArray = ["alice", "bob", "john"]

# Initialize the empty message using SHA-256
password1 = hashlib.sha256()
password2 = hashlib.sha256()
password3 = hashlib.sha256()
# Update the message using byte strings
password1.update(b"1234")
password2.update(b"420")
password3.update(b"1738")

# Print the message digest
# print(password1.digest())
# print(password2.digest())
# print(password3.digest())

userPass = [password1, password2, password3]
containsUser = False

for i in userArray:
    if array[0].lower() == i:
        containsUser = True


if containsUser:
    print("Username Found")


byte_input = array[1].encode()
hash_object = hashlib.sha256(byte_input)
