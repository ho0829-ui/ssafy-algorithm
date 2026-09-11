# 주어진 NXN 크기의 미로에서 출발지(2)부터 목적지(3)까지 갈 수 있는 경로가 존재하는지 판단하는 문제
import sys
sys.stdin = open('미로_input.txt','r')

# 0: 통로, 1: 벽, 2: 출발지, 3: 목적지
T = int(input())
for tc in range(1, T+1):
    N = int(input())
    arr = [list(map(int, input().strip())) for _ in range(N)] # 2차원 리스트(미로판)로 저장

    # 출발지 설정
    start_r, start_c = -1, -1
    for r in range(N):
        for c in range(N):
            if arr[r][c] == 2:
                start_r, start_c = r, c
                break
    # 이동경로
    stack = []
    # 방문확인
    visited = [[0]* N for _ in range(N)]
    # 시작점 표시(출발지를 스택에 넣어서 탐색 시작)
    stack.append((start_r,start_c))
    visited[start_r][start_c] = 1

    # 이동방향: 상, 하, 좌, 우
    dr = [-1, 1, 0, 0] # 행
    dc = [0, 0, -1, 1] # 열

    # 결과 : 도착하면 1, 아니면 0 (기본값 = 도착 못 함)
    result = 0

    # 스택이 비었다는 건 갈 수 있는 길이 없어 되돌아오면서 길을 탐색해도 길이 없음
    while stack:
        # 현재 위치
        cr,cc = stack[-1]
        # 위치 값이 3이면 도착
        if arr[cr][cc] == 3:
            result = 1
            break

        # 길을 따라 이동해보기
        for d in range(4):
            nr = cr + dr[d]
            nc = cc + dc[d]
            # 갈 수 있는 길인지 확인
            # 갈 수 없는 길 : 미로를 벗어나는 경우, 벽, 이미 방문한 곳
            # 조건: 행과 열이 미로 범위 안, 벽(1)이 아님, 아직 방문 안 한 곳
            if 0 <= nr < N and 0 <= nc < N and arr[nr][nc] != 1 and visited[nr][nc] == 0:
                # 갈 수 있는 길이니 이동해보기
                stack.append((nr,nc))
                visited[nr][nc] = 1
                break
        # break을 만나지 않았다는 것은 갈 길이 없다는 것 -> 한 칸 되돌아 가보자
        else:
            stack.pop()

    print(f'#{tc} {result}')