from __future__ import annotations

import argparse
import collections
import math
import os.path
import pytest
from typing import Sequence
from support import timing
import statistics

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    positions = sorted([int(line) for line in s.strip().split(',')])

    optimal_position = round(statistics.mean(positions))  # this should get us close

    def calculate_fuel(position: int) -> int:
        """
        get fuel cost, assuming a particular aligned position
        """
        fuel_cost = 0
        distances = [abs(pos - position) for pos in positions]
        for d in distances:
            fuel = d * (d + 1) // 2
            fuel_cost += fuel
        return fuel_cost

    optimal_fuel = calculate_fuel(optimal_position)

    if calculate_fuel(optimal_position + 1) < optimal_fuel:
        direction = 1
    elif calculate_fuel(optimal_position - 1) < optimal_fuel:
        direction = -1
    else:  # lucky guess!
        return optimal_fuel

    while True:
        optimal_position += direction
        fuel = calculate_fuel(optimal_position)
        if fuel < optimal_fuel:
            optimal_fuel = fuel
            continue
        else:
            return optimal_fuel


INPUT_S = '''\
16,1,2,0,4,2,7,1,2,14
'''

EXPECTED = 168


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
