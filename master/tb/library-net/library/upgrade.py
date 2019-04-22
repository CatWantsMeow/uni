#!/usr/bin/env python3
import json
import os

def main():
    with open('package.json', 'r') as f:
        d = json.load(f)

    version = [int(e) for e in d['version'].split('.')]
    version[2] += 1
    version = '.'.join(str(e) for e in version)
    d['version'] = version

    with open('package.json', 'w') as f:
        json.dump(d, f, indent=4)

    os.system('composer archive create -t dir -n .')
    os.system(f'composer network install -a library@{version}.bna -c PeerAdmin@hlfv1')
    os.system(f'composer network upgrade -c PeerAdmin@hlfv1 -n library -V {version}')


if __name__ == "__main__":
    main()