#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

count=0
successed=0
failed=0
tests=$(find tests -name "*.test" -type f)

echo "Running tests:"
for file in $tests;
do
    key=$(./tea generate_key)
    ./tea encrypt $key $file ~encrypted
    ./tea decrypt $key ~encrypted ~decrypted

    if cmp -s ~decrypted $file;
    then
        printf "\tTesting %s: ${GREEN}ok${NC}\n" $file
        let 'successed += 1'
    else
        printf "\tTesting %s: ${RED}fail${NC}\n" $file
        let 'failed += 1'
    fi

    rm -f ~decrypted ~encrypted
    let 'count += 1'
done
printf "Completed: %d tests runned. %d successed. %d failed.\n" $count $successed $failed
