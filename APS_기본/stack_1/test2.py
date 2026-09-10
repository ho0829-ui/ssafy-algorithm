import math
arr = [(0,0),(None,None),(0,4),(None,None)]
x = arr[1][0] - arr[0][0]
y = arr[1][1] - arr[0][1]
# print(math.atan(y/x))    # 라디안
# print(math.degrees(math.atan(y/x)))
print(math.degrees(math.atan2(x, y)))


