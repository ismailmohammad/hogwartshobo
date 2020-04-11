import timeit

trials = 5

for i in range (0,2):
    # Open benchmark file
    benchmark_file = open('tests/benchmarked.txt', 'a')

    time = timeit.timeit('os.system("python hobo.py b '+ str(i) +'")', setup="import os", number=trials) 
    # Append 'hello' at the end of file
    benchmark_file.write("Number of other hobos: " + str(i) + " Trials: " + str(trials) + "Longest surviving Hobo: " + str(time) + "\n")
    # Close the file
    benchmark_file.close()
