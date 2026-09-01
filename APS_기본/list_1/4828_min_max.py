# 문제를 풀건데, 그 개수가 T개
# 문제 풀기를 T 번 반복

# 테스트 케이스 입력은 각 2줄
# 테스트 케이스가 T개
T = int(input()) #문자열 3을 숫자로 바꿔서 T에 저장
# 테스트케이스 입력 받기  T 번 반복
for tc in range(1,T+1):
    # 테스트 케이스의 첫 번째 줄에는 숫자의 개수
    # 테스트 케이스의 두 번째 줄에는 숫자들
    N = int(input())
    # numbers = input()   # '477162 658880 751280 927930 297191'
    # input()를 자르고 숫자로 바꾸기
    # 1. 띄어쓰기 기준으로 자르기 input().split() : ['477162', '658880', '751280', '927930, '297191']
    # print(input().split())
    # 2. 모든 요소에 int()적용하기
    numbers = list(map(int,input().split()))
    # print(numbers)
    # numbers 에서 최대값 찾기
    # 빈칸 하나 만들어놓고,
    # 배열 하나씩 보면서 빈칸에 들어있는 값보다 현재값이 더 크면 바꿔주기
    max_v = 0
    for i in range(N):  # numbers를 살펴보는 반복문
        if numbers[i] > max_v:
            max_v = numbers[i]
    min_v = 9999999999   # numbers의 요소가 min_v 보다 더 작으면 min_v 값 바꾸기
    for i in range(N):
        if numbers[i] < min_v:
            min_v = numbers[i]

    print(f'#{tc} {max_v - min_v}')