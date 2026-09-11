# 재귀로 DFS 구현하기
# 현재 정점에서 길찾기, 갈 수 있는 길이 있으면 이동
def dfs(v):
    global visited, result
    if v == 99:
        # 끝까지 온 것!
        result = 1
        return

    visited[v] = 1
    # 길은 최대 두 갈래. graph[v][0], graph[v][1] 을 보면 된다!
    for i in range(2):
        # v번과 연결된 정점(graph[v][i])이 있음!
        node = graph[v][i]
        if node is not None and not visited[node]:
            dfs(node)


def dfs2(v,visited):
    if v == 99:
        # 끝까지 온 것!
        return 1

    visited[v] = 1
    # 길은 최대 두 갈래. graph[v][0], graph[v][1] 을 보면 된다!
    for i in range(2):
        # v번과 연결된 정점(graph[v][i])이 있음!
        node = graph[v][i]
        if node is not None and not visited[node]:
            if dfs2(node,visited[:]) == 1:
                return 1
    return 0


T = 10
for _ in range(T):
    tc, N = map(int,input().split())
    edges = list(map(int,input().split()))
    # edges를 2개 씩 읽으면서 graph를 저장할건데
    # 2칸짜리 100개
    graph = [[None]*2 for _ in range(100)]
    # edges를 2개씩 읽으면서 그래프 저장
    for i in range(0,N*2,2):
        a, b = edges[i], edges[i+1]
        if graph[a][0] is None:
            graph[a][0] = b
        else:
            graph[a][1] = b
    # 0번에서 99번으로 갈 수 있냐???
    visited = [0] * 100
    # result = 0  # 일단은 목적지 못 가는걸로 설정
    # dfs(0)
    result = dfs2(0,visited)
    # print(result)
    print(f'#{tc} {result}')
