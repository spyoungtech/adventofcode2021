from __future__ import annotations

import argparse
import collections
import os.path
import pytest
from typing import Sequence
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class BroodingPool:
    def __init__(self, fishes: Sequence[int]):
        self.counts = {i: fishes.count(i) for i in range(9)}

    def advance_day(self):
        zero = self.counts[1]
        for i in range(1, 8):
            self.counts[i] = self.counts[i + 1]
        self.counts[6] += self.counts[0]
        self.counts[8] = self.counts[0]
        self.counts[0] = zero

    def sum(self):
        return sum(self.counts.values())


def compute(s: str) -> int:
    starting_timers = [int(a) for a in s.split(',') if a]
    pool = BroodingPool(starting_timers)
    for _ in range(256):
        pool.advance_day()
    return pool.sum()


INPUT_S = '''\
3,4,3,1,2
'''

EXPECTED = 26984457539


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
