
# bit의 모든 인덱스에 넣을 수 있는거 다 넣어보기

# bit[0] < 0, 1
# bit[1] < 0, 1
#  bit[2] < 0, 1
# for i in range(2):
#     bit[0] = i
#     for j in range(2):
#         bit[1] = j
#         for k in range(2):
#             bit[2] = k
#             print(bit)

# idx 번째에 0또는 1넣기
arr = ['A','B','C']
# 부분집합의 모든 모양 구하기
N = len(arr)
bit = [0] * N  # 부분집합의 모양 [0, 0, 0]
def zero_one(idx):
    #idx N-1번까지는 동작하는데.. N번이면 에러
    if idx == N:
        # print(bit) #부분집합의 모양을 구했으니까..모양대로 부분집합 출력하기
        # bit[i]가 1이라면 i번 요소는 부분집합에 포함된다.
        print('[',end=' ')
        for i in range(N):
            if bit[i]:
                print(arr[i],end=' ')
        print(']')
        return
    for i in range(2):
        bit[idx] = i
        zero_one(idx+1)
zero_one(0)




