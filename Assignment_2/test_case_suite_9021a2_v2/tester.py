import sys
import os
from io import StringIO
import time

# assignment 2 9021 T3 tester version 2

def main():
    try:
        import maze
    except ModuleNotFoundError:
        print("Module not found! Please put your maze.py in the same folder as this program.")
        return
    
    try:
        # test files
        with open('filelist.txt','r') as f:
            testfiles = [fn[:-1] for fn in f]
        # expected error/analyze output
        expected = []
        with open('outputs.txt','r') as f:
            ostor = []
            for l in f:
                l = l[:-1]
                if len(ostor) == 0 and l.startswith('maze.MazeError: '):
                    expected.append(("E",l[16:]))
                elif len(l) > 0:
                    ostor.append(l)
                if len(l) == 0 and len(ostor) > 0:
                    expected.append(("O",ostor))
                    ostor = []
            if len(ostor) > 0:
                expected.append(("O",ostor))
    except:
        print("Error opening test file. Ensure that you have cd-ed to this program's directory.")
        return

    if len(testfiles) != len(expected):
        print("Number of test files and expected output definition mismatch. Cannot proceed.")
        return
    
    # do the actual testing!
    passed = 0
    for i in range(len(testfiles)):
        start_time = time.time()
        has_err = False
        proceed = True
        # test file load
        try:
            inst = maze.Maze(testfiles[i])
        except FileNotFoundError:
            print(f"Test file '{testfiles[i]}'' not found! Aborting.")
            return
        except maze.MazeError as e:
            if expected[i][0] != "E":
                has_err = True
                print(f"'{testfiles[i]}': Load error.")
            elif str(e) != expected[i][1]:
                has_err = True
                print(f"'{testfiles[i]}': Wrong exception message.")
            # we can't test the others if the constructor throws an exception
            proceed = False

        if proceed:
            if expected[i][0] == "E":
                proceed = False
                print(f"'{testfiles[i]}': Does not raise an error.")
                has_err = True

        if proceed:
            # test analyze
            # capture the output!
            orgstdout = sys.stdout
            sys.stdout = mystdout = StringIO()
            inst.analyse()
            sys.stdout = orgstdout
            # analyze the content
            ao = mystdout.getvalue().split('\n')
            if len(ao) < len(expected[i][1]):
                has_err = True
                print(f"'{testfiles[i]}': Incomplete analyze output.")
            elif len(ao) > len(expected[i][1]) + 1:
                has_err = True
                print(f"'{testfiles[i]}': Extraneous analyze output.")
            else:
                for j in range(len(expected[i][1])):
                    if ao[j] != expected[i][1][j]:
                        has_err = True
                        print(f"'{testfiles[i]}': Invalid analyze output.")
                        break
            
            # test display
            # first, remove existing .tex file!
            expect_fn = f"{os.path.splitext(testfiles[i])[0]}.tex"
            try:
                os.remove(expect_fn)
            except Exception:
                # we'll rely on "good deed" :)
                pass

            inst.display()

            # compare the resulting file, line by line
            try:
                with open(expect_fn,'r') as f:
                    result = f.readlines()
            except FileNotFoundError:
                has_err = True
                print(f"'{testfiles[i]}': Output .tex file not produced.")
            
            if not has_err:
                # proceed on comparing file contents line by line
                try:
                    with open(f'expected_tex/{expect_fn}','r') as f:
                        expect_result = f.readlines()
                except:
                    print("Error loading reference .tex file. Operation aborted.")
                    return
                
                if len(result) != len(expect_result):
                    has_err = True
                    print(f"'{testfiles[i]}': Output .tex file line count mismatch.")

                for j in range(len(result)):
                    if result[j] != expect_result[j]:
                        has_err = True
                        print(f"'{testfiles[i]}': Invalid output .tex file content(s).")
                        break
        
        if not has_err:
            passed += 1
            print(f"Test case '{testfiles[i]}' OK - in {time.time() - start_time:.2f} sec.")

        print()

    print(f"{passed}/{len(testfiles)} tests passed.")
    if passed == len(testfiles):
        print("Good job!")

if __name__=="__main__":
    main()