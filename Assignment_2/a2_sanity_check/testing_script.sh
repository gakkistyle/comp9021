#!/bin/bash

./run_submissions.sh
exit_status=$?
if [[ $exit_status -eq 1 ]]; then
    echo "run_submissions.sh requirements not satisfied"
    exit 1
fi

./test_submissions.sh

python3 -c "import json; f= open('student_results.txt'); data=json.loads(f.read()); f.close(); testdata=data[\"testcases\"]; success=[\"failed\", \"success\"]; [print(\"Test {} {}\".format(i+1, success[int(testdata[i][\"passed\"])])) for i in range(len(testdata))];"
