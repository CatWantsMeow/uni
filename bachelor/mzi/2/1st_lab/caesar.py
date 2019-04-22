#!/usr/bin/python
from argparse import ArgumentParser


LETTERS_FREQUENCIES = {
    'a': 0.081,
    'b': 0.014,
    'c': 0.027,
    'd': 0.039,
    'e': 0.130,
    'f': 0.029,
    'g': 0.020,
    'h': 0.052,
    'i': 0.065,
    'j': 0.002,
    'k': 0.004,
    'l': 0.034,
    'm': 0.025,
    'n': 0.072,
    'o': 0.079,
    'p': 0.020,
    'r': 0.069,
    's': 0.061,
    't': 0.105,
    'q': 0.001,
    'u': 0.024,
    'v': 0.009,
    'w': 0.015,
    'x': 0.002,
    'y': 0.019,
    'z': 0.001,
}


ALPHABET = [chr(i) for i in xrange(ord('a'), ord('z') + 1)]


def encrypt(message, key):
    processed_message = ''
    for i in xrange(len(message)):
        if message[i] in ALPHABET:
            index = ALPHABET.index(message[i])
            processed_message += ALPHABET[(index + key) % len(ALPHABET)]
        else:
            processed_message += message[i]
    return processed_message


def decrypt(message, key):
    processed_message = ''
    for i in xrange(len(message)):
        if message[i] in ALPHABET:
            index = ALPHABET.index(message[i])
            processed_message += ALPHABET[(index - key) % len(ALPHABET)]
        else:
            processed_message += message[i]
    return processed_message


def hack(message):
    result = []
    for key in xrange(len(ALPHABET)):
        msg = decrypt(message, key)
        f = {l: float(msg.count(l)) / len(msg) for l in ALPHABET}
        x = 0
        for l in ALPHABET:
            x += (f[l] - LETTERS_FREQUENCIES[l]) ** 2 / LETTERS_FREQUENCIES[l]
        x *= len(message)
        result.append((msg, x))
    return min(result, key=lambda elem: elem[1])[0]


def main():
    parser = ArgumentParser()
    parser.add_argument('--encrypt', action='store_true')
    parser.add_argument('--decrypt', action='store_true')
    parser.add_argument('--hack', action='store_true')

    args = parser.parse_args()
    if args.encrypt:
        message = raw_input('Enter a message: ')
        key = int(raw_input('Enter a key: '))
        print 'Result: {}'.format(encrypt(message, key))

    elif args.decrypt:
        message = raw_input('Enter a message: ')
        key = int(raw_input('Enter a key: '))
        print 'Result: {}'.format(decrypt(message, key))

    elif args.hack:
        message = raw_input('Enter a message: ')
        print "Result: {}".format(hack(message))


if __name__ == '__main__':
    main()
