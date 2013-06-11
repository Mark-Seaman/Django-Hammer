#!/bin/bash
# Test the hammer-wiki command

hammer-wiki < /dev/null

hammer-wiki <<EOF
* Test Page *
This is a test
Check out this output
**Bold text** and so much more
More plain text
 * Bullet **list** item 1
 * Bullet list item 2
 * *Italic bullet*
[[Home]]
[[book/Home]]
[[books][My books]]
http://thisandthat.com
EOF
