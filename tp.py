from comp128.comp128v23 import Comp128v23
import numpy as np
import matplotlib.pyplot as plt
from pylfsr import A5_1
from a51 import A5_dec, A5_enc

ki = bytearray(bytes.fromhex("00112233445566778899AABBCCDDEEFF"))
rand = bytearray(bytes.fromhex("00112233445566778899AABBCCDDEEFF"))


v2_sres, v2_kc = Comp128v23().comp128v2(ki, rand)
v3_sres, v3_kc = Comp128v23().comp128v3(ki, rand)

print(f"v2 SRES: {v2_sres.hex()}, KC: {v2_kc.hex()}")
print(f"v3 SRES: {v3_sres.hex()}, KC: {v3_kc.hex()}")

c = A5_enc(b"Hello", v3_kc)
print(c)
p = A5_dec(c, v3_kc)
print(p)