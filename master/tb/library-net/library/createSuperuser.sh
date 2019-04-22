#!/usr/bin/env bash
export ADMIN_DATA='{
    "$class": "org.library.net.Librarian",
    "id": "1",
    "firstName": "librarian_1",
    "lastName": "librarian_1"
}'

composer participant add -c admin@library  -d "$ADMIN_DATA"
composer identity issue -c admin@library -f cards/superuser-initial.card -u superuser -a "resource:org.library.net.Librarian#1"
composer card import -f cards/superuser-initial.card
composer card export -f cards/superuser.card -c superuser@library
