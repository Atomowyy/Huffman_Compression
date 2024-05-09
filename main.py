import math


def update_file_informations(file) -> list:
    file_informations: list = []
    k: int = 0
    unique_chars: set = set()

    for line in file:
        for char in line:
            k += 1
            unique_chars.add(char)

    x: int = len(unique_chars)
    n: int = math.ceil(math.log(x, 2))
    r: int = (8 - (3 + (k * n)) % 8) % 8
    dictionary: dict = create_dictionary(unique_chars, n)
    file_informations.append(dictionary)
    file_informations.append(r)
    print(f'X: {x}\nK: {k}\nR: {r}')
    return file_informations


def create_dictionary(uniq_chars: set, n: int) -> dict:
    coded_chars: dict = {}
    display_dict: dict = {}
    uniq_chars = sorted(uniq_chars)
    for i in uniq_chars:
        binary_id: str = str(bin(len(coded_chars)))[2:]
        while len(binary_id) < n:
            binary_id = '0' + binary_id
        coded_chars.update({i: binary_id})
        display_dict.update({chr(i): binary_id})
    print(f'Dictionary: {display_dict}')

    return coded_chars


def huffman(file, file_informations: list, przesuniecie) -> None:
    compressed_file = open('skompresowany.txt', 'wb')
    dictionary: dict = file_informations[0]
    chars_left: int = file_informations[1]
    compressed_file.write(len(dictionary).to_bytes(1, 'big'))

    for i in dictionary:
        compressed_file.write(i.to_bytes(1, 'big'))

    bin_str: str = ''
    chars_left_bin: str = bin(chars_left)[2:]

    while len(chars_left_bin) < 3:
        chars_left_bin = '0' + chars_left_bin

    bin_str += chars_left_bin

    for line in file:
        for char in line:
            #print('--------------')
            coded_char: str = dictionary[char]
            if len(bin_str) >=8:
                #print(f'bin_str {bin_str}')
                chr1 = bin_str[:8]
                reszta = bin_str[8:]
                #print(f'Pierwsze 8 znaków{chr1}')
                #print(f'xor: {xor}')
                #print(f'pozostałe znaki: {reszta}')

                xored = xor_cipher(chr1, xor)
                #print(f"Xored: {xored}")
                bin_str = xored + reszta
                #print(f'Nowy string : {bin_str}')

                znak = int(bin_str[:8], 2)

                znak = znak+przesuniecie
                while znak>255:
                    znak = znak-256


                compressed_file.write(znak.to_bytes(1, 'big'))
                rest: str = bin_str[8:]
                bin_str = '' + rest + coded_char
            else:
                bin_str += coded_char

    for i in range(0, chars_left):
        bin_str += '0'
    print(bin_str)
    bin_str = xor_cipher(bin_str, xor)
    print(bin_str)

    znak = int(bin_str,2)
    print(znak)
    znak = znak+przesuniecie
    while znak > 255:
        znak = znak - 256
    print(znak)
    compressed_file.write(znak.to_bytes(1, 'big'))
    compressed_file.close()

def decompress_dict(chars_list: list) -> dict:
    print(chars_list)
    n: int = math.ceil(math.log(len(chars_list), 2))
    dictionary: dict = {}

    for i in chars_list:
        char = chr(i)
        bin_char_id: str = bin(len(dictionary))[2:]

        while len(bin_char_id) < n:
            bin_char_id = '0' + bin_char_id
        dictionary.update({bin_char_id: char})

    return dictionary


def dec_file(file) -> None:
    dictionary: dict = {}
    dict_lenght: int = 0
    end_bytes: list = []
    chars_list: list = []
    reszta = ''
    xored = ''
    xored2 = ''

    file_decompress = open('zdekompresowany.txt', 'w')
    for line in file:
        for i in line:

            if len(xored) != 0:
                if len(end_bytes) == 0:
                    end_bytes.append(int(xored[:3], 2))
                    xored = xored[3:]

                ile_razy = len(xored)//n
                #print(f'xored: {xored}')
                for j in range(ile_razy):
                    decoded_char: str = xored[:n]
                    file_decompress.write(dictionary[decoded_char])
                    xored = xored[n:]
                xored2 = xored
                #print(f'reszta {xored2}')





            if dict_lenght == 0:
                dict_lenght = i
                continue
            if len(chars_list)<dict_lenght and dict_lenght!=0:
                chars_list.append(i)
            if len(dictionary) == 0 and len(chars_list)==dict_lenght:
                n: int = math.ceil(math.log(len(chars_list), 2))
                dictionary = decompress_dict(chars_list)
                continue


            if len(dictionary)!=0:
                odczytany_znak =str(bin(i)[2:])
                #print(f'Odczytany: {odczytany_znak}')
                while len(odczytany_znak)<8:
                    odczytany_znak = '0'+odczytany_znak


                #print(odczytany_znak)
                kopia = int(odczytany_znak, 2)
                kopia2 = kopia-przesuniecie
                while kopia2<0:
                    kopia2 += 256
                #print(kopia2)

                kopia3 = str(bin(kopia2)[2:])
                while len(kopia3)<8:
                    kopia3 = '0' + kopia3
                deszyfr = xor_cipher(str(kopia3), xor)
                #print(f'zdeszyfrowany str: {deszyfr}')
                xored = xored2 + xor_cipher(str(kopia3), xor)
                #print(xored)

    while len(xored) > end_bytes[0]:
        decoded_char = xored[:n]
        file_decompress.write(dictionary[decoded_char])
        xored = xored[n:]


    file_decompress.close()


def xor_cipher(str1, str2):
    xored = ''
    for i in range(0, len(str2)):
        xored += str(int(str1[i])^int(str2[i]))
    #print(xored)
    return xored


klucz: str = input("Podaj klucz do szyfrowania/deszyfrowania")

xor_litera = klucz[:1]
przesuniecie = int(klucz[1:])

xor = str(bin(ord(xor_litera)))[2:]
while len(xor) < 8:
    xor = '0'+xor
#kompresja

file_to_compress = open('do_kompresji.txt', 'rb')
file_informations_list: list = update_file_informations(file_to_compress)
file_to_compress.close()
file_to_compress = open('do_kompresji.txt', 'rb')
huffman(file_to_compress, file_informations_list, przesuniecie)
file_to_compress.close()


#dekompresja

file_to_decompress = open('skompresowany.txt', 'rb')
dec_file(file_to_decompress)