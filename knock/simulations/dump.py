from __future__ import annotations

"""This place is a dump. Dead code and stuff. DO NOT RUN."""

import random
from enum import IntEnum
from typing import cast

from attrs import Factory, define
from depict import *

# TODO: Fix.


class State(IntEnum):
    Alive = 1
    Dead = 0

    def swap(self) -> State:
        return State.Alive if self is State.Dead else State.Dead


@define
class Cell(Rect2D):
    position: Point = Point[int](320, 180)
    size: Size = Size(5, 5)
    color: Color = color.Black
    gen: int = 0
    state: State = State.Dead
    prev: State = State.Dead

    def tick(self, delta: float, engine: Engine) -> None:
        pass
        col = self.position.x // self.size.width
        row = (self.position.y - (self.gen * self.size.height)) // self.size.height
        self.position.y += self.size.height
        self.gen += 1
        if col == 0 or col == (engine.width // self.size.width) - 1:
            return
        left: Cell = cast(Grid, self.parent).at(row, col - 1)
        middle: Cell = self
        right: Cell = cast(Grid, self.parent).at(row, col + 1)
        if self.gen == 1:
            print(
                f"{col + 1} :: Left: {left.prev}, Middle: {middle.state}, Right {right.state}"
            )
        self.state = self.ruleset(int(left.prev), int(middle.state), int(right.state))
        self.prev = self.state

    def ruleset(self, a: int, b: int, c: int) -> State:
        ruleset = [0, 1, 0, 1, 1, 0, 1, 0]
        if a == 1 and b == 1 and c == 1:
            return State(ruleset[0])
        elif a == 1 and b == 1 and c == 0:
            return State(ruleset[1])
        elif a == 1 and b == 0 and c == 1:
            return State(ruleset[2])
        elif a == 1 and b == 0 and c == 0:
            return State(ruleset[3])
        elif a == 0 and b == 1 and c == 1:
            return State(ruleset[4])
        elif a == 0 and b == 1 and c == 0:
            return State(ruleset[5])
        elif a == 0 and b == 0 and c == 1:
            return State(ruleset[6])
        elif a == 0 and b == 0 and c == 0:
            return State(ruleset[7])
        return State.Dead

    def draw(self, canvas: Canvas) -> None:
        # Update the cell's color depending on it's state.
        self.color = color.Black if self.state is State.Dead else color.White
        return super().draw(canvas)


@define
class Grid(Scene):
    size: Size = Size(5, 5)

    rows: int = 1
    cols: int = 128

    def fit(self, size: Size) -> Grid:
        """Create a grid that fits the given `size`."""
        return Grid(
            rows=size.height // self.size.height, cols=size.width // self.size.width
        )

    def ready(self, engine: Engine) -> None:
        # Update children in ready() as we require access to the width and height
        # of the window.
        for row in range(self.rows):
            for col in range(self.cols):
                self.children.append(
                    Cell(
                        position=Point[int](
                            col * self.size.width, row * self.size.height
                        ),
                        size=self.size,
                        parent=self,
                    )
                )
        # By default, the cell in the middle of the first row should be alive.
        self.at(0, self.cols // 2).state = State.Alive

    def at(self, row: int, col: int) -> Cell:
        """Return the cell situated at the given row and column."""
        return cast(Cell, self.children[col * self.rows + row])


Engine(Size(640, 360), background=color.Black, clear=False).run(Grid())
from __future__ import annotations

import random
from typing import cast

from attrs import Factory, define
from depict import *

TEST_STRING: str = "to be or not to be"


@define
class Gene:
    phrase: list[str] = Factory(list)
    score: float = 0.0
    mutation_rate: float = 0.01

    def crossover(self, mate: Gene) -> Gene:
        child: Gene = Gene()
        mid: int = random.randrange(0, len(self.phrase))
        for idx, char in enumerate(self.phrase):
            if idx > mid:
                child.phrase[idx] = self.phrase[idx] if idx > mid else mate.phrase[idx]
        return child

    def mutate(self) -> None:
        for idx, char in enumerate(self.phrase):
            if random.random() < self.mutation_rate:
                self.phrase[idx] = chr(random.randrange(32, 128))

    def fitness(self) -> None:
        score: float = 0.0
        for idx, char in enumerate(TEST_STRING):
            if self.phrase[idx] == char:
                score += 1
        self.score = score / len(TEST_STRING)

    def __attrs_post_init__(self) -> None:
        if not self.phrase:
            self.phrase = [
                chr(random.randrange(32, 128)) for _ in range(len(TEST_STRING))
            ]


@define
class InfiniteMonkeyTheorum(Label):
    position: Point = Point[int](320, 180)
    text: str = "This is the best score"

    population: list[Gene] = Factory(list)
    size: int = 100

    def ready(self, engine: Engine) -> None:
        for _ in range(self.size):
            self.population.append(Gene())

    def tick(self, delta: float, engine: Engine) -> None:
        mating_pool: list[Gene] = []
        for idx, gene in enumerate(self.population):
            gene.fitness()
            n: int = int(gene.score * 100)
            for _ in range(n):
                mating_pool.append(gene)

            a: Gene = random.choice(self.population)
            b: Gene = random.choice(self.population)
            child: Gene = a.crossover(b)
            child.mutate()
            self.population[idx] = child

    def draw(self, canvas: Canvas) -> None:
        best: Gene = Gene()
        for gene in self.population:
            if gene.score > best.score:
                best = gene
        self.text = "".join(best.phrase)
        print("".join(best.phrase))


@define
class Dna:
    genes: list[Point] = Factory(list)
    next_gene: int = 0
    max_force: float = 0.1

    def __iter__(self) -> Point:
        self.next_gene += 1
        return self.genes[self.next_gene - 1]

    def __attrs_post_init__(self) -> None:
        if not self.genes:
            for _ in range(100):
                p = Point(0, 1).rotate(random.randint(0, 360), Point(0, 0))
                self.genes.append(p * random.random() * self.max_force)


@define
class Rocket(Polygon2D):
    # Center point of the triangle.
    position: Point = Point(320, 180)
    color: Color = Color.random()
    target: Point = Point(0, 0)
    genes: Dna = Factory(Dna)

    # The angle that the triangle is initially at.
    rotation: float = deg2rad(270.0)
    last_position: Vec3D = Vec3D.origin()

    def fitness(self) -> int:
        return 1 / (self.position - self.target).size() ** 2

    def ready(self, engine: Engine) -> None:
        # The point about which to rotate the triangle.
        self.offset: Point = self.position
        # The vertices of a triangle.
        self.lines: list[Point] = [
            self.position + Point(0, -6 * 2),
            self.position + Point(-6, 6 * 2),
            self.position + Point(6, 6 * 2),
        ]
        self.last_position = self.position

    def build(self) -> list[Scene]:
        return [Mover("Rocket", position=self.position, draw_=False)]

    def moved(self, last_position: Point, position: Point) -> Point:
        """Called whenever the Rocket moves."""
        # If the position hasn't changed by much, do not update `lines`.
        # Reset each line to origin then add the new position.
        self.lines = [((line - last_position + position)) for line in self.lines]

        # Save the new position and set the offset to be at that position.
        self.position = position
        self.offset = position

        return position

    def tick(self, delta: float, engine: Engine) -> None:
        mover: Mover = cast(Mover, self.get_node("Rocket"))

        self.last_position: Point = self.moved(self.last_position, mover.position)
        # Rotate the boid to point towards the direction it's moving.
        # velocity.angle_2d() is used instead of look_at(target)
        # so that boid doesn't instantly turn towards target.
        self.set_rotation(rad2deg(mover.velocity.angle_2d()))
        mover.add_force(next(self.genes))  # type: ignore


Engine(Size(640, 360), background=color.Black, record=False).run(Rocket())
