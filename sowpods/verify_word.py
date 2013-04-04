from sowpods.dictionary import scrabble_dict

dictionary = frozenset(scrabble_dict)


def verify_word(word):
    return word in dictionary
