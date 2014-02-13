#!/bin/bash
# Test the checked out files

cd $p
echo $p | filter-path
git status | grep -v 'nothing to commit'
