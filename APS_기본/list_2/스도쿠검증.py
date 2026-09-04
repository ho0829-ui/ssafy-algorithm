import sys
sys.stdin = open('스도쿠_input.txt','r')

def solve(puzzle):
    '''
    인자로 받은 9*9 행렬이 스도쿠라면...1을 반환 아니라면 0을 반환
    '''
    # puzzle을 행 우선순회하면서 각 행에 1-9까지 들어갔는지 확인

    for i in range(9):
        # 행 하나에 숫자가 중복으로 나오는지 확인
        check = [0] * 10
        for j in range(9): # 행 하나(i번째 행)를 순회하는 반복문
            # puzzle[i][j] 행을 이루는 숫자 하나
            if check[puzzle[i][j]] == 1: # 중복이네?
                return 0
            check[puzzle[i][j]] = 1
    # 열검사
    for i in range(9):
        # 열 하나에 숫자가 중복으로 나오는지 확인
        check = [0] * 10
        for j in range(9): # 열 하나(i번째 행)를 순회하는 반복문
            # puzzle[j][i] 열을 이루는 숫자 하나
            if check[puzzle[j][i]] == 1: # 중복이네?
                return 0
            check[puzzle[j][i]] = 1

    # 3*3 행렬 검사
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            #시작점에서 3*3 돌면서 중복검사
            check = [0] * 10
            for r in range(i,i+3):
                for c in range(j,j+3):
                    # check[puzzle[r][c]]==1  >>  if check[puzzle[r][c]]: 써도 같은 뜻
                    if check[puzzle[r][c]]:
                        return 0
                    check[puzzle[r][c]] = 1

    return 1
T = int(input())
for tc in range(1,T+1):
    # data = []
    # for _ in range(9):
    #     data.append(list(map(int,input().split())))
    data = [list(map(int,input().split())) for _ in range(9)]
    # for row in data:
    #     print(row)
    # print('====================================')
    result = solve(data)
    print(f'#{tc} {result}')