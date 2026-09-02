T = int(input()) # 테스트 케이스 넘버 받기
for test_case in range(1, T + 1): # 테스트 케이스 for문 돌리기
    N = int(input()) # 색칠되는 영역 수 받기
    box = [[0] * 10 for _ in range(10)] #0으로 채워진 2차원 배열 생성
    for n in range(N): # 영역별로 색 채우기 위해 for문 돌림
        r1, c1, r2, c2, color = list(map(int, input().split())) # 범위와 색상 입력 받음
        for i in range(r1, r2+1): # 가로열 색칠할 범위 for문으로 정해주고
            for j in range(c1, c2+1): # 세로열도 정해서
                box[i][j] += color # 색칠함, 주어진 정보에서 같은 색인 영억은 겹치지 않기에 그냥 더해도 중복이 발생안함

    cnt = 0 # 보라색 갯수는 0으로 초기화
    for i in range(10): # 가로 범위 잡고
        for j in range(10): # 세로 범위 잡아서
            if box[i][j] == 3: # 보라색인 칸 찾아서
                cnt +=1 # 카운팅

    print(f'#{test_case} {cnt}')