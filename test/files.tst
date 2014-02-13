#!/bin/bash
# File list test

rmas $p # Remove autosave files
ls $p $p/* | grep -v 'pyc$\|diff$\|out$\|like$'
