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


def huffman(file, file_informations: list) -> None:
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
            coded_char: str = dictionary[char]
            if len(bin_str) == 8:
                compressed_file.write(int(bin_str, 2).to_bytes(1, 'big'))
                bin_str = ''
                bin_str += coded_char
            elif len(bin_str) > 8:
                znak = int(bin_str[:8], 2)
                compressed_file.write(znak.to_bytes(1, 'big'))
                rest: str = bin_str[8:]
                bin_str = '' + rest + coded_char
            else:
                bin_str += coded_char

    for i in range(0, chars_left):
        bin_str += '0'

    compressed_file.write(int(bin_str, 2).to_bytes(1, 'big'))
    compressed_file.close()


def decompress_dict(chars_list: list) -> dict:
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
    bin_char: str = ''

    file_decompress = open('zdekompresowany.txt', 'w')

    for line in file:
        for i in line:
            if len(bin_char) != 0:
                # print(bin_char)
                if len(end_bytes) == 0:
                    end_bytes.append(int(bin_char[:3], 2))
                    bin_char = bin_char[3:]
                while len(bin_char) >= 2:
                    decoded_char: str = bin_char[:2]
                    file_decompress.write(dictionary[decoded_char])

            if dict_lenght != 0 and len(chars_list) < dict_lenght:
                chars_list.append(i)
                if len(chars_list) == dict_lenght:
                    dictionary = decompress_dict(chars_list)
                    continue

            if dict_lenght == 0:
                dict_lenght = i

            if len(dictionary) == dict_lenght:
                new_byte: str = str(bin(i))[2:]
                while len(new_byte) < 8:
                    new_byte = '0' + new_byte

                bin_char = bin_char + new_byte

    while len(bin_char) > end_bytes[0]:
        decoded_char = bin_char[:2]
        file_decompress.write(dictionary[decoded_char])
        bin_char = bin_char[2:]

    file_decompress.close()


#file_to_compress = open('do_kompresji.txt', 'rb')
#file_informations_list: list = update_file_informations(file_to_compress)
#file_to_compress.close()
#file_to_compress = open('do_kompresji.txt', 'rb')
#huffman(file_to_compress, file_informations_list)
#file_to_compress.close()

file_to_decompress = open('skompresowany.txt', 'rb')
dec_file(file_to_decompress)

