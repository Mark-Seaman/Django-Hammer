#!/bin/bash
# Check the platform files

x=~/Projects/jack-hammer


cd $x/bin

for f in `ls`
do
    echo ____________________
    echo $f
    diff $pb/$f $x/bin/$f
done


cd $x/test

for f in `ls *.tst`
do
    echo ____________________
    echo $f
    diff $pt/$f $x/test/$f
done


