# 3
# 1 2 3
# 4 5 6
# 7 8 9
# N = int(input())

# arr = [list(map(int,input().split())) for _ in range(N)]
# [x for x in range(5)]  [0,1,2,3,4]
# print(arr)
# arr = []
# for _ in range(N):
#     row = list(map(int, input().split()))
#     arr.append(row)
# print(arr)

# 3
# 123
# 456
# 789
N = int(input())
# input() '123'
arr2 = []
for _ in range(N):
    arr2.append(list(map(int,input())))
print(arr2)