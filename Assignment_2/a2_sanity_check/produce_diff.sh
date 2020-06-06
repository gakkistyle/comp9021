#!/bin/bash

bash run_submissions.sh
bash test_submissions.sh
cat student_results.txt
rm student_outputs.txt
rm student_results.txt
#exit 0
