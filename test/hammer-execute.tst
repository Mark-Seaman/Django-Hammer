#!/bin/bash
# Test the hammer-execute command script

hammer-execute seaman1/jobs/resume/Index | grep -v 'Results from'
hammer-execute xxx.tst

