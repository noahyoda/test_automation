import sys, subprocess

# new comparison courtecy of jakepink08
def are_different(t_out, e_out):
    t_out = t_out.split('\n')
    e_out = e_out.split('\n')

    # make sure the two outputs have the same number of lines
    if len(t_out) != len(e_out):
        print(f"\nFAIL\nThe number of lines did not match")
        print(f"The number of line in output was {len(t_out)} the number expected was {len(e_out)}\n")
        return True
    
    #loop over each line in the two outputs
    lineNum = 0
    while lineNum < len(t_out):
        testWords = t_out[lineNum].split(" ")
        expectedWords = e_out[lineNum].split(" ")
        
        ##Test for the ps command. These outputs will be different and can be ignored. 
        # However the running states of any mysplit processes in the output of the /bin/ps command should be identical.
        #The /bin/ps command always end in /bin/ps a so look for this to exit skipping loop
        lineString = "".join(t_out[lineNum])
        times_hit = 0
        if lineString == "tsh> /bin/ps a":
            while times_hit < 2:
                ##ensure mysplit processes have the same state
                if testWords[-2] == "./mysplit":
                    if lineString[17:20] != "".join(e_out[lineNum][17:20]):
                        print("\nFAIL\n The process states of mysplit did not match the expected output\n")
                        return True
                if t_out[lineNum][-1] == "a" and t_out[lineNum].split(" ")[-2] == "/bin/ps":
                    times_hit+=1
                lineNum+=1
                
            
        if (len(testWords) != len(expectedWords)):
            print(f"\nFAIL\nThe number of words in line {lineNum + 1} did not match")
            print(f"The number of words in line {lineNum + 1} of output was {len(testWords)} the expected number was {len(expectedWords)}")
            print("Make sure to check for extra whitespaces\n")
            return True

        #loop over every word in each line
        for word in range(len(testWords)):
            if testWords[word] != expectedWords[word]:
                # only pid numbers should be different and these number start with ( and end with ) so ignore these words
                if testWords[word].startswith("(") and testWords[word].endswith(")") and expectedWords[word].startswith("(") and expectedWords[word].endswith(")"):
                    pass
                else:
                    print(f"\nFAIL\nThe word number {word + 1} did not match in line number {lineNum +1}")
                    print(f"The word outputed was \"{testWords[word]}\" the word expected was \"{expectedWords[word]}\"\n")
                    return True
        lineNum+=1


    return False

# runs make clean and rebuilds project
def clean():
    subprocess.run(["make", "clean"], stdout=subprocess.PIPE)
    subprocess.run(["make"], stdout=subprocess.PIPE)

if __name__ == "__main__":
    # clean and rebuild project
    clean()
    # setup test variables
    tests = []

    ''' parses args -
        -n followed by a number to run tests 1 to n, 
        just numbers to run specific tests, 
        no args to run all tests
    '''
    if len(sys.argv) > 1:
        if sys.argv[1] == '-n':
            tests = [int(i) for i in range(1, len(sys.argv[2]))]
        else:
            tests = [int(i) for i in sys.argv[1:]]
    else:
        tests = [i for i in range(1, 18)]
    
    # run tests
    for i in tests:
        t_name = "test"
        t_name += str(i) if i > 9 else "0" + str(i)

        t_result = subprocess.run(["make", t_name], stdout=subprocess.PIPE)
        e_result = subprocess.run(["make", 'r' + t_name], stdout=subprocess.PIPE)

        t_out = '\n'.join(t_result.stdout.decode('utf-8').split('\n')[1:])
        e_out = '\n'.join(e_result.stdout.decode('utf-8').split('\n')[1:])

        # check if test failed
        if are_different(t_out, e_out):
            print("test {0} failed: {1}".format(str(i), t_name))

            print("expected:\n{0}".format(e_out))
            print("got:\n{0}".format(t_out))
            exit(0)
        else:
            print("{0} passed".format(t_name))
