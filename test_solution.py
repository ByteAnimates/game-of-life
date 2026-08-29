"""
Run it: python3 test_solution.py   (or: pytest)
"""

from solution import COLS, PERIOD, ROWS, SEED, around, period, run, step


def test_the_board_returns_to_its_start_after_thirty_generations():
    # The claim the whole loop depends on: generation 30 is generation 0, cell for cell.
    assert run(SEED, PERIOD)[PERIOD] == SEED


def test_thirty_is_the_first_time_it_happens():
    # A shorter period would mean the reel repeats itself inside a single loop.
    assert period(SEED) == PERIOD


def test_nothing_ever_reaches_the_border():
    # The edges are dead, not wrapped. Anything touching them would be eaten and the
    # period would not hold.
    for gen in run(SEED, PERIOD):
        for r, c in gen:
            assert 0 < r < ROWS - 1 and 0 < c < COLS - 1, (r, c)


def test_the_rules_on_the_textbook_cases():
    assert step(set()) == set()
    assert step({(5, 5)}) == set()                      # loneliness
    assert step({(5, 5), (5, 6)}) == set()              # two is not enough on its own
    block = {(5, 5), (5, 6), (6, 5), (6, 6)}
    assert step(block) == block                         # still life


def test_a_blinker_blinks():
    blinker = {(5, 5), (5, 6), (5, 7)}
    assert step(blinker) == {(4, 6), (5, 6), (6, 6)}
    assert step(step(blinker)) == blinker
    assert period(blinker) == 2


def test_three_neighbours_is_a_birth_and_four_is_death():
    l = {(5, 5), (5, 6), (6, 5)}
    assert step(l) == l | {(6, 6)}                      # the L completes into a block
    crowded = {(6, 6), (5, 5), (5, 6), (5, 7), (6, 5)}
    assert len([n for n in around((6, 6)) if n in crowded]) == 4
    assert (6, 6) not in step(crowded)                  # overcrowding


def test_the_population_oscillates_rather_than_exploding():
    sizes = [len(g) for g in run(SEED, PERIOD)]
    assert max(sizes) < COLS * ROWS / 3
    assert sizes[0] == sizes[PERIOD]


if __name__ == '__main__':
    passed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith('test_'):
            fn()
            print(f'  ok  {name}')
            passed += 1
    print(f'\n{passed} tests passed\n')
