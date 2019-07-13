"""based on https://stackoverflow.com/a/34482761/5172579"""

import sys


def progressbar(it, prefix="progress:", size=35, file=sys.stdout):
    count = max(1, len(it))
    n = len(str(count)) 

    def show(j):
        x = int(size * j / count)
        counter = "{:{}d}/{}".format(j, n, count)
        bar = "{} |{}{}| {}\r".format(prefix, "|" * x, " " * (size - x), counter)
        # bar = "{} {}{} {}\r".format(prefix, "|" * x, "." * (size - x), counter)
        file.write(bar)
        file.flush()

    show(0)

    for i, item in enumerate(it):
        yield item
        show(i + 1)

    file.write("\n")
    file.flush()


if __name__ == "__main__":
    import time

    # for _ in progressbar(range(15), "Computing: ", 30):
    for _ in progressbar(range(15)):  # , "Computing: ", 30):
        time.sleep(0.2)  # any calculation you need

