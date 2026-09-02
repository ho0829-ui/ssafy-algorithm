arr = [
    [1,2,3,4,5],
    [5,4,3,2,1],
    [2,4,6,8,10],
    [1,3,5,7,9],
    [10,8,6,4,2],
]

di = [-1,-1,1,1]
dj = [-1,1,-1,1]

N = len(arr)
i = 2
j = 3
sum_v = arr[i][j]
K = 2
for k in range(1,K+1):
    for d in range(4):
        #K번 더하면....길이 K짜리 십자기 만들기
        ni = i + di[d]*k
        nj = j + dj[d]*k
        if 0 <= ni < N and 0 <= nj < N:
            sum_v += arr[ni][nj]
print(sum_v)

max_v = 0
for i in range(N):
    for j in range(N):
        sum_v = arr[i][j]
        for d in range(4):
            ni = i + di[d]
            nj = j + dj[d]
            if 0 <= ni < N and 0 <= nj < N:
                sum_v += arr[ni][nj]
        if sum_v > max_v:
            max_v = sum_v
print(max_v)