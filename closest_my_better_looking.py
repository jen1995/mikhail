#Uses python3
import sys
import math
from time import perf_counter_ns
import random

def distance (p1, p2): return math.sqrt (math.pow(p2[0]-p1[0],2) + math.pow(p2[1]-p1[1],2))

def y7neighbors (y, y_sorted, y_sorted_len, i, min_distance):
    base = i - 7 if i >= 7 else 0
    top = min (y_sorted_len, i+8)
    for j in range (i, base-1, -1):
        if y-y_sorted[j][1] >= min_distance:
            base = j+1
            break
    for j in range (i, top):
        if y_sorted[j][1]-y >= min_distance:
            top = j
            break
    yield from y_sorted [base:top]

def min_distance (x_sorted):
    """
    recieve the list of non sorted tuples (x,y)
    return the minimal distance
    """
    min_distance = 1e12
    points_num = len (x_sorted)   # the nuber of points
    x_sorted = list (set (x_sorted))   # remove dubplicate points    # don't use set before sort!!!! it destroies sorting
    if len (x_sorted) != points_num: return 0   # duplicate points = zero distance
    x_sorted.sort(key = lambda xcoord : (xcoord[0]))    #  sort by x

    #main job - with every 3 points in the list
    for (p1, p2, p3)  in zip((x_sorted [0::3]), (x_sorted [1::3]), (x_sorted[2::3])):
        min_distance = min(min_distance, min ( map (distance, [p1, p1, p2], [p2, p3, p3]) ))
        if min_distance == 0: return min_distance

    #glue borders
    # starts from the right point on the border - 3 points on the left, two points to the right - 6 overall
    border_point_i = 3
    while border_point_i <= points_num-3:   # it mast work fast so we assume here that we have 3 points to the left and 2 points to the right. All that remains - do Remainder part
        #form the list of closest points to border
        rightborder_x = x_sorted[border_point_i][0] + min_distance
        righti = border_point_i+3           #  we look futher for full min_distance only to the left   - right step is only 3 points
        i = border_point_i+1
        while i < righti and x_sorted[i][0] < rightborder_x: i += 1  # we can do this because i is checked before [i]
        righti = i

        leftborder_x = x_sorted[border_point_i][0] - min_distance
        lefti = 0 #border_point_i-3         #  the full scan to the left - we go to the first element if min_distance is big
        i = border_point_i - 1
        while i >= lefti and x_sorted[i][0] > leftborder_x: i -= 1  # we can do this because i is checked before [i]
        lefti = i+1

        if lefti < righti-1:    # points found
            y_sorted = sorted(x_sorted[lefti:righti:], key = lambda xcoord : (xcoord[1]))
            y_sorted_len = len (y_sorted)
            temp_min_distance = min_distance
            for i,p in enumerate (y_sorted):
                temp_min_distance = min (temp_min_distance, min( [distance (p, p2) for p2 in y7neighbors(p[1], y_sorted, y_sorted_len, i, min_distance) if p2 != p], default=min_distance)  )
            min_distance = min (min_distance, temp_min_distance)     # remove additional min from the loop above
        border_point_i += 3

    #remainder - only for remainig part  < 7
    border_point_i = points_num - points_num % 3          # it can be 1 or 2 for remainder to work
    if border_point_i < points_num:   # one or none point to the right
        rightborder_x = x_sorted[border_point_i][0] + min_distance
        righti = points_num
        i = border_point_i          # borderpoint - is inclusive index for point  not like hi index of list
        while i < righti and x_sorted[i][0] < rightborder_x: i += 1  # we can do this because i is checked before [i]
        righti = i  # it can be points_num for all points included  or points_num-1 if last point is too far

        lefti = 0  #border_point_i-3    # the only border here is min_distance and the first point in x_sorted
        leftborder_x = x_sorted[border_point_i][0] - min_distance
        i = border_point_i - 1
        while i >= lefti and x_sorted[i][0] > leftborder_x:   # we can do this because i is checked before [i]
            i -= 1
        lefti = i+1

        if lefti == righti-1: return min_distance    # no points found
        y_sorted = sorted(x_sorted[lefti:righti:], key = lambda xcoord : (xcoord[1]))
        y_sorted_len = len (y_sorted)
        for i,p in enumerate (y_sorted):        # filter zero  for points self distance
            min_distance = min(min_distance, min( filter(lambda x: x != 0,  [distance (p, p2) for p2 in y7neighbors(p[1], y_sorted, y_sorted_len, i, min_distance)]), default=min_distance)  )

    return min_distance

if __name__ == '__main__':
    while True:
        xy = list (zip (random.sample(range(-1000000000, 1000000000), random.randint(2,100000)),random.sample(range(-1000000000, 1000000000), random.randint(2,100000))))
        start_time = perf_counter_ns()
        my = min_distance (xy)
        print ("time ms  ", (perf_counter_ns() - start_time)/10e6, "   for points number   ", len(xy))
        print (my)
