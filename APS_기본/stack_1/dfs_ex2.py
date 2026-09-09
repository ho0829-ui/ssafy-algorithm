# 2차원 행렬에서 dfs
# 전에는 그래프 표현으로 인접행렬을 사용...
# 연결 정보를 인접행렬을 이용해서 확인

# 2차원 행렬 >> 연결 정보를 확인할 필요도 없음....어차피 상하좌우 연결이니까
# 네 개만 보면된다..델타만 하면 됩니다.
# 정점 하나를 좌표로 표현 (r,c) 나랑 인접한 정점은 (r-1,c),(r+1,c), (r,c-1), (r,c+1)
# 0 : 벽, 1은 통로, 2는 시작점, 3은 도착점
maze1 = [
    [0,1,0,0,0],
    [1,2,1,1,1],
    [0,0,0,1,0],
    [0,1,0,1,0],
    [3,1,1,1,0]
]
maze2 = [
    [0,1,0,0,0],
    [1,2,1,1,1],
    [0,0,0,0,0],
    [0,1,0,1,0],
    [3,1,1,1,0]
]
# 목적지에 도착할 수 있는지 여부 출력

def dfs(maze):
    #시작점에서 목적지로 갈 수 있으면 1반환 없으면 0 반환
    N = len(maze)

    #시작점 찾기#
    for i in range(N):
        for j in range(N):
            if maze[i][j] == 2:
                sr = i
                sc = j
    ################################
    stack = []
    stack.append((sr,sc))
    #미로와 동일한 모양의 visited 배열
    visited = [[0]* N for _ in range(N)]
    visited[sr][sc] = 1

    while stack:
        cr, cc = stack[-1]   #현재 위치
        if maze[cr][cc] == 3:
            return 1
        #현재위치에서 길찾기 >> 상하좌우 살피기
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr = cr + dr
            nc = cc + dc
            if 0<= nr < N and 0<= nc < N and maze[nr][nc] != 0 and visited[nr][nc] == 0:
                stack.append((nr,nc))
                visited[nr][nc] = 1
                break
        else:   # 길없으면 되돌아가라...
            stack.pop()
    # 갈 수 있는길 찾아봤는데...목적지가 없더라..
    return 0
print(dfs(maze1))
print(dfs(maze2))