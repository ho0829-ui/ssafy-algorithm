'''
7 8
1 2 1 3 2 4 2 5 4 6 5 6 6 7 3 7
'''

def dfs(start, N): # 모든 정점을 중복없이 빠짐없이 방문
    visited = [0] * (N + 1)     # 방문기록 배열 생성
    stack = []                  # 스택 생성
    v = start                   # 시작점 방문 (방문한 위치 v)
    print(v)                    # 방문해서 할 일 - 정점 번호 출력
    visited[v] = 1              # 방문 표시

    while True:                 # 반복
        for w in adj_list[v]:   # 현재 방문한 v에 인접한 정점 w가 있고
            if visited[w] == 0: # 아직 방문 전이면
                stack.append(v)     # 막혔을 때 되돌아올 자리 push
                visited[w] = 1      # 방문 표시
                v = w  # w를 현재 방문한 위치로
                print(v)
                # w를 새로운 방문지 v로 해서 반복 -> for w로 이동
                break       # for w, 새로 이동한 정점 v부터 다시 탐색 반복
        else:                   # v에 인접한 w가 더이상 없으면
            if stack:           # 최근에 지나온 곳부터 다시 탐색
                v = stack.pop()
            else:               # 남은 경로가 없으면/스택이 비어있으면
                break           # while True



V, E = map(int, input().split())
graph = list(map(int, input().split()))
adj_list = [[] for _ in range(V+1)]         # 인접 리스트
for i in range(E):
    v, w = graph[i*2], graph[i*2+1]     #

    adj_list[v].append(w)
    adj_list[w].append(v)                 # 방향이 없는 경우

dfs(1, V)                           # 1번부터 탐색

