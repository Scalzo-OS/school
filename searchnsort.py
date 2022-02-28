#Generates a random list
#Sorts using bubble sort
#Searches using binary search

import random
import time

now = time.time()

x = 100
my_list = [random.randint(1, 1000) for i in range(x)]
to_search = my_list[random.randint(0, x-1)]
print('Searching for:', to_search, '\nList: ', my_list)

def Sort(data):
    sorting = True
    while sorting:
        sorting = False
        for key, value in enumerate(data):
            if key >= 1:
                if value < data[key-1]:
                    data[key-1], data[key] = data[key], data[key-1]
                    sorting = True
    return data

def Try(data, test):
    return test == data

def Binary(data, search):
    lower = 0
    upper = len(data) - 1
    
    if Try(data[lower], search): return 'Found at ' + str(lower)
    if Try(data[upper], search): return 'Found at ' + str(upper)
    
    while True:
        middle = round((upper + lower)/2)
        
        if Try(data[middle], search):
            return 'Found at ' + str(middle)
        
        if data[middle] > search: upper = middle
        if data[middle] < search: lower = middle

        if upper == lower: return 'Not Found'

print('Sorted: ', Sort(my_list))

print(Binary(Sort(my_list), to_search))

print('Finished in', round(time.time() - now, 3), 'seconds')