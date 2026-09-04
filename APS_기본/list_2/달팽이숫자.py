N = 10
arr = [[0] * N for _ in range(N)]
# for row in arr:
#     print(row)

num = 1
r, c = 0, 0 # 시작점은 좌측 상단
#         우    하     좌      상
dirs = [(0,1),(1,0),(0,-1),(-1,0)]
# dr = [0,1,0,-1]
# dc = [1,0,-1,0]
d = 0 # 현재방향은 0으로 초기화
# 숫자넣고 다음칸 이동하는 것을 반복
while num <= N**2:  #N^2보다 작거나 같으면 숫자넣기 반복해라
    arr[r][c] = num
    for row in arr:
        print(row)
    print('=========================')
    r += dirs[d][0]
    # r += dr[d]
    c += dirs[d][1]
    # r,c가 정상 범위인지 확인, 정상범위가 아니라면...방향 바꿔주고 이동
    if r < 0 or r >= N or c < 0 or c >= N or arr[r][c] != 0:  #비정상!
        #원래자리로 가서 방향바꾸고 이동
        r -= dirs[d][0]
        # r += dr[d]
        c -= dirs[d][1]
        d = (d+1) % 4
        r += dirs[d][0]
        # r += dr[d]
        c += dirs[d][1]
    num += 1


