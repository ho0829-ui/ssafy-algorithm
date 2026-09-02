# 표준입력 스트림 : 터미널로 기본 설정 되어있음, 파일로 변경하면 파일에서 입력받기
import sys
sys.stdin = open('전기버스_input.txt','r')
# sys.stdout = open('전기버스_output.txt','w')

# 손으로 풀리는지 풀어보기!
# 현재 위치에서 갈 수 있는 위치에 충전소가 있는지 확인
# 없으면 뒤로 되돌아 가면서 충전하기
T = int(input())
for tc in range(1,T+1):
    # K는 충전량, N 정류장 개수, M 충전기 개수
    K, N, M = map(int,input().split())
    charger = list(map(int,input().split()))
    stations = [0] * (N+1)
    for idx in charger:
        stations[idx] = 1
    # for i in range(M):
    #     stations[charger[i]] = 1
    # [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    # print(stations)
    #현재 위치에서 갈 수 있는 정류장부터 충전기가 있는지 검사
    # 없으면 되돌아가기
    # 충전기가 있으면 충전하기 >> 반복! 목적지에 도착할 때 까지 반복
    position = 0    # 현재위치
    cnt = 0 # 충전 횟수 세기 변수
    while position + K < N: # 충전기 찾아서 충전하기 반복
        # 갈 수 있는데 까지 가서 되돌아 오면서 찾기
        is_find = False
        for next in range(position+K,position,-1):
            if stations[next] == 1: #충전기 있니?
                cnt += 1 #충전하고 다음충전소 찾기
                position = next
                is_find = True
                break  #돌아가면서 찾기 중단
        #충전소 찾는 반복문에서 충전소 찾았니??
        if is_find == False:
            cnt = 0   #목적지 도착 못 할 경우 0출력
            break
    print(f'#{tc} {cnt}')