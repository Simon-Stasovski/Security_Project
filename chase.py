import hashlib
from wallet.wallet import Owner, Wallet

private_key = b'0\x82\x04\xa4\x02\x01\x00\x02\x82\x01\x01\x00\xa1\x02M\xa7\x01A\x1e\xa0e\x11\x9f@\x07\x9b\x8e\x18\xb3\xf3Tj\x9a\xac\xb4\xa5\xfdy\xa1\x90\xcb\x05,]\xf8\xf4i\xd0\re\x9c\x98\x17\xa5\x9a$;\xc7\x81\xda\x15\xdf^\xd5\xcd\xe5(\x04Un(?\xa6 ]\x1cv\xc2\x90\xb32\xedAR6Dj\xd1/V\xa7\xf2\xb0nd\xfdU#r\xbcw_z\xc2\xd16|\xa7\x98\x16\xce\x01\t\x80\xa3:\x14\xb3\x95"Qn\x02>\x8aD\xd9\r[\xa9\xcf\xd3#\x1b\ni\xef\xe9\xe8-t\x89=\x04 \xfb\x8b\xb7\x96\x1b\xa0\xe5\xd0Mi}\x98\xb9f\x9e\\\r\xbc\xd8\x0b\x99B\xd6\xe7v\xe0\x89\xfb\xb5\xcd\xe7\xc1v\x84X\xfcw\x8bt!\xfd\xc0\xeb\xebn\x01\xc4\xb2_t\xde\xf4\xc4\x9b\x7f\xa7\xea\xce\xc5\x82\xfd\x03\x05Ap\xd5\xedl#\xbf\x9d9\xb8\xaf\xfa\x10N$\xa5"\xc1b\xa7\xe2\x01\x83Db\xb4\xe5\xbdU02{\xb6\x14\x90sX\xe7[\xb5#J\x12+F\x05Pq\x0e\x17\x8d\x03\x05X\xa0\xd8\xe2\xd5R\x83\x02\x03\x01\x00\x01\x02\x82\x01\x00\x05\xca\xb4\xebd\x86\xa8\xa8\xe1i\xdc^+\xc7\xe39-C\xfc\r\xe7\xa9}\xc8\x18\xd1\xa6\xc7\xb4\x1d\xe8\x06+]\xf3nz\x04\xe58\xade\x16!\xe6\x8a\x9b7\xb2\xa0\xb9\xe3\x1c\x08y\xc3\x8a%/\xcavY\xe4\xaf\x90\xf0\x17\xcfrn\ts\x01#\xbd\xe9\xefw\x81\x0c _\xa0?b\xb0\'@\xf3TZp\xa6\xa0\xfc\xa3\xf4\xbb!F\xf5F\x0c\xd9\x1a\x84\x89AVG\x8cJ\x1e\xa42`\xa2"\xfe(\\\xb3l\xd0\xf9\xc1\xe2\xc9\xad2\xe9\xbe\x91\x829\xdc\x8f\xe7n\xdfv\xbc\x81\nW\xd0\xf1"<9\xa22\xfc@?\xe5\xad:\xe9\xb1\xfdzOjx\r\xcbv\xc3C\n,\xf3\xb0u\x8e\x8c\x90\x90\xa4\xdbr\xe4\xc9f\xae\x1b\x99A]b\x98\x11\xc9Z\x9f\xb0^\x19 O\xd3\xda\x11NJ!\xd05\xa1\x92\x1c\xb8iFOn\xbd\xf4j\xbf\xc6\x81\xebV\x89Bu\xd4%z\xff\xf8$\xa3\xcdZ`n\x9e\xca\xddpj\xde\xba\x98\xfd\xa8\xc9\xe4;<?\xe6\xa5\x02\x81\x81\x00\xc6\xd0\xed\xa7 \x1eL\xb6\xfb\x05\xdb\xc3K\x96J8\xe3\xafKi\xbeB\x13! \x9b\x00\xa8\x94{s\xe4\x8f\xc1\xd1j\xb3TL\xeb\x9d\xf7\x8b\x8e\xf7\xe0\x8c\xff!\xd6:*\xbe\x8b\xe5\xeb\xf5\xac\x87\x95\xd3\xc1\xdb\xae\x14\x91\x00\xa1\xa7\x1ch\xb5\xf1\x80\xd6E\r\xa6\x1e\xd8H]\x8a\xb9Q\xe5 z\x80\x06\xd6\xa3Z\x18\xe3\xa6\xe1z\xa0\xff\x87TK\x19\xf2g \x9bQ@!>U\x0e\xdc\xad\xe82\x13\xd0\x97\x12-\xb5\x08\xa3\xa5\x07\x02\x81\x81\x00\xcfQ\x97$\x9e-\xb9\x9f\x7fs\x12\x9f\xedt\x17\xa1!\xec\x85c\r\xc4\x03\xfem\xfb%\xca\xf3i\xde=\xce\xf4D\xf1\x16$\x01\x9deA\x06?\xa2b\xff\xcd\x10\xec\x82\xdfb\xabL\xe5\x0b\xda4\xab\x03}a\xe9\x82\xcap\x0fV\x97\xce\xa1\xa1b\x95c5\xa2\x99\x90\x9aMA\x8dI;\x85\x96\xc3etwPw\xc5\xba\x89%$\xfe\x96O\xddaO\xd9\x1e\r\xcdH\xc2\xb2@\x0b\x8a\xcd\xd4\x05\xf8\xde\xd78\xb6\x04x\xd4#\xa5\x02\x81\x80CX\xd2\xa8"A!Kz\x8c\xe9|\xa6F*\xaeJ\xb2>\xa1{Iv\xa1j"\x17\x7f\x03\x8d.\x1c\xe6u\x892\xd3\xbcb\xb2\r\xb8\xa5\x15\xb0\xf1\xe7\xd1$\xed$\x97\x06$\xed\xa5\x98z\xf1\x12\xd7\xc0{a\xe4\xa5\x99\xc9(\x8a\x7f\r\xe2\xd8\xf9\xbc:{cGp{\xffY\xf7[\xde<\xa0\xd1\xb03uy\xa8\xe4\x06\xcd;lS\xb3B\x1do\xf7o\x1c-\xd1\xc3q\x11\xef\x0e\xe1\xfa\x1d\xbc\x88\x94$\x1cG\x8e\xbd\xa0Q\x02\x81\x81\x00\x86t\x0c\xc8\xd3\xc9%\xd4Z,\xc0\x0cvLO2\xd24y\xc1f\xe1\x14\x12\x033\xd9+\xc97\x84\xc9\xa3\x19jH\xcc\xaa\']\xf3\x97\xfb<s\xcd.\xc6\xc8\xce\n\x86c\x90b\xfb<\xf7\x94&\xc0\xc9\xa5!s\x10e"\x9do0\xb4D]\x123XJ\x8e\xbbhF\xe8W\x80\x02\x19>P\x94\xd0\xb6\xbc\xba \xc3<D\x99\xbc~\xb1g\n\xc0e8\x07\x8dv=\xc6\xaa\xa0\x91\xb1\xb1j\xfa\x1fS\x87U\x0c\x8blQ}\x02\x81\x81\x00\xa9\xdeM\xb8\xec\xba\x0c4,\xa8\xb0\xb3J\xc9\x19\xe9\x1f\x13z1\xb1\xdbI<\xa8%\x05\xf1\x80\xeb\x90\x8e\x8d\xc9\xb7\xbb\x19\xa64\xb5\xa1\xfb\xa4\xc9\xea\x1e6\xac\x82-7\xee0\xb6Mt\xf4\xd9\xcf\x7f\x91\xeb\xa4\xa3o{\x8fB\xc8\x05\xbe:qq\xcb\xd5cg\xa8<\x8e\xfc\x02\x7fFuE\xc4\xe6\xb9\x8fID\xb3\xadeG\x17\x01V\x00\x7fy\x8d\xee\x85\x8a\x87K~\x13\xb7\xbe\xd41\xcf\x8a\x18\x9eF@\x81\x08\x97Y\x9c\xf3\xb6'
public_key_hex = "30820122300d06092a864886f70d01010105000382010f003082010a0282010100a1024da701411ea065119f40079b8e18b3f3546a9aacb4a5fd79a190cb052c5df8f469d00d659c9817a59a243bc781da15df5ed5cde52804556e283fa6205d1c76c290b332ed415236446ad12f56a7f2b06e64fd552372bc775f7ac2d1367ca79816ce010980a33a14b39522516e023e8a44d90d5ba9cfd3231b0a69efe9e82d74893d0420fb8bb7961ba0e5d04d697d98b9669e5c0dbcd80b9942d6e776e089fbb5cde7c1768458fc778b7421fdc0ebeb6e01c4b25f74def4c49b7fa7eacec582fd03054170d5ed6c23bf9d39b8affa104e24a522c162a7e201834462b4e5bd5530327bb614907358e75bb5234a122b460550710e178d030558a0d8e2d552830203010001"
public_key_hash = "a45fd8eabc95603e1c85db6c402db772845e8cb8c08a87f68adcfa6a6615e651"
username = "chase"
password = "123456"
byte_input = password.encode()
hash_pass = hashlib.sha256(byte_input)
owner = Owner(private_key)
user_wallet = Wallet(owner)
