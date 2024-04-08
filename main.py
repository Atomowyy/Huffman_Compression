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
    print(unique_chars)  # list of unique chars found in file to compress
    print(x)  # count of unique_chars elements
    print(k)  # count of chars in file to compress
    print(n)  # code lenght
    print(r)  # count of '0' to add at end of the file
    dictionary = create_dictionary(unique_chars, n)
    """file_informations.append()"""
    return None


def create_dictionary(uniq_chars: set, n: int) -> dict:
    coded_chars: dict = {}
    print(f'List of unique chars: {uniq_chars}, code lenght for single char is: {n}')
    for i in uniq_chars:
        print(i)

    return coded_chars


def huffman(file) -> None:
    pass


file_to_compress = open('do_kompresji.txt', 'r')
update_file_informations(file_to_compress)
file_to_compress.close()
