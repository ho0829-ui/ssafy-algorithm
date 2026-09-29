# 한 인덱스에서 할 수 있는거 다해보기
#부분집합
arr = [1,2,3]
N = len(arr)
bit = [0] * N

def ps(idx):
    if idx == N:
        print(bit)
        return
    for i in range(2):
        bit[idx] = i
        ps(idx + 1)

#순열
perm =[None] * N # [A, C ,C]
# 쓴거 체크
# [A,B,C]
# [1,0,0]
check = [0] * N
def permutation(idx):
    if idx == N:
        print(perm)
        return
    for i in range(N):
        if check[i] == 0:
            perm[idx] = arr[i]
            check[i] = 1 #썼음!
            permutation(idx+1)
            check[i] = 0

def perm2(idx):
    if idx == N:
        print(arr)
        return
    # 현재 인덱스랑 (내 뒤 인덱스랑 )바꿀 수 있는것 다 바꿔보기기
    for i in range(idx,N):
        arr[idx], arr[i] = arr[i], arr[idx]
        perm2(idx+1)
        arr[idx], arr[i] = arr[i], arr[idx]

perm2(0)

#
# idx 번째 숫자 조합에 포함여부 표시
bit = [0] * N
M = 2
def comb(idx,cnt):   # 내가 몇 개 뽑았는지 알아야 함
    if cnt == M:
        print(bit)
        return
    if idx == N:    # 조합 만들기 실패
        return
    # for i in range(2):
    #     bit[idx] = i
    #     comb(idx + 1,cnt + i)
    bit[idx] = 0
    comb(idx + 1, cnt)
    bit[idx] = 1
    comb(idx + 1, cnt + 1)
    bit[idx] = 0

M = 3
arr = [1,2,3,4,5]
N = len(arr)
combination = [0] * M
def comb2(idx,start):
    if idx == M:
        print(combination)
        return
    # 다 넣어보긴 할건데...이전에 선택한거 다음거 부터
    for i in range(start,N):
        combination[idx] = arr[i]
        # i번을 idx에 넣으면.... idx+1번에는 i+1 부터 넣으면 됨
        comb2(idx+1,i+1)

comb2(0,0)





# permutation(0)
# comb(0,0)