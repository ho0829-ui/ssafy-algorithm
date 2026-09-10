# nqueen 경우의 수 찾기
# N*N크기의 체스판에 N개의 퀸을 놓을 수 있는 경의 수 찾기
N = 4
case = [-1] * N
# 모든 경우의 수 다 살펴보기


# row 행에 퀸 놓아보기

def nqueen(row):
    if row == N: # 모든행에 숫자 넣어봤음!
        print(case)
        return
    for col in range(N):
        if check[col] == 0 and check_dia_1[row+col] == 0 and check_dia_2[row-col + 3] == 0:
        # if not check[col] and not check_dia_1[row + col] and not check_dia_2[row - col + 3]:
            case[row] = col
            check[col] = 1
            check_dia_1[row+col] = 1
            check_dia_2[row-col + 3] = 1
            nqueen(row+1)
            check_dia_1[row + col] = 0
            check_dia_2[row - col + 3] = 0
            check[col] = 0


check = [0] * N
check_dia_1 = [0] * (2*N -1)
check_dia_2 = [0] * (2*N -1)
nqueen(0)