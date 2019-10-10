import math
# in_file = "test.txt"
in_file = "4char_100MB.dat"
out_file = "output100mb.txt"

x = 0 #dlugosc slownika
n = 0 #liczba bitów potrzebnych na znak
k = 0 #dlugosc tekstu
r = 0 #nadmiarowe bity
dictionary = [] #slownik

tem_dict = []
for i in range(255):
  tem_dict.append(0)

with open(in_file, "rb") as inp:
        while True:
            chunk = inp.read(1)
            if not chunk:
                break  # end of file
            tem_dict[ord(chunk)] = 1
            k += 1
        for i in tem_dict:
            if i == 1:
                x += 1
n = math.ceil(math.log(x,2))
r = (8-(3+k*n)%8)%8
inp.close()
print("Liczba znaków: " + str(x))
print("Liczba potrzebnych bitów na jeden znak: " + str(n))
print("Długość tekstu: " + str(k))
print("Nadmiarowe bity: " + str(r))

if x < 128:
    with open(out_file, "wb") as out:
        out.write(bytes([x])) #dlugosc slownika
        for i in range(255):
            if tem_dict[i] != 0:
                dictionary.append(chr(i))
                out.write(bytes([i])) #znak
        bits = 3
        out_byte = r
        with open(in_file, "rb") as inp:
            while True:
                chunk = inp.read(1)
                if not chunk:
                    if bits != 0:
                        out.write(bytes([(out_byte << r | 2**r-1)]))
                        # print(out_byte << r | 2**r-1) #dodanie na końcu statniego bitu z uzupelnieniem jedynkami
                        print("Kompresja zakończona")
                    break  # end of file
                for ch in range(len(dictionary)):
                    if chunk.decode() == dictionary[ch]:
                        bits += n
                        out_byte = out_byte << n | ch #dodanie z prawej strony bitow nowego znaku
                        if bits >= 8:
                            out.write(bytes([(out_byte >> (bits - 8))]))
                            # print((out_byte >> (bits - 8))) #wziecie 8 bitow
                            out_byte = out_byte & (~(255 << (bits - 8))) #usuniecie uzytych juz bitow (8 z lewej)
                            bits -= 8
        inp.close()
    out.close()
else:
    print("Nie da się skompresować")

# print(chr(int("01100000", 2)))
# with open("output.txt", "rb") as inp:
#         while True:
#             chunk = inp.read(1)
#             if not chunk:
#                 break  # end of file
#             print(ord(bytes(chunk).decode()))
#             print(bin(ord(bytes(chunk).decode())))