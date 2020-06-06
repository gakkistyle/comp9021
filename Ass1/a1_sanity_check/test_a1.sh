#!/bin/bash

for i in {0..35} ; do
    if ! [ -e tests/test$i.in ] ; then
        echo "You are missing the file tests/test$i.in. Please add it and start again."
        exit 1
    fi
    if ! [ -e tests/test$i.out ] ; then
        echo "You are missing the file tests/test$i.out. Please add it and start again."
        exit 1
    fi
done

num_tests_failed=0

for i in {0..35} ; do
    temp_file=$(mktemp --tmpdir=.)
    python3 roman_arabic.py < tests/test$i.in > $temp_file
    DIFF=$(diff tests/test$i.out $temp_file)
    if [ "$DIFF" != "" ] ; then
        printf "test $i failed (Required input is in tests/test$i.in and required output is in tests/test$i.out)\n########## Command to reproduce\n"
        printf "python3 roman_arabic.py < tests/test$i.in\n"
        printf "########## Expected output\n"
        cat tests/test$i.out
        printf "########## Your output\n"
        cat $temp_file
        ((num_tests_failed++))
    else
        printf "test $i passed\n"
    fi
    printf "***********************************\n\n"
    rm -f $temp_file
done

if [ $num_tests_failed -ne 0 ] ; then
    echo "You have failed $num_tests_failed tests"
else
    echo "All tests passed! Good job!"
fi
