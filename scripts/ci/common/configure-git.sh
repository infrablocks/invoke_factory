#!/usr/bin/env bash

[ -n "$DEBUG" ] && set -x
set -e
set -o pipefail

git crypt unlock

git config --global user.email "ci@infrablocks.io"
git config --global user.name "CI"
