from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

LANTERNFISH = []

BROODING_POOL = []


class Lanternfish:
    def __init__(self, timer=8):
        self.timer = timer

    def advance_day(self):
        self.timer -= 1
        if self.timer < 0:
            self.timer = 6
            BROODING_POOL.append(Lanternfish())


def advance_day():
    for f in LANTERNFISH:
        f.advance_day()
    while BROODING_POOL:
        f = BROODING_POOL.pop()
        LANTERNFISH.append(f)


def compute(s: str) -> int:
    starting_timers = [int(a) for a in s.split(',') if a]
    for t in starting_timers:
        LANTERNFISH.append(Lanternfish(t))
    for _ in range(80):
        advance_day()
    return len(LANTERNFISH)


INPUT_S = '''\
3,4,3,1,2
'''

EXPECTED = 5934


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
