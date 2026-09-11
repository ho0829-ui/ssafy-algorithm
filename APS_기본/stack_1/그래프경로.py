def dfs(S,G):
    stack = [S]
    visited = [0] * (V+1)
    visited[S] = 1

    while stack:
        # 현재 위치에서 갈 수 있는 길 찾고, 찾으면 이동
        # 없으면 현재위치 제거(되돌아가기)
        current = stack[-1]
        if current == G:
            return 1
        is_noway = True
        for i in range(1,V+1): #연결정보 확인...
            # current 정점과 i번 정점이 연결되어 있고
            # i번정점에 아직 방문하지 않았으면
            if graph[current][i] and not visited[i]:
                visited[i] = 1
                stack.append(i) # 경로에 i번 추가 (방문)
                is_noway = False
                break
        if is_noway:  #길 없다면..
            #현재 위치를 경로에서 제거(되돌아가기)
            stack.pop()
    # 목적지에 도착하지 못하고 길찾기가 끝났음!
    return 0



T = int(input())
for tc in range(1,T+1):
    V, E = map(int,input().split())
    # 그래프 정보를 입력 받기 위해서
    # 그래프를 준비 : 인접행렬
    graph = [[0] * (V+1) for _ in range(V+1)]
    #간선의 개수가 E개
    for _ in range(E):
        start, end = map(int,input().split())
        graph[start][end] = 1

    S, G = map(int,input().split())
    #S에서 DFS 수행해서 G로 갈 수 있으면 연결된거...
    result = dfs(S,G)
    print(f'#{tc} {result}')




















