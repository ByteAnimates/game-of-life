"""
Run it: python3 main.py

Conway's Game of Life, seeded so the whole board returns to its starting position every
30 generations — which is what lets the reel loop without a cut.
"""

from solution import COLS, PERIOD, ROWS, SEED, around, period, render, run, step


def main() -> None:
    gens = run(SEED, PERIOD)

    print(f'\n  generation 0\n')
    print(render(gens[0]))
    print(f'\n  generation {PERIOD}\n')
    print(render(gens[PERIOD]))

    print(f'\n  gen  population')
    for g in range(0, PERIOD + 1, 5):
        same = '   <- identical to generation 0' if gens[g] == SEED and g else ''
        print(f'  {g:>3}  {len(gens[g]):>10}{same}')

    print(
        f'\n  The board is exactly its starting position again after {PERIOD} generations, and\n'
        f'  that is lcm(15, 2): a pulsar with a period of 15 and blinkers with a period of\n'
        f'  2. Neither number is chosen — they are properties of the patterns — so the\n'
        f'  loop length is a consequence of what was seeded, not a setting.\n'
        f'\n  The edges are dead, not wrapped. On a torus a glider comes back around and\n'
        f'  shreds every oscillator it passes through, and nothing returns to anything.\n'
    )


# ── the claims above, checked ────────────────────────────────────────────────────

# THE CLAIM the loop depends on: generation 30 is generation 0, cell for cell.
_gens = run(SEED, PERIOD)
assert _gens[PERIOD] == SEED

# And 30 is the FIRST time it happens — a shorter period would mean the reel repeats
# itself inside a single loop.
assert period(SEED) == PERIOD

# Nothing ever reaches the border. If it did, the dead edge would eat it and the period
# would not hold.
for _g in _gens:
    for _r, _c in _g:
        assert 0 < _r < ROWS - 1 and 0 < _c < COLS - 1, (_r, _c)

# The rules themselves, on the textbook cases.
assert step(set()) == set()
assert step({(5, 5)}) == set()                                  # loneliness
assert step({(5, 5), (5, 6)}) == set()                          # two is not enough alone
_block = {(5, 5), (5, 6), (6, 5), (6, 6)}
assert step(_block) == _block                                   # still life
_blinker = {(5, 5), (5, 6), (5, 7)}
assert step(_blinker) == {(4, 6), (5, 6), (6, 6)}               # and back again
assert step(step(_blinker)) == _blinker
assert period(_blinker) == 2

# A cell with exactly THREE live neighbours is born — three, and an L of three live
# cells completes itself into a block, which is the shortest demonstration of it.
_l = {(5, 5), (5, 6), (6, 5)}
assert step(_l) == _l | {(6, 6)}
# Overcrowding: a LIVE cell with four live neighbours dies.
_crowded = {(6, 6), (5, 5), (5, 6), (5, 7), (6, 5)}
assert len([n for n in around((6, 6)) if n in _crowded]) == 4
assert (6, 6) not in step(_crowded)

# The population moves rather than growing without bound — oscillators, not an explosion.
_sizes = [len(g) for g in _gens]
assert max(_sizes) < COLS * ROWS / 3
assert _sizes[0] == _sizes[PERIOD]

if __name__ == '__main__':
    main()
