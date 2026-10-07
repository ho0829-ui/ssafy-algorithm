# Kruskal : MST를 만드는 알고리즘
# 1. 간선 비용기준 오름차순 정렬
# 2. 비용이 작은 간선 부터 선택
# 3. 단, 간선을 선택하는 과정에서 '사이클'이 발생하면,
#    해당간선은 선택하지 않음
#(정점을 같은 간선을 두 번 지나지 않고 되돌아 올 수 있으면 사이클)

#사이클 판단은 어떻게 하냐??
# 연결이 되면 같은 그룹으로 구성, 같은그룹안의 정점을 연결하는 사이클을 발생시킴!
# 6 11
# 0 1 32
# 0 2 31
# 0 5 60
# 0 6 51
# 1 2 21
# 2 4 46
# 2 6 25
# 3 4 34
# 3 5 18
# 4 5 40
# 4 6 51

# 그룹 나누기
# 각 정점을 대표자를 설정, 시작은 각 정점을 모두 다른 그룹으로 만들기
V, E = map(int,input().split())
edges = [list(map(int,input().split())) for _ in range(E)]
print(edges)
# 각 정점의 부모를 저장하는 배열
p = [x for x in range(V+1)]
print(p)

# 정점의 대표찾기
def find_set(x):
    # 정점의 부모 번호가 스스로 라면, 해당정점은 그룹의 대표자
    if p[x] == x:
        return x
    # 정점의 부모가 스스로가 아니라면, 부모의 대표자를 찾아서 반환
    return find_set(p[x])
# 두 정점을 하나의 그룹으로 만들기(union)
# - 두 정점의 대표를 하나로 만들어주기, 각 정점의 대표찾기
# 
def union(x,y):
    # x의 대표를 y의 대표로 만들면(혹은 반대로..)같은 그룹이 된다.
    px = find_set(x)   # px의 부모는 px
    py = find_set(y)   # py의 부모는 py
    p[py] = px

def kruskal():
    edges.sort(key=lambda x:x[2])
    #모든 간선에 대해서 선택 여부 판단
    MST = []
    for edge in edges:
        # 선택 했을 때, 사이클이 안생기면 선택 : 두 정점이 같은 그룹이 아니라면 선택
        a,b, weight = edge
        if find_set(a) != find_set(b):  #각 대표자가 다르면 다른그룹이니까 사이클이 생기지 않음
            union(a, b) #선택했으니까 같은 그룹으로 만들어주기
            MST.append(edge)
    return MST

print(kruskal())


# print(find_set(2))  #2의 대표자 출력
# print(find_set(3))  # 3의 대표자 출력
# union(2,3)
# print('------------------------')
# print(find_set(2))  # 2의 대표자 출력
# print(find_set(3))  # 3의 대표자 출력
# print(find_set(4))
# union(4,3)
# print('###############################')
# print(find_set(2))  # 2의 대표자 출력
# print(find_set(3))  # 3의 대표자 출력
# print(find_set(4))


















