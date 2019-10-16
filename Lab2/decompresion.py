import math
in_file = "plik_compressed.dat"
out_file = "morys_lorem.txt"

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

    with open(out_file, "w") as out:
        while bits >= n:
            ch = in_data >> (bits - n)
            out.write(dictionary[ch])
            # print("ch: ", dictionary[ch])
            in_data = in_data & (2 ** (bits - n) - 1)
            bits -= n

        while True:
            chunk = inp.read(1)
            if not chunk:
                while bits - r >= n:
                    ch = in_data >> (bits - n)
                    out.write(dictionary[ch])
                    # print("ch: ", dictionary[ch])
                    in_data = in_data & (2 ** (bits - n) - 1)
                    bits -= n
                print("Dekompresja zakończona")
                break  # end of file
            while bits >= n:
                ch = in_data >> (bits - n)
                out.write(dictionary[ch])
                # print("ch: ", dictionary[ch])
                in_data = in_data & (2 ** (bits - n) - 1)
                bits -= n
            if bits > 0:
                in_data = (in_data << 8) | int.from_bytes(chunk, byteorder='big')
            else:
                in_data = int.from_bytes(chunk, byteorder='big')
            bits += 8

out.close()
inp.close()
