maze = [
[2,1,1,3,0,0],
[0,0,1,0,0,0],
[0,0,1,0,0,0],
[1,1,1,1,1,2],
[0,0,1,0,0,0],
[0,0,2,0,0,0]
]
N = 6
dr = [-1,1,0,0]
dc = [0,0,-1,1]
visited = [[0]* N for _ in range(N)]
# 현재 위치에서 길찾기
# r : row, c : column
def dfs(r,c):
    # 현재 위치에서 갈 수 있는 길 다 찾아보기
    # 상하좌우 보기
    visited[r][c] = 1
    if maze[r][c] == 2:
        print("목적지 도착!")
        return
    for d in range(4):
        tr = r + dr[d]
        tc = c + dc[d]
        if 0 <= tr < N and 0 <= tc < N and not visited[tr][tc]:
            if maze[tr][tc] != 0:
                dfs(tr,tc)

for i in range(N):
    for j in range(N):
        if maze[i][j] == 3:
            dfs(i,j)

