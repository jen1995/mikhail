# Uses python3
import sys
import numpy as np
from time import perf_counter_ns

def optimal_weight(capacity, items_list):
    # write your code here
    items_num = len (items_list)
    dp_table = [[0]*(capacity+1) for _ in range (items_num+1)]

    for i in range (1, items_num+1):
        for j in range (1, capacity+1):
            prev_table_weight = dp_table[i-1][j]
            prev_item_weight = items_list[i-1]
            #print ("i, j, prevtable, previtem, dp   ", i, j, prev_table_weight, prev_item_weight)
            #print (dp_table)
            dp_table[i][j] = prev_table_weight if prev_item_weight > j else max(  dp_table[i-1][j - prev_item_weight] + prev_item_weight,   prev_table_weight  )
    return dp_table[-1][-1]

def optimal_weight_numpy (capacity, items_list):
    # write your code here
    items_num = len (items_list)
    dp_table = np.zeros((items_num+1, capacity+1), dtype = np.int16)

    for i in range (1, items_num+1):
        for j in range (1, capacity+1):
            prev_table_weight = dp_table[i-1][j]
            prev_item_weight = items_list[i-1]
            #print ("i, j, prevtable, previtem, dp   ", i, j, prev_table_weight, prev_item_weight)
            #print (dp_table)
            dp_table[i][j] = prev_table_weight if prev_item_weight > j else max(  dp_table[i-1][j - prev_item_weight] + prev_item_weight,   prev_table_weight  )
    return dp_table[-1][-1]


#test
W = 100
w = list (range (100000))
start_time = perf_counter_ns()
n = optimal_weight(W,w)
time_used = (perf_counter_ns() - start_time)/10e6
print ("list -  time ms ", time_used)
start_time = perf_counter_ns()
n = optimal_weight_numpy(W,w)
time_used = (perf_counter_ns() - start_time)/10e6
print ("numpy - time ms ", time_used)


