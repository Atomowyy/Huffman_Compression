import math


def update_file_informations(file) -> dict:
    K: int = 0
    unique_chars: set = set()
    for line in file:
        for char in line:
            K += 1
            unique_chars.add(char)

    X: int = len(unique_chars)
    N: int = math.ceil(math.log(X, 2))
    #R need to be added

    print(unique_chars)
    print(X)
    print(K)
    print(N)
    return None


def huffman(file) -> None:
    pass


file_to_compress = open('do_kompresji.txt', 'r')
update_file_informations(file_to_compress)
file_to_compress.close()
