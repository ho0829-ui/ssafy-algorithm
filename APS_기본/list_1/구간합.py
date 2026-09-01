# 요소의 개수가 N개인 배열에서
# 길이 M인 모든 구간의 합을 구하기
# 길이 M인 모든 구간의 합을 구하기 위해서
# 구간의 시작점을 설정 :
# 시작점 : 0번 부터 N-M번까지
# 각 시작점에서 길이 M 만큼의 합구하기
T = int(input())
for tc in range(1, T+1):
    # 테스트 케이스의 첫번째 줄 입력받기
    N, M = map(int, input().split())
    # 테스트 케이스의 두 번째줄 입력받기
    numbers = list(map(int,input().split()))

    max_sum = 0
    min_sum = 1000000

    # 시작점이 여러개니까...시작점먼저 설정
    for i in range(N-M+1): # 시작점은 0번 부터 N-M번까지
        # 각 시작점에서 길이 M 만큼의 합구하기
        # i 번 부터 i+M-1 번까지 돌면서 합구하기
        sum_v = 0
        for j in range(i,i+M):  # 구간을 순회하는 반복문
            # sum_v = sum_v + numbers[i]
            sum_v += numbers[j]

        if sum_v > max_sum:
            max_sum = sum_v
        if sum_v < min_sum:
            min_sum = sum_v

    print(f'#{tc} {max_sum-min_sum}')





