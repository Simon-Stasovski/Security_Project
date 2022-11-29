from Crypto.Hash import RIPEMD160, SHA256

# calculates the hash of data in SHA256 or RIPEMD160 (defaults to SHA256)
def calculate_hash(data, func: str = "sha256") -> str:
    if type(data) == str:
        data = bytearray(data, "utf-8")
    if func == "sha256":
        return SHA256.new().update(data).hexdigest()
    elif func == "ripemd160":
        return RIPEMD160.new().update(data).hexdigest()