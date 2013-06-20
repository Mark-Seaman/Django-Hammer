#!/bin/bash
# Test the hammer-show command

function execute
{
    echo
    echo  hammer-show $*
    hammer-show $* | grep -v 'Results from'
}

execute 
execute Index
execute __App__
execute seaman
execute seaman/Index

