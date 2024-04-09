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
    print(f'Dictionary: {unique_chars}\nX: {x}\nK: {k}\nR: {r}')
    return file_informations


def create_dictionary(uniq_chars: set, n: int) -> dict:
    coded_chars: dict = {}
    uniq_chars = sorted(uniq_chars)
    for i in uniq_chars:
        binary_id: str = str(bin(len(coded_chars)))[2:]

        while len(binary_id) < n:
            binary_id = '0' + binary_id

        coded_chars.update({i: binary_id})
    print(coded_chars)
    return coded_chars


def huffman(file, file_informations: list) -> None:
    compressed_file = open('skompresowane.txt', 'wb')
    dictionary: dict = file_informations[0]
    chars_left: int = file_informations[1]
    chars_left_bin: str = bin(chars_left)[2:]

    compressed_file.write(bytes(chars_left))
    #compressed_file.write(chr(chars_left))
    #for i in dictionary:
    #    compressed_file.write(i)

    bin_str: str = ''

    while len(chars_left_bin) < 3:
        chars_left_bin = '0' + chars_left_bin

    bin_str += chars_left_bin

    print(bin_str)

    for line in file:
        for char in line:
            coded_char: str = dictionary[char]
            if len(bin_str) == 8:
                #compressed_file.write(chr(int(bin_str, 2)))
                bin_str = ''
                bin_str += coded_char
            elif len(bin_str)>8:
                #print(bin_str[:8])
                znak = int(bin_str[:8], 2)
                #print(f"znak: {znak}")
                #compressed_file.write(chr(znak))
                rest: str = bin_str[8:]
                bin_str = '' + rest + coded_char
            else:
                bin_str += coded_char
    for i in range(0, chars_left):
        bin_str += '0'

    #print(bin_str)

    #compressed_file.write(chr(int(bin_str, 2)))
    compressed_file.close()

file_to_compress = open('do_kompresji.txt', 'r')
file_informations_list: list = update_file_informations(file_to_compress)
file_to_compress.close()

file_to_compress = open('do_kompresji.txt', 'r')
huffman(file_to_compress, file_informations_list)
file_to_compress.close()
