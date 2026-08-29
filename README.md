# Game of Life

**gen 0**

The working code from the [@ByteAnimates](https://www.facebook.com/ByteAnimates) reel.

```bash
python3 main.py
```

No dependencies. Python 3.9+.

### As shown in the reel

The panel holds twelve lines, so `Counter` and `around` were named on screen but not written.
`solution.py` writes them, under those same names.

```python
def step(on):
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
```

### Files

| | |
| --- | --- |
| `main.py` | run this — the demo, with real inputs and the claims asserted |
| `solution.py` | the working implementation, with the helpers the reel named |

---

The snippet above is generated from the video itself — what you read is byte-for-byte
what was typed on screen. A fix to it belongs in the episode, so open an issue and the
next reel carries it. Everything else here is hand-written and welcome as a pull request.
