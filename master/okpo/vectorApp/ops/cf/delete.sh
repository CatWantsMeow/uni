#!/usr/bin/env sh

if [[ $1 == '-h' || $1 == '--help' || $1 == "" ]]; then
    echo "usage: $0 stack-name"
    exit 1
fi

echo "Waiting for $1-app stack to be deleted.."
aws cloudformation delete-stack --stack-name "$1-app"
aws cloudformation wait stack-delete-complete --stack-name "$1-app"
echo "Successfully deleted stack - $1-app\n"

echo "Waiting for $1-alb stack to be deleted.."
aws cloudformation delete-stack --stack-name "$1-alb"
aws cloudformation wait stack-delete-complete --stack-name "$1-alb"
echo "Successfully deleted stack - $1-alb\n"

echo "Waiting for $1-vpc stack to be deleted.."
aws cloudformation delete-stack --stack-name "$1-vpc"
aws cloudformation wait stack-delete-complete --stack-name "$1-vpc"
echo "Successfully deleted stack - $1-vpc\n"
