T = int(input())
for test in range(1, T + 1):
    N, M = map(int, input().split())

    arr_N = list(map(int, input().split()))
    arr_M = list(map(int, input().split()))

    arr_N.sort(reverse=True)
    arr_M.sort(reverse=True)

    cnt = 0
    Sum = 0
    idx = 0
    truck = 0

    while True:
        if idx == N or truck == M:
            break
        if arr_M[truck] >= arr_N[idx]:
            print(truck, arr_N[idx])
            Sum += arr_N[idx]
            # cnt += 1
            truck += 1
        idx += 1

    print(arr_N)
    print(arr_M)
    print(Sum, cnt)
    print()
    print(f'#{test} {Sum}')