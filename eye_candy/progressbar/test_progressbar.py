from progress.bar import Bar

it = []

bar = Bar("test")
for elem in bar.iter(it):
    pass
