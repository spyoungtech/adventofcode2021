from __future__ import annotations

import argparse
import os.path

import pytest
from typing import Literal, Sequence
from support import timing
from collections import Counter

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

RATING_SELECTION = Literal['co2', 'o2']


def get_rating(lines: Sequence[str], which_rating: RATING_SELECTION) -> int:
    width = len(lines[0])
    for position in range(width):
        bits = Counter()
        for line in lines:
            bits[line[position]] += 1

        n_zero = bits['0']
        n_one = bits['1']
        if n_zero > n_one:
            oxygen = '0'
            co = '1'
        else:
            oxygen = '1'
            co = '0'

        if which_rating == 'o2':
            rating = oxygen
        elif which_rating == 'co2':
            rating = co
        else:
            raise ValueError("which_rating must be 'o2' or 'co'")

        considered = []
        for line in lines:
            if line[position] == rating:
                considered.append(line)
        lines = considered
        if len(lines) == 1:
            break
    return int(lines[0], 2)


def compute(s: str) -> int:
    lines = s.splitlines()

    ox_rating = get_rating(lines, 'o2')
    co_rating = get_rating(lines, 'co2')

    return co_rating * ox_rating


INPUT_S = '''\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
'''

EXPECTED = 230


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    ((INPUT_S, EXPECTED),),
)
def test_foo(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        answer = compute(f.read())
        print(answer)
        try:
            import pyclip

            pyclip.copy(str(answer))
            print('ANSWER COPIED TO CLIPBOARD!')
        except ImportError:
            print('PyClip not installed. Install pyclip to copy your answer to the clipboard automagically')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
