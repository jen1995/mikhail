#Uses python3
import sys
import math
from time import time
import random


def naivemindist(xy):
    """ Naive for stress tests
    """
    xylen = len(xy)
    min_distance = float("inf")
    for i in range(xylen):
        for j in range(xylen):
            if i != j:
                cur_distance = (xy[j][0] - xy[i][0]) ** 2 + (xy[j][1] - xy[i][1]) ** 2
                if cur_distance < min_distance: 
                    min_distance = cur_distance
                if min_distance == 0: 
                    return min_distance

    return math.sqrt(min_distance)


def distance(p1, p2): 
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def y7neighbors(y_sorted, idx, min_distance):
    y = y_sorted[idx][1]
    base = idx - 7 if idx >= 7 else 0
    top = min(len(y_sorted), idx + 8)

    for j in range(idx, base - 1, -1):
        if y - y_sorted[j][1] >= min_distance:
            base = j + 1
            break

    for j in range(idx, top):
        if y_sorted[j][1] - y >= min_distance:
            top = j
            break

    return y_sorted[base: top]


def update_min_distance(points, min_distance):
    y_sorted = sorted(points, key=lambda point: point[1])
    temp_min_distance = min_distance

    for idx, p in enumerate(y_sorted):
        temp_min_distance = min(
            temp_min_distance, 
            min(
                [distance(p, neighbor) for neighbor in y7neighbors(y_sorted, idx, min_distance) if neighbor != p], 
                default=min_distance
            )
        )
    return temp_min_distance


def min_distance(points):
    """
    recieve the list of non sorted tuples (x,y)
    return the minimal distance
    """
    min_distance = float("inf")
    points_num = len(points)
    if len(set(points)) != points_num: 
        return 0   # duplicate points = zero distance

    x_sorted = sorted(points, key=lambda xcoord: xcoord[0])   #  sort by x

    # main job - with every 3 points in the list
    for (p1, p2, p3) in zip(x_sorted[0::3], x_sorted[1::3], x_sorted[2::3]):
        """
        what is happening here?
        """
        min_distance = min(min_distance, min(map(distance, [p1, p1, p2], [p2, p3, p3])))
        if min_distance == 0: 
            return min_distance

    # glue borders
    # starts from the right point on the border - 3 points on the left, two points to the right - 6 overall
    # it must work fast so we assume here that we have 3 points to the left and 2 points to the right. All that remains - do Remainder part
    for border_point in range(3, points_num - 2):

        # form the list of closest points to border
        right_edge = x_sorted[border_point][0] + min_distance
        right = border_point + 1
        while right < border_point + 3 and x_sorted[right][0] < right_edge: 
            right += 1

        left_edge = x_sorted[border_point][0] - min_distance
        left = border_point - 1
        while left >= 0 and x_sorted[left][0] > left_edge:
            left -= 1
        left += 1

        if left < right - 1:    # points found
            min_distance = min(min_distance, update_min_distance(x_sorted[left: right], min_distance))

    # remainder - only for remainig part < 7
    border_point = points_num - points_num % 3
    if border_point < points_num:   # one or none point to the right
        right_edge = x_sorted[border_point][0] + min_distance
        right = border_point   # borderpoint - is inclusive index for point not like hi index of list

        while right < points_num and x_sorted[right][0] < right_edge: 
            right += 1   # it can be points_num for all points included  or points_num-1 if last point is too far

        left_edge = x_sorted[border_point][0] - min_distance
        left = border_point - 1   # the only border here is min_distance and the first point in x_sorted
        while left >= 0 and x_sorted[left][0] > left_edge:
            left -= 1
        left += 1

        if left < right - 1:
            min_distance = min(min_distance, update_min_distance(x_sorted[left: right], min_distance))

    return min_distance


if __name__ == '__main__':
    n_tests = 500
    random_range = 100
    n_points = 50
    for _ in range(n_tests):
        x = random.sample(range(-random_range, random_range), n_points)
        y = random.sample(range(-random_range, random_range), n_points)
        xy = list(zip(x, y))
        # print(xy)

        naive = naivemindist(xy)
        start_time = time()
        my = min_distance(xy)
        print(f"time in seconds: {time() - start_time} for points number {len(xy)}, my solution = {my}")

        if abs(naive - my) > 1e-10:
            raise("Stress test failed")
