from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing
from typing import Literal

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def is_vertical_or_horizonal(x1, y1, x2, y2) -> Literal['vertical', 'horizontal', False]:
    if x1 == x2:
        return 'vertical'
    elif y2 == y1:
        return 'horizontal'
    return False


def compute(s: str) -> int:
    lines = s.splitlines()

    covered = set()
    overlapped = set()
    overlapping = 0

    for line in lines:
        a, b = line.split(' -> ')
        x1, y1 = a.split(',')
        x2, y2 = b.split(',')
        orientation = is_vertical_or_horizonal(x1, y1, x2, y2)
        if not orientation:
            continue
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        if orientation == 'horizontal':
            if x2 > x1:
                for i in range(x1, x2 + 1):
                    point = (i, y1)
                    if point in covered and point not in overlapped:
                        overlapped.add(point)
                        overlapping += 1
                    covered.add(point)
            elif x1 > x2:
                for i in range(x2, x1 + 1):
                    point = (i, y1)
                    if point in covered and point not in overlapped:
                        overlapped.add(point)
                        overlapping += 1
                    covered.add(point)
            else:
                raise ValueError('no movement?')
        else:
            if y2 > y1:
                for i in range(y1, y2 + 1):
                    point = (x1, i)
                    if point in covered and point not in overlapped:
                        overlapped.add(point)
                        overlapping += 1
                    covered.add(point)
            elif y1 > y2:
                for i in range(y2, y1 + 1):
                    point = (x1, i)
                    if point in covered and point not in overlapped:
                        overlapped.add(point)
                        overlapping += 1
                    covered.add(point)
            else:
                raise ValueError('no movement>?')

    return overlapping


INPUT_S = '''\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
'''

EXPECTED = 5


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
