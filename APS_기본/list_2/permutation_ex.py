#순열 (수열이 있을 때 가능한 모든 순서 나열...)
# 완전탐색(완전검색): 모든 경우의 수 살펴보기
# 1,2,3
# 1 2 3, 1 3 2, 2 1 3, 2 3 1, 3 1 2, 3 2 1
arr = [1,2,3]
N = len(arr)
perm = [0] * N # 순열이 저장될 배열, 숫자의 숫서를 바꿔가며 나열하기
#perm의 0번에 1,2,3 넣어보기
#perm의 1번에 1,2,3 넣어보기 할거고...
# .....
# for i in range(N): #perm 의 인덱스, 0 번째 칸에 숫자 넣기
#     perm[0] = arr[i]
#     for j in range(N):
#         if j == i:
#             continue
#         perm[1] = arr[j]
#         for k in range(N):
#             if k == i or k == j:
#                 continue
#             perm[2] = arr[k]
#             print(perm)

# 특정 인덱스에 모든 요소 넣어보기
# 앞 idx에서 사용한건 사용안했으면...좋겠는데...

def func_perm(idx):
    if idx == N: #이건 실행하면 안됨!
        print(perm)
        return
    for i in range(N):
        # check 안 된,표시 없는것만 써라...
        if not used[i]:
            perm[idx] = arr[i]
            used[i] = 1
            func_perm(idx + 1)
            used[i] = 0

used = [0] * N   #

func_perm(0)