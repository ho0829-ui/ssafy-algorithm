import sys
sys.stdin = open('전기버스_input.txt','r')
# 이전 충전 정류장에서 현재 정류장에 올 수 있는지 확인
# 만약에 도착이 불가능하면 직전 정류장에서 충전해야 한다!
# 마지막 충전 정류장을 저장하면서 풀이 진행...
T = int(input())
for tc in range(1,T+1):
    K, N, M = map(int,input().split())
    stations = list(map(int,input().split()))

    last = 0 #마지막 충전위치
    cnt = 0 # 충전횟수

    # 1. 현재 정류장과 이전 정류장의 거리 차이 구하기.. K를 초과하면 목적지 도착 불가능
    # 2. 마지막 충전소에서 현재 정류장에 도착가능한지 확인하고, 도착 불가능하면 이전 정류장에서 충전하기
    stations.insert(0,0)
    stations.append(N)
    # print(stations)
    for i in range(1,M+2): #시작 정류장과 목적지 정류장 추가
        # 현재 정류장과 이전 정류장의 거리 차이 구하기
        if stations[i] - stations[i-1] > K:
            # 도착가능하면......
            cnt = 0 # 목적지 도착 불가능
            break   # 더이상 안 돌아도 됩니다.
        # 마지막 충전소에서 현재 정류장에 도착가능한지 >> 도착 가능하면 아무것도 안하고 진행
        # 도착 불가능하면 >> 이전 정류장에서 충전하기
        if last + K < stations[i]: # 도착 불가능
            last = stations[i-1]     # 이전 정류장에서 충전!
            cnt += 1

    print(f'#{tc} {cnt}')