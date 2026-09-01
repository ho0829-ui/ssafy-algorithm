T = 10
for tc in range(1,T+1):
    N = int(input())
    buildings = list(map(int,input().split()))
    # 각 건물의 조망권이 확보된 세대수 합 구하기
    sum_v = 0
    # 각 건물의 조망권 계산하기
    for i in range(2,N-2):
        #i : 건물번호
        # i번 건물의 양쪽 2칸 보기 i-2 ~ i+2번까지 (i는 제외)
        # 건물 네개 중에 제일 높은건물 높이 찾기
        max_height = 0
        for j in range(i-2,i+3):
            if j == i: continue #아무것도 하지마라...현재건물은 비교대상에서 제외
            if buildings[j] > max_height:
                max_height = buildings[j]
        # 현재건물 (building[i])이 주변 건물보다 높을 때만....(조망권이 있을 때만)
        if buildings[i] > max_height:
            sum_v = sum_v + (buildings[i] - max_height)

    print(f'#{tc} {sum_v}')






