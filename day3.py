from dataclasses import dataclass
from typing import Tuple
from uuid import uuid4

sample = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

sample2 = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


@dataclass
class Number:
    value: int
    coords: list[Tuple[int, int]]


def parse_intput(txt: str):
    c_matrix = []
    for line in txt.strip().splitlines():
        c_matrix.append(list(line))

    nums = []
    for i, line in enumerate(c_matrix):
        current_digits = ""
        current_coords = []
        for j, c in enumerate(line + ["."]):
            if c.isdigit():
                current_digits += c
                current_coords.append((i, j))
            elif not c.isdigit() and len(current_digits) > 0:
                nums.append(Number(value=int(current_digits), coords=current_coords))
                current_digits = ""
                current_coords = []

    return c_matrix, nums


def is_symbol(c):
    return c != "." and not c.isdigit()


def make_adj(x, y):
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            yield x + i, y + j


def part1(input) -> int:
    matrix, nums = input
    sum_ = 0

    def cord_is_symbol(x, y):
        try:
            return is_symbol(matrix[x][y])
        except IndexError:
            return False

    for num in nums:
        valid = False
        for i, j in num.coords:
            for x, y in make_adj(i, j):
                if cord_is_symbol(x, y):
                    valid = True
                    break
            if valid:
                break
        if valid:
            sum_ += num.value

    return sum_


def part2(input) -> int:
    matrix, nums = input
    position_map = {}
    sum_ = 0

    for num in nums:
        num_id = uuid4()
        for cord in num.coords:
            position_map[cord] = (num_id, num.value)

    for i, line in enumerate(matrix):
        for j, c in enumerate(line):
            if c != "*":
                continue
            adjcent_nums = {}
            for x, y in make_adj(i, j):
                try:
                    num_id, val = position_map[(x, y)]
                except KeyError:
                    continue
                else:
                    adjcent_nums[num_id] = val
            if len(adjcent_nums) == 2:
                product = 1
                for v in adjcent_nums.values():
                    product *= v
                sum_ += product

    return sum_


day = int(__file__.split("/")[-1].removeprefix("day")[0])
expected_a1 = 4361
expected_a2 = 467835

input = ""
with open(f"./inputs/2023-{day}.txt") as f:
    input = parse_intput(f.read())

a1_s = part1(parse_intput(sample))
print(f"{a1_s=}")
assert a1_s == expected_a1

a1 = part1(input)
print(f"{a1=}")

a2_s = part2(parse_intput(sample2))
print(f"{a2_s=}")
assert a2_s == expected_a2

a2 = part2(input)
print(f"{a2=}")
