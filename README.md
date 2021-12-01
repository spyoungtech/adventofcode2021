# Advent of Code 2021

## Environment setup

### Install support code

Setup support code:
```
pip install -e ./support
pip install pytest # optional for testing
```

### Setup .env with AOC cookie

Create `.env` in the root with the AOC session cookie value (use inspector or Edit This Cookie extension)

```
session=abc123456790
```

### Install pyclip (optional)

Optionally, install `pyclip` -- when you run your code, the answer will be copied to the clipboard


## Usage

### Starting the day

`aoc2021/day0` contains the code template to start each challenge

When the day is about to begin (a second or 3 beforehand) run the `download-input` command to download the input:

```bash
YEAR=2021
DAY=1
cp aoc2021/day0 "aoc2021/day${DAY}"
pushd "aoc2021/day${DAY}"
download-input "$YEAR" "$DAY"
popd
```

The script will download the input for the day and place it in the newly created directory. It will also display a small sample
of the input text.

(when you move on to part 2, just copy part1.py to part2.py)


### Testing

Each day will have a sample input text in the question and the expected solution, given the sample input.

In the `part1.py` file, enter the sample input as the `INPUT_S` constant, and the expected answer as the `EXPECTED` constant.

To test, run `pytest` on the solution file to test against the sample and expected.

```bash
pytest "aoc2021/day${DAY}/part1.py"
```

### Running solutions

When your test passes, run the file normally and (if you installed pyclip) the answer will be copied to your clipboard.

```
python "aoc2021/day${DAY}/part1.py"
```

A handy way to do both testing and (if tests pass) copying the answer is to do something like:

```bash
pytest "aoc2021/day${DAY}/part1.py" && python "aoc2021/day${DAY}/part1.py"
```
