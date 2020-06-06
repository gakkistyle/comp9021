-------------------------------------------
 COMP9021 19T3 Assignment 1 Sanity Checker
-------------------------------------------

To use a1 sanity checker, follow the instructions below:

1. log in to your CSE account

2. extract the zip file into an empty directory.  You should have a file named test_a1.sh as well as a subdirectory named tests.

3. put your roman_arabic.py file into the created root directory - alongside the file test_a1.sh

4. run the script: 
	. test_a1.sh
		
	(if the above did not work then run: "chmod +x test_a1.sh" (to make it executable) then "./test_a1.sh")


The tests are the same tests as the ones in Assignment 1 Specification pdf file.

The script will complain if you accidentally delete any of the input or output test files (in the tests subdirectory), and will show the command to reproduce the issue, the required output and your output when the test fails, otherwise tell you the test passed. At the end you are informed how many tests you failed, or get a nice message if you passed them all.
