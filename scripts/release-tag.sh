#!/usr/bin/env bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# if [[ `git status --porcelain` ]]; then
#   echo -e "${RED}Changes to pyproject.toml must be pushed first.${NC}"
# else
  v=$(python -c "
import sys
try:
    import tomllib
except ImportError:
    import tomli as tomllib
with open('pyproject.toml', 'rb') as f:
    data = tomllib.load(f)
print(data['project']['version'])
") || exit
  git tag -a "v${v}" -m "${1:-Release}" && git push origin --tags && echo -e "${GREEN}Released version v${v} ${NC}" && exit
  echo -e "${RED}Failed${NC}"
# fi