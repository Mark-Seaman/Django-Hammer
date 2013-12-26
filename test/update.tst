#!/bin/bash
# Check the platform files

x=~/Projects/jack-hammer
cd $x

# bin  test  app  app/views

for f in `ls bin/* test/*.tst app/doc/*.py app/Hammer/*.py`
do
    echo ____________________
    echo $f
    diff $p/$f $x/$f
done

x=~/Projects/thumper/webapps/simpleapps/app
cd $x

for f in `ls doc/*.py Hammer/*.py`
do
    echo ____________________
    echo $f
    diff $pa/$f $x/$f
done
