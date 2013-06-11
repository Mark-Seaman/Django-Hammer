#!/bin/bash
# Check the platform files

x=~/Projects/jack-hammer
cd $pb

for f in `ls`
do
    echo ____________________
    echo $f
    diff $pb/$f $x/bin/$f
done



cd $pt

for f in `ls *.tst`
do
    echo ____________________
    echo $f
    diff $pt/$f $x/test/$f
done


