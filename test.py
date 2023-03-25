import sys, subprocess

# compare output of test and expected output
def are_different(t_out, e_out):
    t_out = t_out.split('\n')
    e_out = e_out.split('\n')

    reg = "\[\d\] \([0-9]+\)"

    if len(t_out) != len(e_out):
        return True
    for i in range(len(t_out)):
        if t_out[i] != e_out[i]:
            # if contains reg ignore and check rest are equal
            if reg in t_out[i] and reg in e_out[i]:
                t_out[i] = t_out[i].replace(reg, "")
                e_out[i] = e_out[i].replace(reg, "")
                if t_out[i] != e_out[i]:
                    return True
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
            print("test {0} passed".format(t_name))