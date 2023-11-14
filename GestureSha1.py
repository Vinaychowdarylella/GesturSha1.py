#!/usr/bin/env python

import binascii
import hashlib
import itertools
import os
import sys

def brute_force_gesture_key_file(gestureSHA1):
    """
    Brute forces possible permutations of gesture.key file until one of them matches the supplied SHA1 hash sum.
    """
    for i in range(3, 10):  # pattern length between 3-9 digits
        print('checking patterns with length %d...' % i)
        perms = itertools.permutations([0, 1, 2, 3, 4, 5, 6, 7, 8], i)
        for combo in perms:
            pattern = ''.join(str(v) for v in combo)
            key = binascii.unhexlify(''.join('%02x' % int(c) for c in pattern))
            sha1 = hashlib.sha1(key).hexdigest()
            if sha1 == gestureSHA1:  # eureka! we found it!
                return pattern
    return None  # fail

def main():
    if len(sys.argv) < 2:
        print('usage: bruteforcegesture.py gesture.key [more gesture.key files]')
        sys.exit(1)

    fn = sys.argv[1]
    if not os.path.isfile(fn):
        print('Invalid file path')
        sys.exit(1)

    with open(fn, 'rb') as f:
        gestureSHA1 = binascii.hexlify(f.read(hashlib.sha1().digest_size)).decode('utf-8')

    if len(gestureSHA1) != hashlib.sha1().digest_size * 2:
        print('invalid gesture.key file')
        sys.exit(1)

    cracked_pattern = brute_force_gesture_key_file(gestureSHA1)

    if cracked_pattern:
        print('pattern found:', cracked_pattern)
    else:
        print('pattern not found')

if __name__ == '__main__':
    main()
