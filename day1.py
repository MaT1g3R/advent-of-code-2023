sample = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

sample2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""


def parse_intput(txt: str) -> list[str]:
    return txt.strip().splitlines(keepends=False)


def part1(input: list[str]) -> int:
    sum_ = 0
    for line in input:
        digits = [c for c in line if c.isdigit()]
        sum_ += int("".join([digits[0], digits[-1]]))
    return sum_


def part2(input: list[str]) -> int:
    digit_strs = [
        s.strip()
        for s in "one, two, three, four, five, six, seven, eight, nine".split(",")
    ]
    for i in range(1, 10):
        digit_strs.append(str(i))

    def string_to_num(s):
        try:
            return int(s)
        except ValueError:
            return {
                "one": 1,
                "two": 2,
                "three": 3,
                "four": 4,
                "five": 5,
                "six": 6,
                "seven": 7,
                "eight": 8,
                "nine": 9,
            }[s]

    def find_digit(line: str):
        first_i, first = 999999999999999999, -1
        last_i, last = -1, -1

        for d in digit_strs:
            i = line.find(d)
            j = line.rfind(d)
            val = string_to_num(d)
            if i != -1 and i < first_i:
                first_i = i
                first = val
            if j != -1 and j > last_i:
                last_i = j
                last = val

        return first, last

    sum_ = 0
    for line in input:
        first, last = find_digit(line)
        n = 10 * first + last
        sum_ += n

    return sum_


a1_sample = part1(parse_intput(sample))
print(f"{a1_sample=}")
assert a1_sample == 142

input = ""
with open("./inputs/2023-1.txt") as f:
    input = parse_intput(f.read())

a1 = part1(input)
print(f"{a1=}")

a2_s = part2(parse_intput(sample2))
print(f"{a2_s=}")
assert a2_s == 281

a2 = part2(input)
print(f"{a2=}")
