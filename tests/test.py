

from random import randrange


def sim():
    for i in range(9-randrange(-9, 9)):
        for p in range(1, 3+1):
            if randrange(100) < 4:
                return p
            continue
        continue
    return 0


def main():
    results = [0 for _ in range(4)]
    for _ in range(100000):
        results[sim()] += 1
        continue
    print(results[1]*100/sum(results))
    return


if __name__ == '__main__':
    main()
    ...
