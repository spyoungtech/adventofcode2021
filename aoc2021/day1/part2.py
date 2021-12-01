from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def group_gen():
    yield '1'
    yield '1 2'
    i = 1
    while True:
        yield f'{i} {i+1} {i+2}'
        i += 1


def compute(s: str) -> int:
    from collections import defaultdict

    window_increases = 0
    windows = defaultdict(list)
    groupos = group_gen()
    for line in s.splitlines():
        n = int(line)
        groups = next(groupos).split()
        for group in groups:
            windows[group].append(n)

    previous = None
    for group in windows:
        n = sum(windows[group])
        if previous is not None:
            diff = n - previous
            if diff > 0:
                window_increases += 1
        previous = n
    return window_increases


INPUT_S = '''\
199
200
208
210
200
207
240
269
260
263
'''

EXPECTED = 5


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
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
