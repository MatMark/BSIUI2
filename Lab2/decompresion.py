import math
in_file = "4char_100MB.dat_compressed.dat"
out_file = "4char_100MB.dat_decompressed.dat"

x = 0 #dlugosc slownika
n = 0 #liczba bitów potrzebnych na znak
r = 0 #nadmiarowe bity
dictionary = [] #slownik

bits = 0
in_data = 0

with open(in_file, "rb") as inp:
    chunk = inp.read(1)
    if chunk:
        x = ord(chunk)
    n = math.ceil(math.log(x, 2))
    for i in range(x):
        chunk = inp.read(1)
        dictionary.append(chr(ord(chunk)))
    chunk = inp.read(1)
    in_data = int.from_bytes(chunk, byteorder='big') & 31 #ostatnie 5 bitów
    bits = 5
    r = int.from_bytes(chunk, byteorder='big') >> 5 #3 najstarsze bity

    print("Liczba znaków: ", x)
    print("Liczba potrzebnych bitów na jeden znak: ", n)
    print("Słownik: ", dictionary)
    print("Nadmiarowe bity: ", r)

    def compression():
        global in_data, bits, n
        ch = in_data >> (bits - n)
        out.write(dictionary[ch])
        # print("ch: ", dictionary[ch])
        in_data = in_data & (2 ** (bits - n) - 1)
        bits -= n

    with open(out_file, "w") as out:
        while bits >= n:
            compression()
        while True:
            chunk = inp.read(1)
            if not chunk:
                while bits - r >= n:
                    compression()
                print("Dekompresja zakończona")
                break  # end of file
            while bits >= n:
               compression()
            if bits > 0:
                in_data = (in_data << 8) | int.from_bytes(chunk, byteorder='big')
            else:
                in_data = int.from_bytes(chunk, byteorder='big')
            bits += 8

out.close()
inp.close()
