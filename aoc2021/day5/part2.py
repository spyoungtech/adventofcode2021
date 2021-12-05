from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()

    covered = set()
    overlapped = set()
    overlapping = 0

    for line in lines:
        a, b = line.split(' -> ')
        x1, y1 = a.split(',')
        x2, y2 = b.split(',')
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        if x2 > x1:
            r1 = range(x1, x2 + 1)
        elif x1 > x2:
            r1 = reversed(range(x2, x1 + 1))
        else:
            l = abs(y1 - y2)
            r1 = [x1 for _ in range(l + 1)]

        if y2 > y1:
            r2 = range(y1, y2 + 1)
        elif y1 > y2:
            r2 = reversed(range(y2, y1 + 1))
        else:
            l = abs(x2 - x1)
            r2 = [y1 for _ in range(l + 1)]
        for x, y in zip(r1, r2):
            point = (x, y)
            if point in covered and point not in overlapped:
                overlapped.add(point)
                overlapping += 1
            covered.add(point)
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

EXPECTED = 12


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
