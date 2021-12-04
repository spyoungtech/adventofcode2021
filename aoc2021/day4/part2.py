from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Board:
    def __init__(self, matrix):
        self.rows = []
        self.called = []
        for row_index, row in enumerate(matrix):
            r = []
            for col_index, val in enumerate(row):
                r.append(val)
            self.rows.append(r)
        self.columns = [[] for _ in range(len(self.rows))]
        for index, col in enumerate(self.columns):
            for row in self.rows:
                for i, tile in enumerate(row):
                    if i == index:
                        col.append(tile)

    def __hash__(self):
        return hash(''.join(self.elements()))

    def __getitem__(self, item):
        return self.rows[item]

    def __repr__(self):
        return repr(self.rows)

    def get_col(self, index):
        return self.columns[index]

    def get_row(self, index):
        return self.rows[index]

    def call(self, num: str):
        self.called.append(num)
        return self.check_win()

    def check_rows(self):
        for row in self.rows:
            for e in row:
                if e not in self.called:
                    break
            else:
                return True
        return False

    def check_cols(self):
        for col in self.columns:
            for e in col:
                if e not in self.called:
                    break
            else:
                return True
        return False

    def check_win(self):
        return self.check_rows() or self.check_cols()

    def sum(self):
        c = 0
        for row in self.rows:
            for elem in row:
                if elem not in self.called:
                    c += int(elem)
        return c

    def elements(self):
        elems = []
        for row in self.rows:
            for elem in row:
                elems.append(elem)
        return elems


def compute(s: str) -> int:
    lines = s.splitlines()
    called, *lines = lines
    lines.pop(0)
    boards = '\n'.join(lines).split('\n\n')
    called = called.split(',')
    print(called)
    board_list = []
    for board in boards:
        elems = []
        rows = [row.split() for row in board.splitlines()]
        b = Board(rows)
        board_list.append(b)

    done = []
    winners = []
    for c in called:
        print('calling', c)
        done.append(c)
        to_remove = []
        for b in board_list:
            winner = b.call(c)
            if winner:
                winners.append((b, c))
                to_remove.append(b)
        for r in to_remove:
            board_list.remove(r)

    l, c = winners[-1]
    return l.sum() * int(c)


INPUT_S = '''\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
'''

EXPECTED = 1924


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
