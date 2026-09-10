# 1. 그래프 저장하기
# 2. 그래프 순회하기(DFS)
# 정점의 개수와 간선의 개수
# 연결정보
# 7 8
# 1 2 1 3 2 4 2 5 4 6 5 6 6 7 3 7
V, E = map(int,input().split())
edges = list(map(int,input().split()))
# 인접행렬로 변환
# 인접행렬에서는 정점의 번호를 인덱스로 사용(정점이 7번까지있으니까 8칸 짜리 만들기)
adj = [[0]*(V+1) for _ in range(V+1)]
for i in range(0, E*2, 2):

    s = edges[i]
    e = edges[i+1]
    adj[s][e] = 1
    adj[e][s] = 1
# v: 현재정점에서 길찾기....
visited = [0] * (V+1)
def dfs(v):
    # 현재 정점에서 길찾기 : 갈 수 있는 길이 있으면 이동
    # 현재 정점과 인접한 정점 살펴보기
    visited[v] = 1
    print(v,end=' ')
    for i in range(1,V+1):
        if adj[v][i] and not visited[i]:
            dfs(i)


dfs(1) #1번 정점에서 DFS 시작!







