# Uses python3
import sys
import numpy as np
from time import time


def optimal_weight(capacity, items_list):
    items_num = len (items_list)
    dp_table = [[0]*(capacity + 1) for _ in range(items_num + 1)]

    for i in range(1, items_num + 1):
        for j in range(1, capacity + 1):
            prev_table_weight = dp_table[i - 1][j]
            prev_item_weight = items_list[i - 1]

            if prev_item_weight > j:
                dp_table[i][j] = prev_table_weight
            else:
                dp_table[i][j] = max(
                    dp_table[i - 1][j - prev_item_weight] + prev_item_weight,
                    prev_table_weight
                )
    return dp_table[-1][-1]


def optimal_weight_numpy(capacity, items_list):
    items_num = len(items_list)
    dp_table = np.zeros((items_num + 1, capacity + 1), dtype=np.int16)

    for i in range(1, items_num + 1):
        for j in range(1, capacity + 1):
            prev_table_weight = dp_table[i - 1][j]
            prev_item_weight = items_list[i - 1]

            if prev_item_weight > j:
                dp_table[i][j] = prev_table_weight
            else:
                dp_table[i][j] = max(
                    dp_table[i - 1][j - prev_item_weight] + prev_item_weight,
                    prev_table_weight
                )
    return dp_table[-1][-1]


#test
W = 100
w = list(range(100000))
start_time = time()
res_list = optimal_weight(W, w)
print(f"list -  time sec: {time() - start_time}")

start_time = time()
res_numpy = optimal_weight_numpy(W, w)
print(f"numpy - time sec {time() - start_time}")

if res_numpy != res_list:
    print("A ya tomat")


