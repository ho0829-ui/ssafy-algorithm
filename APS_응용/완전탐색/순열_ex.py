arr = ['A','B','C']
N = len(arr)
# 1,2,3 으로 만들 수 있는 모든 순서
perm_arr = [None] * N   # 순열을 만들기 위한 배열
check = [0] * N
# perm_arr의 idx에 들어갈 수 있는 요소 다 넣어보기
def perm(idx):
    if idx == N: #N-1번까지 숫자를 다 넣음
        print(perm_arr)
        return
    # perm_arr의 idx 번에 모든 요소 넣기
    for i in range(N):
        # 중복 아닌 애들만 넣기!
        if check[i] == 0:   # 표시 없는 애들만 골라서 사용
            perm_arr[idx] = arr[i]
            check[i] = 1    # i번째 요소를 썼음을 표시
            perm(idx + 1)
            check[i] = 0  # i번째 요소 다 썼으니 표시 지우기
perm(0)