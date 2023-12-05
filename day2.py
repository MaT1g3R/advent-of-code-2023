from dataclasses import dataclass

sample = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

sample2 = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

blue = "blue"
red = "red"
green = "green"

maxes = {
    red: 12,
    green: 13,
    blue: 14,
}


@dataclass
class Cube:
    num: int
    color: str

    def possible(self):
        m = maxes[self.color]
        return self.num <= m


@dataclass
class Game:
    id: int
    sets: list[list[Cube]]

    def possible(self):
        for set in self.sets:
            for s in set:
                if not s.possible():
                    return False
        return True

    def find_min_power(self):
        mins = {
            red: -1,
            blue: -1,
            green: -1,
        }
        for set in self.sets:
            for cube in set:
                if cube.num > mins[cube.color]:
                    mins[cube.color] = cube.num
        return mins[red] * mins[blue] * mins[green]


def parse_intput(txt: str) -> list[Game]:
    games = []
    for line in txt.strip().splitlines(keepends=False):
        gam, _, rest = line.partition(":")
        game_id = int(gam.split(" ")[-1])

        rest = [s.strip() for s in rest.strip().split(";")]
        sets = []
        for s in rest:
            set = []
            cubes = [a.strip() for a in s.split(",")]
            for cube in cubes:
                num, _, color = cube.partition(" ")
                set.append(Cube(num=int(num), color=color))
            sets.append(set)
        games.append(Game(id=game_id, sets=sets))

    return games


def part1(input: list[Game]) -> int:
    sum_ = 0
    for game in input:
        if game.possible():
            sum_ += game.id

    return sum_


def part2(input: list[Game]) -> int:
    sum_ = 0
    for game in input:
        sum_ += game.find_min_power()
    return sum_


input = ""
with open("./inputs/2023-2.txt") as f:
    input = parse_intput(f.read())

a1_s = part1(parse_intput(sample))
print(f"{a1_s=}")
assert a1_s == 8

a1 = part1(input)
print(f"{a1=}")

a2_s = part2(parse_intput(sample2))
print(f"{a2_s=}")
assert a2_s == 2286

a2 = part2(input)
print(f"{a2=}")
