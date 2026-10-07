# 각 제품을 모든 공장에서 만들어보기
# idx번 제품을 모든 공장에서 만드는 비용
def solve(idx,cost):
    global min_cost
    # 중간 계산 결과가 이미 내가 알고 있는 최소값보다 크니까
    # 연산 해 볼 필요 없음
    if cost >= min_cost:
        return

    if idx == N:    # 모든 물건을 다 만들어봤으면
        # print(cost)
        if cost < min_cost:
            min_cost = cost
    # A공장 :0 번, B공장 : 1번, C공장 : 2번
    # idx번 제품을 A공장에서 생산할 경우 비용
    for i in range(N):
        # 하나의 물품을 생산할 공장을 결정했으면
        # 다음 물품 생산 해보러 가기..
        if not check[i]:
            check[i] = 1    # i번 공장 사용
            solve(idx+1,cost + data[idx][i])
            check[i] = 0    #i번 공장 사용 완료...

T = int(input())
for tc in range(1,T+1):
    N = int(input())
    data = [list(map(int,input().split())) for _ in range(N)]
    check = [0] * N
    min_cost = 10000
    solve(0,0)
    print(f'#{tc} {min_cost}')