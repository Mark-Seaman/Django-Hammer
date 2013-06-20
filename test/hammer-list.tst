#!/bin/bash
# Test the hammer-list script

function show
{
    echo
    echo  $*
    $* | sort
}

show  hammer-list 
show  hammer-list  seaman
show  hammer-list  seaman/mybook/Automate
