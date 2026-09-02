T = int(input().strip())

for t in range(1, T + 1):
    N, M = map(int, input().split())

# N x N 배열 입력 받기
grid = []
for r in range(N):
    row = list(map(int, input().split()))
    grid.append(row)

max_flies = 0

# M x M 파리채를 내리칠 수 있는 모든 시작 위치(r, c) 순회
for r in range(N - M + 1):
    for c in range(N - M + 1):
        current_sum = 0

        # 파리채 영역 내부의 파리 수 합산
        for i in range(M):
            for j in range(M):
                current_sum += grid[r + i][c + j]

        # 최댓값 갱신
        if current_sum > max_flies:
            max_flies = current_sum

print(f"#{t} {max_flies}")