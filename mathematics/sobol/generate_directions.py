#!/usr/bin/env python

with open('directions.dat') as f:
    f.readline()
    f.readline()
    data = [[int(el) for el in l.split()[2:]] for l in f]

with open('directions.py', 'w') as f:
    f.write('directions = [\n')
    for d in data:
        f.write('    [{}],\n'.format(','.join(map(str, d))))
    f.write(']')
