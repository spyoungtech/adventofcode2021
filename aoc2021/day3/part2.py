from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()

    # Oxygen rating
    filtered_lines = lines[::]
    for position in range(len(lines[0])):
        bits = [line[position] for line in filtered_lines]
        n_zero = bits.count('0')
        n_one = bits.count('1')
        if n_zero > n_one:
            oxygen = '0'
            co = '1'
        else:
            oxygen = '1'
            co = '0'

        considered = []
        for line in filtered_lines:
            if line[position] == oxygen:
                considered.append(line)
        filtered_lines = considered
        if len(filtered_lines) == 1:
            break
    ox_rating = int(filtered_lines[0], 2)

    # CO rating
    # XXX: can this be made DRY?
    filtered_lines = lines[::]
    for position in range(len(lines[0])):
        bits = [line[position] for line in filtered_lines]
        n_zero = bits.count('0')
        n_one = bits.count('1')
        if n_zero > n_one:
            oxygen = '0'
            co = '1'
        else:
            oxygen = '1'
            co = '0'

        considered = []
        for line in filtered_lines:
            if line[position] == co:
                considered.append(line)
        filtered_lines = considered
        if len(filtered_lines) == 1:
            break
    co_rating = int(filtered_lines[0], 2)

    # power
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
