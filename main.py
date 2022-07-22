# Wordle Solver
import os
from collections import Counter


def load_words():
    words = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/wordle_words.txt", "r") as f:
        for line in f:
            words.append(line[0:5])

    return words


def calculate_weights(words):
    characters = {}
    for word in words:
        for c in word:
            if c in characters:
                characters[c] += 1
            else:
                characters[c] = 1

    total_characters = sum(characters.values())
    highest_char_count = max(characters.values())
    highest_weight = highest_char_count/total_characters;

    weights = {
        c[0]: (c[1]/total_characters) / highest_weight for c in characters.items()
    }
    return weights


def calculate_word_weight(word, weights):
    weight = 0
    for c in word:
        weight += weights[c]

    # If unique characters increase weight
    freq = Counter(word)
    offset = 0
    for key, value in freq.items():
        offset += value * weights[key] - weights[key]
    weight -= offset

    return weight


def find_hightest_weighted_word(words, weights):
    highest_weighted_word = ""
    highest_weight = 0
    for word in words:
        word_weight = calculate_word_weight(word, weights)
        if word_weight > highest_weight:
            highest_weighted_word = word
            highest_weight = word_weight
    return highest_weighted_word


def get_next_guess(
    current_word,
    letters_in_word,
    letters_not_in_word,
    letters_not_first,
    letters_not_second,
    letters_not_third,
    letters_not_fourth,
    letters_not_fifth,
):
    words = load_words()
    weights = calculate_weights(words)

    possible_words = []
    for word in words:
        possible_word = set(letters_in_word).issubset(word)
        for pos, c in enumerate(current_word):
            if c != "*" and c != word[pos]:
                possible_word = False
        for c in letters_not_in_word:
            if c in word:
                possible_word = False
        if (
            word[0] in letters_not_first
            or word[1] in letters_not_second
            or word[2] in letters_not_third
            or word[3] in letters_not_fourth
            or word[4] in letters_not_fifth
        ):
            possible_word = False
        if possible_word:
            possible_words.append(word)

    return find_hightest_weighted_word(possible_words, weights)


if __name__ == "__main__":
    import argparse

    my_parser = argparse.ArgumentParser(description="Suggest the next wordle guess")

    my_parser.add_argument(
        "current_word",
        metavar="Current Word",
        type=str,
        help="(* for unknown letter)",
    )

    my_parser.add_argument(
        "--letters_in_word",
        metavar="Letters in word",
        type=str,
        help="All of the known letters in the word",
        default="",
    )

    my_parser.add_argument(
        "--letters_not_in_word",
        metavar="Letters not in word",
        type=str,
        help="All of the letters that are not in the word",
        default="",
    )

    my_parser.add_argument(
        "--letters_not_first",
        metavar="Letters not first",
        type=str,
        help="All of the letters that are not in the first position",
        default="",
    )

    my_parser.add_argument(
        "--letters_not_second",
        metavar="Letters not second",
        type=str,
        help="All of the letters that are not in the second position",
        default="",
    )

    my_parser.add_argument(
        "--letters_not_third",
        metavar="Letters not third",
        type=str,
        help="All of the letters that are not in the third position",
        default="",
    )

    my_parser.add_argument(
        "--letters_not_fourth",
        metavar="Letters not fourth",
        type=str,
        help="All of the letters that are not in the fourth position",
        default="",
    )

    my_parser.add_argument(
        "--letters_not_fifth",
        metavar="Letters not fifth",
        type=str,
        help="All of the letters that are not in the fifth position",
        default="",
    )

    args = my_parser.parse_args()

    if len(args.current_word) != 5:
        exit(1)

    print(
        get_next_guess(
            args.current_word,
            [c for c in args.letters_in_word],
            args.letters_not_in_word,
            args.letters_not_first,
            args.letters_not_second,
            args.letters_not_third,
            args.letters_not_fourth,
            args.letters_not_fifth,
        )
    )
