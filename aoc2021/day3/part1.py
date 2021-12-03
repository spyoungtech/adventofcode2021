from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    gamma = 0

    counts = [0] * len(lines[0])

    for line in lines:
        for i, c in enumerate(line):
            if c == '0':
                counts[i] += 1
    gamma = []
    epsilon = []
    for bit, c in enumerate(counts):
        if c >= len(lines) // 2:
            g = '0'
            e = '1'
        else:
            g = '1'
            e = '0'
        gamma.append(g)
        epsilon.append(e)
    gamma_str = ''.join(gamma)
    epsilon_str = ''.join(epsilon)
    return int(gamma_str, 2) * int(epsilon_str, 2)

    return 0


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

EXPECTED = 198


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
