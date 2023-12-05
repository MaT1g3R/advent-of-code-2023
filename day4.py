from dataclasses import dataclass
from typing import Tuple, Set
from uuid import uuid4

sample = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

sample2 = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


@dataclass
class Input:
    winning_numbers: Set[int]
    nums: list[int]

    def num_wins(self):
        x = 0
        for n in self.nums:
            if n in self.winning_numbers:
                x += 1
        return x

    def score(self):
        w = self.num_wins()
        if not w:
            return 0
        return 2 ** (w - 1)


def parse_intput(txt: str) -> list[Input]:
    out = []
    for line in txt.strip().splitlines(keepends=False):
        _, _, rest = line.partition(":")
        winning, _, n = rest.partition("|")
        winning_numbers = {int(s.strip()) for s in winning.strip().split()}
        nums = [int(s.strip()) for s in n.strip().split()]
        out.append(Input(winning_numbers=winning_numbers, nums=nums))

    return out


def part1(input: list[Input]) -> int:
    sum_ = 0
    for card in input:
        sum_ += card.score()

    return sum_


def part2(input: list[Input]) -> int:
    s = 0

    def do(card: Input, rest: list[Input]):
        num_wins = card.num_wins()
        sum_ = num_wins
        for i in range(num_wins):
            sum_ += do(rest[i], rest[i + 1 :])
        return sum_

    for i, card in enumerate(input):
        s += do(card, input[i + 1 :])
    return s + len(input)


day = int(__file__.split("/")[-1].removeprefix("day")[0])
expected_a1 = 13
expected_a2 = 30

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
