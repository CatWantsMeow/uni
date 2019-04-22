#!/usr/bin/env bash
export COMPOSER_PROVIDERS='{
  "jwt": {
    "provider": "jwt",
    "module": "/Users/georgiy.yarosh/uni/2/tb/library-net/library/jwt.js",
    "secretOrKey": "gSi4WmttWuvy2ewoTGooigPwSDoxwZOy",
    "authScheme": "saml",
    "successRedirect": "/",
    "failureRedirect":"/"
    }
}'

composer-rest-server -c admin@library -n never -a true -m true -u true -d logging -w true