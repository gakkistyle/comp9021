#!/bin/bash

if ! [ -e patterns_of_outputs.txt ] ; then
    echo 'A file named [;34mpatterns_of_outputs.txt[m is expected to be found in working directory'
    printf '\nCreate this file and run script again\n'
    exit 1
fi
if ! [ -e student_outputs.txt ] ; then
    echo 'Student outputs have not been generated'
    exit 1
fi
    
student_results=student_results.txt
rm -f "$student_results"
printf '{\n' >>$student_results
printf '    "testcases": [\n' >>$student_results
test_nb=0
while egrep -qs "TEST $((test_nb=++test_nb)) BEGIN" patterns_of_outputs.txt ; do
    command_and_student_output=\
$(LANG=C sed -n '/'"TEST $test_nb BEGIN"'/,/'"TEST $test_nb END"'/ {
    /TEST/!p
}' student_outputs.txt | LC_CTYPE=C tr '\n' '')
    command=$(echo "$command_and_student_output" | sed 's/..//' | sed 's/\\/\\\\\\\\/g' | LANG=C sed 's/.*//' | sed 's/"/\\\\"/g' | sed 's/%/%%/g')
    student_output=$(echo "$command_and_student_output" | LANG=C sed 's/[^]*//')		          
    output_pattern=\
$(LANG=C sed -n '/'"TEST $test_nb BEGIN"'/,/'"TEST $test_nb END"'/ {
    /^TEST/!p
}' patterns_of_outputs.txt | tr '\n' '' | sed 's/.*//')

    expected_output=\
$(LANG=C sed -n '/'"TEST $test_nb BEGIN"'/,/'"TEST $test_nb END"'/ {
    /TEST/!p
}' commands_and_expected_outputs.txt | LC_CTYPE=C tr '\n' '' | LANG=C sed 's/[^]*//')
    if [ $test_nb -gt 1 ] ; then
	printf ',\n' >>$student_results
    fi
    printf '        {\n' >>$student_results
    printf '            "name": ' >>$student_results
    printf "\"Test $test_nb run as: $command\"" >>$student_results
    printf ',\n' >>$student_results
    printf '            "ok": true,\n' >>$student_results
    if $(echo "$student_output" | egrep -qs "$output_pattern") ; then
	printf '            "passed": true,\n' >>$student_results
    else
	printf '            "passed": false,\n' >>$student_results
    fi
    printf '            "observed": ' >>$student_results
    student_output=$(echo "$student_output" | LC_CTYPE=C sed 's/\\/\\\\\\\\/g' | sed s'//\\\\\\\\n/g' | sed 's/%/%%/g' | sed 's/"/\\\\"/g' | sed 's/	/\\\\t/g')
    printf "\"$student_output\"" >>$student_results
    printf ',\n' >>$student_results
    printf '            "expected": ' >>$student_results
    expected_output=$(echo "$expected_output" | LC_CTYPE=C sed 's/\\/\\\\\\\\/g' | sed s'//\\\\\\\\n/g' | sed 's/%/%%/g' | sed 's/"/\\\\"/g' | sed 's/	/\\\\t/g')
    printf "\"$expected_output\"" >>$student_results
    printf '\n        }' >>$student_results
    continue
done
printf '\n    ]\n' >>$student_results
printf '}\n' >>$student_results

