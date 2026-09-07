# 이동 방향을 상,좌,우 로 설정
# 상방향 이동중 : 좌우 살피면서 이동
# 좌,우 이동중 : 상 살피면서 이동
# 이동할 수 있으면 방향 바꾸고 이동
import sys
sys.stdin = open('ladder_input.txt','r')
T = 10
# 2번 도착지에 도착할 수 있는 시작점 번호 반환
def solve(ladder):
    #상 좌 우
    dr = [-1, 0, 0]
    dc = [0, -1, 1]
    # 시작은 값이 2인 열에서 시작하면
    r = 99
    c = 0 #임의의 값

    for i in range(100):    # 시작점 열 찾기 반복문
        if ladder[r][i] == 2:
            c = i
            break
    # 시작점 찾았으니....한 칸씩 이동하기 반복
    d = 0   # 현재 이동하는 방향을 저장하는 변수
    while r > 0:
        # if r == 0:  # 목적지 도착했으니
        #     break   # 멈춰!
        #현재 이동방향에 맞게...살피면서 이동
        if d == 0: #위로 이동중...
            # 좌우 살펴보고 갈 수 있으면 방향바꾸기
            if c - 1 >= 0 and ladder[r][c-1] == 1: # 왼쪽에 길이 있다!
                d = 1   #
            if c + 1 <= 99 and ladder[r][c+1] == 1: # 오른쪽에 길이 있다!
                d = 2
        elif d ==1 :    #왼쪽, 
            # 윗 방향 살펴보고 갈 수 있으면 방향바꾸기
            if ladder[r-1][c] == 1:
                d = 0
        else: # 오른쪽
            if ladder[r-1][c] == 1:
                d = 0
        # 방향대로 한 칸 이동하기
        r += dr[d]
        c += dc[d]
    # while문을 빠져나왔다는건....r == 0 이라는 이야기고 도착했으니
    return c

for _ in range(1,T+1):
    tc = input()
    ladder = [list(map(int,input().split())) for _ in range(100)]
    result = solve(ladder)
    print(f'#{tc} {result}')