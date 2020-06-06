---------------------------------
 COMP9021 19T3 A2 Sanity Checker
---------------------------------

To use A2 sanity checker, follow the instructions below:

1. log in to your CSE account

2. extract the zip file into an empty directory.  You should have a file named testing_script.sh as well as other files.

3. put your maze.py file into the created directory alongside the files testing_script.sh and produce_diff.sh.

4. run the script: 
	. testing_script.sh (or ./testing_script.sh)
		
	(if the above did not work then run: "chmod +x *.sh" (to make sh files executable) then "./testinq_script.sh" or ". testing_script.sh".

The tests are the same tests as the ones in A2 Specification pdf file in addition to four additional tests.

The script will complain if you accidentally delete any of the files.
If some of the tests fail, then run the script ". produce_diff.sh" to see the difference between the required output and your output.