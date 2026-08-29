"""
The working version of what the reel shows.

The reel's `step()` names two things it does not write: `Counter`, which is one import,
and `around`, the eight cells touching a given one. Both are here.

IT COUNTS FROM THE LIVE CELLS OUTWARD, which is the part worth understanding. The obvious
implementation walks every cell of the board and counts its neighbours; this one walks
only the live cells and adds one to each of THEIR neighbours. Any cell that ends up in the
tally is either alive or touching something alive, and every cell not in the tally has
zero live neighbours and cannot possibly be born. So the board never has to be visited at
all — the cost is proportional to the population, not to the grid, and the same code runs
on an infinite plane.

DEAD EDGES, NOT A TORUS. A glider that runs off a bounded board dies at the wall; on a
wrapped one it comes back and shreds every oscillator it passes through. This board is
finite with dead edges, and the patterns are placed clear of each other and of the border
so that nothing ever collides — which is what lets the whole thing return to its starting
position on a fixed beat.
"""

from collections import Counter

COLS = 32
ROWS = 13

#: The seed, written as art rather than as coordinates, because the clearances are the
#: point: the gaps you can see between these shapes are why they never interfere.
SEED_ART = [
    '................................',
    '................................',
    '....................OOO.....OOO.',
    '...........................OOO..',
    '......O....O....................',
    '....OO.OOOO.OO..................',
    '......O....O....................',
    '....................OO..........',
    '....................OO.....OO...',
    '......................OO...OO...',
    '......................OO.....OO.',
    '.............................OO.',
    '................................',
]

SEED = frozenset(
    (r, c) for r, row in enumerate(SEED_ART) for c, ch in enumerate(row) if ch == 'O'
)

#: lcm(15, 2) — the pulsar's fifteen against the blinkers' two. Checked, never assumed.
PERIOD = 30


def around(cell: tuple[int, int]) -> list[tuple[int, int]]:
    """
    The eight cells touching `cell`, clipped to the board.

    Clipping rather than wrapping is what makes the border dead: a cell on row 0 simply
    has fewer neighbours, so a blinker seeded there is not a blinker at all.
    """
    r, c = cell
    return [
        (r + dr, c + dc)
        for dr in (-1, 0, 1)
        for dc in (-1, 0, 1)
        if (dr or dc) and 0 <= r + dr < ROWS and 0 <= c + dc < COLS
    ]


def step(on: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """Line for line what is on screen, with `Counter` imported and `around` written."""
    count = Counter()
    for c in on:
        for n in around(c):
            count[n] += 1

    new = set()
    for c, n in count.items():
        born = n == 3
        stays = n == 2 and c in on
        if born or stays:
            new.add(c)
    return new


def run(on: set[tuple[int, int]], generations: int) -> list[set[tuple[int, int]]]:
    """Every generation from `on`, inclusive of the starting one."""
    out = [set(on)]
    for _ in range(generations):
        out.append(step(out[-1]))
    return out


def period(on: set[tuple[int, int]], limit: int = 200) -> int | None:
    """How many generations until the board is exactly what it started as."""
    live = set(on)
    for g in range(1, limit + 1):
        live = step(live)
        if live == on:
            return g
    return None


def render(on: set[tuple[int, int]]) -> str:
    return '\n'.join(
        ''.join('O' if (r, c) in on else '.' for c in range(COLS)) for r in range(ROWS)
    )
