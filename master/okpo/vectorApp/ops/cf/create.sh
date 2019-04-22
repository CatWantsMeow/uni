#!/usr/bin/env sh

if [[ $1 == '-h' || $1 == '--help' || $1 == "" ]]; then
    echo "usage: $0 stack-name"
    exit 1
fi

aws cloudformation deploy --stack-name "$1-vpc" \
                          --template-file "0.vpc.yml" \
                          --parameter-overrides "StackName=$1"

aws cloudformation deploy --stack-name "$1-alb" \
                          --template-file "1.alb.yml" \
                          --parameter-overrides "StackName=$1"

aws cloudformation deploy --stack-name "$1-app" \
                          --template-file "2.app.yml" \
                          --parameter-overrides "StackName=$1" \
                          --capabilities "CAPABILITY_IAM"
