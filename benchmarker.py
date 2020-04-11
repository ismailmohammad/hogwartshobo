import timeit

trials = 3

for i in range (0,4):
    # Open benchmark file
    benchmark_file = open('tests/results_report.txt', 'a')

    time = timeit.timeit('os.system("python hobo.py b '+ str(i) +'")', setup="import os", number=trials) 
    # Append 'hello' at the end of file
    benchmark_file.write("Number of other hobos: " + str(i) + " Trials: " + str(trials) + " Total Trial Time: " + str(time) + " Average: " + str(time/trials) +"\n")
    # Close the file
    benchmark_file.close()
