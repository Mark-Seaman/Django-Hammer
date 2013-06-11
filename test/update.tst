#!/bin/bash
# Check the platform files

cd $pb

for f in `ls`
do
    echo ____________________
    echo $f
    diff $pb/$f ~/Projects/jack-hammer/bin/$f
done



