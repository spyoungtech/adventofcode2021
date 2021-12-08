from __future__ import annotations

import argparse
import collections
import os.path
import pytest
from typing import Sequence
from support import timing
import statistics

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    positions = [int(line) for line in s.strip().split(',')]
    optimal_point = int(statistics.median(positions))

    distances = [abs(pos - optimal_point) for pos in positions]
    return sum(distances)


INPUT_S = '''\
16,1,2,0,4,2,7,1,2,14
'''

EXPECTED = 37


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
