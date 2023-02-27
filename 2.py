import math
import sys

total_belanja = input("Total belanja : ")
bayar = input("Pembeli bayar : ")

if int(bayar) < int(total_belanja):
    print("false, kurang bayar")
    sys.exit()

pecahan_uang = [
    100000,
    50000,
    20000,
    10000,
    5000,
    2000,
    1000,
    500,
    200,
    100
]

sisa = int(bayar) - int(total_belanja)
kembalian = int(math.floor(sisa/ 100)) * 100

print("\n")
print("kembalian : ",sisa)
print("dibulantkan menjadi ",kembalian)
print("\n")

arrays = list()
for idx, x in enumerate(pecahan_uang):
    if kembalian >= pecahan_uang[idx]:
        total_pecahan = int(kembalian / x)
        kembalian = kembalian - (total_pecahan * x)
        keys = {
            'index_pecahan': idx,
            'total': total_pecahan
        }
        arrays.append(keys)

print("pecahan uang : \n")
for idx, x in enumerate(arrays):
    satuan = "koin" if x["index_pecahan"] == 8 or x["index_pecahan"] == 9 else "lembar"
    print(x["total"], " ", satuan, pecahan_uang[x["index_pecahan"]])
