#!/usr/bin/env bash
set -e

docker build -f ./app/Dockerfile -t my-repo/library/ml-assignment:latest .
