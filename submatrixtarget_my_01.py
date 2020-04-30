from typing import List
from time import perf_counter_ns
import numpy as np

class Solution:
    def numSubmatrixSumTarget(self, matrix: List[List[int]], target: int) -> int:
    # def numSubmatrixSumTarget(self, matrix, target: int) -> int:
        m_width = len (matrix[0])
        m_height = len (matrix)
        match_count = 0
        a = np.array(matrix, dtype=np.int16)
        for _ in range (m_width):
            b = np.cumsum (a, axis = 1)
            for _ in range (m_height):
                c = np.cumsum (b, axis = 0)
                match_count += np.count_nonzero (c==target) if target else (c.size - np.count_nonzero (c))
                b = b [1:,:]    # remove first column
                #print (c)
            a = a [:,1:]    # remove first row
            #print (b)
        return match_count

#"""  test
matrix = [[0,1,0],[1,1,1],[0,1,0]]    # 4
#matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
#matrix =  [[1,-1],[-1,1]]    # 5
#matrix = [[1, 2, 3, 4, 0, 0, 0, 8], [1, 2, 3, 4, 0, 0, 0, 8], [1, 2, 3, 4, 0, 0, 0, 8]]
#matrix = [[0,0,0,1,1],[1,1,1,0,1],[1,1,1,1,0],[0,0,0,1,0],[0,0,0,1,1]]     # 28
target = 0
#   27539   target 500
#target = 500
start_time = perf_counter_ns()
print (Solution.numSubmatrixSumTarget(None, matrix, target))
print ("my time ms ", (perf_counter_ns() - start_time)/10e6)



