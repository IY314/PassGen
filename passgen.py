"""Generate a passphrase based on specified options."""


import argparse
from dataclasses import dataclass
import json
import os
import secrets
import pyperclip


@dataclass
class _ArgClass:
    adjectives: int
    nouns: int
    builtins: bool
    number: bool
    output: str


def generate(adjectives=2, nouns=1, builtins=False,
             number=False, output='clipboard'):
    """Generates a passphrase based on the options"""
    return _generate(_ArgClass(adjectives, nouns, builtins, number, output))


def _main():
    args = _generate_args()
    passphrase = _generate(args)
    if args.output is None or args.output == 'clipboard':
        pyperclip.copy(passphrase)
    elif args.output == 'print':
        print(passphrase)
    else:
        print(f'Unknown output option {args.output}')


def _generate(args):
    words = _get_data(args)
    indices = _generate_indices(args, words)
    passphrase = _get_passphrase(args, words, indices)
    return passphrase


def _generate_args():
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


def _get_data(args):
    paths = ['./words/builtin']
    words = {'adjectives': [], 'nouns': []}
    if not args.builtins:
        with open('./words/extension/passgen_modules.json', encoding='utf-8') as file:
            paths.extend((f'./words/extension/{path}' for path in json.load(file)))
    for dirpath in paths:
        for path in os.listdir(dirpath):
            with open(f'{dirpath}/{path}', encoding='utf-8') as file:
                words.update(json.load(file))

    return words


def _generate_indices(args, words):
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


def _get_passphrase(args, words, indices):
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
    _main()
