#!/usr/bin/python
from argparse import ArgumentParser


INITIAL_LFSR = 0x3b5f07e2


def lfsr(r, shift_sequence=(0, 1, 2, 3, 5, 8, 13, 21)):
    bit = r >> shift_sequence[0]
    for shift in shift_sequence[1:]:
        bit ^= (r >> shift)
    return (r >> 1) | ((bit & 0x00000001) << 31)


def main():
    parser = ArgumentParser()
    parser.add_argument('fin', action='store')
    parser.add_argument('fout', action='store')

    r = INITIAL_LFSR
    args = parser.parse_args()
    with open(args.fin, 'r') as fin, open(args.fout, 'w+') as fout:
        message = fin.read()
        for char in message:
            r = lfsr(r)
            fout.write(chr((ord(char) ^ r) & 0xff))

if __name__ == '__main__':
    main()