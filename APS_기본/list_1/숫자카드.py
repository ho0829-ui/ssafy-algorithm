T = int(input())
for test in range(1, T + 1):

    N = int(input())
    num = int(input())
    K = 10  # 문제의 최대값 9 따라서 9+1=10

    lst = [0] * N  # 빈 리스트 생성
    i = N  # 숫자의 크기 N

    while i > 0:  # 자릿수 나눠서 리스트 저장 해서 리스트
        i -= 1
        lst[i] = num % 10
        num //= 10
    print(lst)
    arr = [0] * K  # 카운트 리스트 생성
    max_n = max_v = 0  # 최대 갯수, 최대 값

    for i in range(N):  # lst을 돌면서 lst를 인덱스로 해서 카운팅 정렬
        arr[lst[i]] += 1
    print(arr)

    for i in range(K):  # 카운트 리스트를 전체를 돌면서 현재 값 확인
        curr = arr[i]

        if max_v <= curr:  # 최대 값 확인
            max_v = curr
            max_n = i

    print(f'#{test} {max_n} {max_v}')













