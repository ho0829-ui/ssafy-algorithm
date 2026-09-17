# 행 하나에서 모든 열 선택해보기
# idx 번째 행에서 모든 열 선택해보기
# 중간합을 매 경우의수 비교
def solve(idx):
    global min_v
    if idx == N:    # 모든 경우의 수를 끝까지 보고 합구하기
        # print(selected)
        sum_v = sum(selected)
        if sum_v < min_v:
            min_v = sum_v
        return
    for i in range(N):  # i: 열번호
        if check[i] == 0:
            selected[idx] = data[idx][i]
            check[i] = 1
            solve(idx + 1)  # 다음 행 선택
            check[i] = 0 # 다 썼으니 체크 해제


def solve2(idx,sum_v):  # 중간합 구하기
    global min_v
    if sum_v > min_v: #나는 최소합을 구해야 하는데 이미 정답이 아님!
        return
    if idx == N:
        if sum_v < min_v:
            min_v = sum_v
        return
    for i in range(N):  # i: 열번호
        if check[i] == 0:
            check[i] = 1
            solve2(idx + 1, sum_v + data[idx][i])  # 다음 행 선택
            check[i] = 0 # 다 썼으니 체크 해제


T = int(input())
for tc in range(1,T+1):
    N = int(input())
    data = [list(map(int,input().split())) for _ in range(N)]
    # 완전탐색 >> 현재상황에서 모든 경우의 수 고려하기 *****
    #  행 하나에서 선택할 수 있는 열 모두 선택해보기
    # 내가 각 행에서 선택할 값을 저장할 배열
    selected = [0] * N
    check = [0] * N #열 중복 선택 확인 배열
    min_v = 10000
    solve2(0,0)
    print(f'#{tc} {min_v}')



