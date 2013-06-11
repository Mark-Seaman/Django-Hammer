#!/bin/bash
# Test writing WMD docs

echo 'Write blank file'
hammer-write 'MyTestFile' < /dev/null
cat $p/doc/MyTestFile


echo 'Write test text'
hammer-write 'MyTestFile' <<EOF 
This is a test.
Is it working?
EOF
cat $p/doc/MyTestFile

rm $p/doc/MyTestFile


python <<EOF
from subprocess         import Popen,PIPE
def do_command(cmd, input=''):
    p = Popen(cmd.split(), stdin=PIPE, stdout=PIPE)
    p.stdin.write(input)
    p.stdin.close()
    return  p.stdout.read()
print 'do_command start'
do_command('hammer-write %s'%'MyTestFile2','''This is a test.
Is it working?
''')
print 'do_command end'
EOF

cat $p/doc/MyTestFile2
echo

rm $p/doc/MyTestFile2
