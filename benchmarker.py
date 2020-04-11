import timeit

trials = 3

for i in range (4,7):
    # Open benchmark file
    benchmark_file = open('tests/benchmarked.txt', 'a')

    time = timeit.timeit('game(True, '+ str(i) +')', setup="from hobo import game" ,number=trials) 
    # Append 'hello' at the end of file
    benchmark_file.write("Number of other hobos: " + str(i) + "Trials: " + str(trials) + " Average Time of Longest surviving Hobo: " + str(time) + "\n")
    # Close the file
    benchmark_file.close()
