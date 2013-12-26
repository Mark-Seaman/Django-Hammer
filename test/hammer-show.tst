#!/bin/bash
# Test the hammer-show command

mkdir -p $pd/test

cat <<EOF > $pd/test/Index
* Test User Home *
This is a test page for the test user.

**Tab 1**
 This is some text

**Tab 2**

This is some more text
 
EOF


hammer-read 'test/Index'

hammer-show test/Index
