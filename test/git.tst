#!/bin/bash
# Test the checked out files

cd $p
echo $p | sed 's/seaman\/Projects\///'
git status
