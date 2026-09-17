def f(T, a):    # 첫 번째 a 왼쪽 조상의 값
    if T > N:   # 존재하지 않는 정점(자식)이면
        return 0
    l = f(T * 2, a)
    tree[T] = l + a + 1
    r = f(T * 2 + 1, tree[T])
    return l + r + 1

T = int(input())
for tc in range(1, T+1):
    N = int(input())

    tree = [0] * (N + 1)    # 완전이진트리를 저장할 배열

    f(1, 0)              # 완전이진트리의 루트는 1

    print(f'#{tc} {tree[1]} {tree[N//2]}')