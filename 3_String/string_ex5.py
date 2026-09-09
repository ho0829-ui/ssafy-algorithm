N = int(input())
text = [input() for _ in range(N)]

ans = 0     # 4방향이 모두 통로인 칸 수
for i in range(N-1):
    for j in range(N-1):
        if text[i][j] != '1': # 벽이 아니면
            cnt = 0         # 현재 위치에서 주변의 통로개수
            for di, dj in [[0,1],[1,0],[0,-1],[-1,0]]:
                ni = i + di
                nj = j + dj
                if 0<=ni<N and 0<=nj<N:
                    if text[ni][nj] != '1':
                        cnt += 1
            if cnt == 4:
                ans += 1
print(ans)
