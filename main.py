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



if __name__ == '__main__':
    main()
