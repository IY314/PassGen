import argparse
import json
import os
import pyperclip
import secrets


def main():
    args = generate_args()
    words = get_data(args)
    indices = generate_indices(args, words)
    passphrase = get_passphrase(args, words, indices)
    if args.output is None or args.output == 'clipboard':
        pyperclip.copy(passphrase)
    elif args.output == 'print':
        print(passphrase)
    else:
        print(f'Unknown output option {args.output}')


def generate_args():
    parser = argparse.ArgumentParser(prog='PassGen')
    parser.add_argument('--adjectives', '-a', type=int, help='The number of '
                        'adjectives (default 2)')
    parser.add_argument('--nouns', '-N', type=int, help='The number of nouns '
                        '(default 1)')
    parser.add_argument('--builtins', '-b', action='store_true', help='Use '
                        'only builtin words')
    parser.add_argument('--number', '-n', action='store_true', help='Add '
                        'number at end')
    parser.add_argument('--output', '-o', help='The form that the passphrase '
                        'is displayed (default clipboard)')
    return parser.parse_args()


def get_data(args):
    paths = ['./words/builtin']
    words = {'adjectives': [], 'nouns': []}
    if not args.builtins:
        paths.append('./words/extension')

    for dirpath in paths:
        for path in os.listdir(dirpath):
            with open(f'{dirpath}/{path}') as f:
                words.update(json.load(f))

    return words


def generate_indices(args, words):
    len_adj = len(words.get('adjectives', []))
    len_noun = len(words.get('nouns', []))
    indices = []

    for _1 in range(args.nouns or 1):
        for _2 in range(args.adjectives or 2):
            adj_idx = secrets.randbelow(len_adj)
            indices.append((adj_idx, 'adjectives'))

        noun_idx = secrets.randbelow(len_noun)
        indices.append((noun_idx, 'nouns'))

    return indices


def get_passphrase(args, words, indices):
    result = ''

    for index, location in indices:
        word_list = words.get(location, None)
        if word_list is None:
            raise Exception(f'Unknown location {location!r}')
        word = word_list[index].capitalize()
        result += word

    if args.number:
        number = secrets.randbits(7)
        result += str(number)

    return result


if __name__ == '__main__':
    main()
