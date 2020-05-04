from typing import List
from time import time
import numpy as np

class Solution:
    def numSubmatrixSumTarget(self, matrix: List[List[int]], target: int) -> int:
        # converts memory into speed by two arrays and additional columns for cumsums
        # and by nditer loop (width + height) instead of (width * height)
        # not so good looking but faster than 99% of Python submissions
        # still best in memory usage

        m_width = len(matrix[0])
        m_height = len(matrix)
        a_width = m_width * (m_width+1) // 2      # additional rows for all horizontal cumsums
        a = np.empty(m_height * a_width, dtype=np.int32).reshape(m_height, a_width)
        b = np.copy(a)        
        b[:, :m_width] = matrix
        match_count = 0
        
        base = a_width        
        for row in range(m_width-1, -1, -1):
            step = m_width - row
            base -= step            
            np.cumsum(b[:, row:row+step], axis=1, out=a[:, base:base+step])            

        np.cumsum(a, axis=0, out=b)
        match_count = np.count_nonzero(a == target)
        col = 1
        for c in np.nditer(a, flags=['external_loop', 'buffered'], buffersize=a_width): 
            match_count += np.count_nonzero(b[col:] == target)
            if col == m_height - 1:  break
            np.subtract(b,c, out=b, casting="unsafe")            
            col += 1

        return match_count
    
matrix = [[0,1,0], [1,1,1], [0,1,0]]    # 4
target = 0
start_time = time()
print(Solution.numSubmatrixSumTarget(None, matrix, target))
print(f"my time sec: {time() - start_time}")



