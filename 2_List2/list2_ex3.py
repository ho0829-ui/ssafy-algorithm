#arr = [-7, -5, 2, 3, 8, -2, 4, 6, 9, 12]
arr = [1,2,3]
N = len(arr)

ans = 'N'
for i in range(1, 1<<N):   # 2**N, 부분집합을 표현할 비트 생성
    s = 0
    for j in range(N):  # 검사할 비트 번호 j
        if (i & (1 << j)):  # j번 비트가 1이면 arr[j]가 부분집합의 원소
            s += arr[j]
    if s == 0:
        ans = 'Y'
        break # for i
print(ans)