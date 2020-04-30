from typing import List
from time import time

import numpy as np


class Solution:
    def numSubmatrixSumTarget(self, matrix: List[List[int]], target: int) -> int:
        m_width = len(matrix[0])
        m_height = len(matrix)
        match_count = 0
        a = np.array(matrix, dtype=np.int16)

        for row in range(m_width):
            b = np.cumsum(a[:, row:], axis=1)
            for col in range(m_height):
                c = np.cumsum(b[col:], axis=0)
                match_count += np.count_nonzero(c == target)

        return match_count


matrix = [[0,1,0], [1,1,1], [0,1,0]]    # 4
target = 0
start_time = time()
print(Solution.numSubmatrixSumTarget(None, matrix, target))
print(f"my time sec: {time() - start_time}")



