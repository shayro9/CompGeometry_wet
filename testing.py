from helpers import *
import random

MAX_TESTS = 100
MAX_LINES = 300


def count_brute_force(segments):
    counter = 0
    for seg1 in segments:
        for seg2 in segments:
            if seg1 != seg2:
                if intersects(seg1, seg2):
                    counter += 1
    return counter // 2


def generate_file():
    tests = MAX_TESTS
    with open("test.txt", "w") as f:
        f.write(f"{tests}\n")
        for t in range(0, tests):
            n = random.randint(1, MAX_LINES)
            x1, x2, y1, y2 = [], [], [], []
            a, b, c, d = 0, 0, 0, 0
            for i in range(0, n):
                while a == c or a in x1 or b in y1 or c in x2 or d in y2:
                    a = round(random.random() * 1000 * (1 if random.randint(0, 1) else -1), 1)
                    b = round(random.random() * 1000 * (1 if random.randint(0, 1) else -1), 1)
                    c = round(random.random() * 1000 * (1 if random.randint(0, 1) else -1), 1)
                    d = round(random.random() * 1000 * (1 if random.randint(0, 1) else -1), 1)
                x1.append(a)
                y1.append(b)
                x2.append(c)
                y2.append(d)

            f.write(f"{n}\n")
            for a, b, c, d in zip(x1, y1, x2, y2):
                f.write(f"{a} {b} {c} {d}\n")
        f.write("-1\n")

