#!/bin/bash

if ! [ -e commands_to_run.txt ] ; then
    echo 'A file named [;34mcommands_to_run.txt[m is expected to be found in working directory'
    printf '\nCreate this file and run script again\n'
    exit 1
fi

for command in $(grep -E '[^[:space:]]' commands_to_run.txt) ; do
    if echo "$command" | grep -Eq 'python$'; then
		echo 'One of the commands incorrectly calls python, not python 3.'
	exit 1
    fi
done

# check files exist, and no extra files exist
for test in $(cat list_of_tests.txt); do
    if ! [ -e "$test.txt" ]; then
        echo "Should have copy of file $test.txt , important for testing"
        exit 1
    fi
done

max_running_time=300 # 30 seconds

ifs=$IFS
IFS='
'
if [ -e Test_files ] ; then
    if [ -n "$(ls Test_files)" ] ; then
        cp Test_files/* .
    fi
fi
outputs=student_outputs.txt
rm -f $outputs
test_nb=0
for command in $(grep -E '[^[:space:]]' commands_to_run.txt) ; do
    raw_command=$(echo "$command" | sed 's/\\/\\\\/g')
    if $(echo "$command" | grep -qs "|") ; then
	the_command=$(echo "$command" | sed -r 's/.*\|[[:space:]]*//')
	command=$(echo "$command" | sed -r 's/[[:space:]]*\|.*//')
	command=$(echo "$command" | sed -r "s/^[[:space:]]*echo [[:space:]]*(-e [[:space:]]*)?'[[:space:]]*(.*)'$/{ sleep 0.1; echo \2 | tee -a tmp_outputs.txt; } | $the_command/")
	command=$(echo "$command" | sed -r "s/^[[:space:]]*echo [[:space:]]*(.*)$/{ sleep 0.2; echo \1 | tee -a tmp_outputs.txt; } | $the_command/")
        command=$(echo "$command" | sed -r 's/\\n/ | tee -a tmp_outputs.txt ; sleep 0.2; echo /'g)
    fi
    echo "TEST $((test_nb=++test_nb)) BEGIN" >>$outputs
    raw_command=$(echo $raw_command | sed 's/%/%%/g' | sed 's/\\\\(/(/g' | sed 's/\\\\)/)/g')
    printf "\$ $raw_command\n" >>$outputs
    (IFS=$ifs eval $command >>tmp_outputs.txt 2>&1)&
    process=$(ps -c | egrep Python | sed 's/ t.*//')
    i=0
    while [ $((i=++i)) -lt $max_running_time ] && [ $(stat -c "%s" tmp_outputs.txt) -lt 20000 ] ; do
        sleep 0.1
 
        if ! jobs % &>/dev/null; then
	    	break
        fi
    done
    process=$(ps -c | egrep Python | sed 's/ tty.*//')
    if [ -n "$process" ] ; then
        kill $process
        if [ $i -ge $max_running_time ] ; then
    	    echo "Max running time exceeded, program killed" >>$outputs
	else
	    echo "Too much output" >>$outputs
	fi
    else
	cat tmp_outputs.txt >>$outputs
    fi
    rm tmp_outputs.txt
    printf "TEST $test_nb END\n\n" >>$outputs
done
IFS=$ifs
