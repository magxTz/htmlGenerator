import time


def memorize(f):
    mem = {}

    def inner(num):
        if num not in mem:
            mem[num] = f(num)
        return mem[num]

    return inner


@memorize
def factor(num):
    try:
        if num == 1:
            return 1
        else:
            result = num*factor(num - 1)
            return result

    except RecursionError as e:
        print(str(e))


if __name__ == "__main__":
    start = time.time()
    print(factor(200))
    end = time.time()
    print(f'it took {end - start} s to execute')
