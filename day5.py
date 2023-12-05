from dataclasses import dataclass
from typing import Tuple, Set, Optional, Iterable
from uuid import uuid4
import itertools

sample = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

sample2 = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


@dataclass
class Range:
    dest_start: int
    source_start: int
    length: int

    def find(self, n) -> Optional[int]:
        actual = n + (self.dest_start - self.source_start)
        if actual >= self.dest_start and actual < self.dest_start + self.length:
            return actual
        return None

    def find_range(self, start, l) -> Tuple[Tuple[int, int], int]:
        diff = self.dest_start - self.source_start
        s = max(self.source_start, start)

        size = 0
        input_end = start + l
        range_end = self.source_start + self.length
        actual_end = min(input_end, range_end)

        if s > range_end:
            size = 0
        elif (start + l) < self.source_start:
            size = 0
        else:
            size = actual_end - s

        return (s, size), diff

@dataclass
class Map:
    ranges: list[Range]

    def find(self, n) -> int:
        for r in self.ranges:
            a = r.find(n)
            if a is not None:
                return a
        return n

    def find_range(self, start, length) -> list[Tuple[int,int]]:
        found = []
        found_map = {}

        results = []
        for r in self.ranges:
            f = r.find_range(start, length)
            (s, l), diff = f
            if l:
                found.append(f)
                found_map[s] = f

        found.sort(key=lambda t: t[0][0])

        i = iter(found)
        cur_start = start
        cur_len = 0
        for (s,l),diff in found:
            if s > cur_start:
                results.append((cur_start, s - cur_start))
            results.append((s + diff, l))
            cur_start = s+l
            cur_len = l

        final_diff = (start + length) - (cur_start + cur_len)
        if final_diff > 0:
            results.append((cur_start+cur_len, final_diff))

        return results

@dataclass
class Input:
    seeds: list[int]
    seed_ranges: list[Tuple[int, int]]
    maps: list[Map]

    def find_location(self, seed) -> int:
        loc = seed
        for m in self.maps:
            loc = m.find(loc)
        return loc
    
    def find_loc_range(self, start, l) -> int:
        ranges = [(start, l)]
        for m in self.maps:
            tmp = []
            for s, l in ranges:
                tmp += m.find_range(s,l)
            ranges = tmp

        return sorted(ranges, key=lambda r: r[0])[0][0]

def parse_intput(txt: str) -> Input:
    lines = txt.strip().splitlines(keepends=False)
    seeds = [int(a.strip()) for a in lines[0].removeprefix('seeds:').strip().split()]
    maps = []

    def gen_seed_ranges():
        i = iter(seeds)
        while True:
            try:
                start, l = next(i), next(i)
            except StopIteration:
                break
            else:
                yield start, l

    cur_ranges = []
    for line in lines[2:] + ['']:
        if 'map:' in line:
            cur_ranges = []
            continue
        if not line.strip() and len(cur_ranges) > 0:
            maps.append(Map(ranges=cur_ranges))
            continue
        d, s, l  = line.strip().split()
        cur_ranges.append(Range(dest_start=int(d), source_start=int(s), length=int(l)))

    return Input(seeds=seeds, seed_ranges=list(gen_seed_ranges()), maps=maps)


def part1(input: Input) -> int:
    locs = []
    for s in input.seeds:
        locs.append(input.find_location(s))
    return min(*locs)


def part2(input: Input) -> int:
    locs = []
    for s, l in input.seed_ranges:
        locs.append(input.find_loc_range(s,l))
    return min(*locs)


day = int(__file__.split("/")[-1].removeprefix("day")[0])
expected_a1 = 35
expected_a2 = 46

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

