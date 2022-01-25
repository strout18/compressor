#!/bin/bash

for dir in ./tests/test*
do
    echo "Testing ${dir}"
    cd $dir
    > test.txt.comp
    > test.txt.interm
    rm -f test.txt.comp.plaintext
    python3 ../../mainencoderchar.py test.txt 8 2> /dev/null
    python3 ../../maindecoderchar.py test.txt.comp 2> /dev/null
    sleep 10
    DIFF=$(diff test.txt test.txt.comp.plaintext)
    if [ "$DIFF" != "" ]
    then
	echo "Test failed on orig to plaintext"
    fi
    cd ../..

done
