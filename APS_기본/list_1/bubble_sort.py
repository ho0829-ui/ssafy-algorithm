# 거품정렬
# [5,2,3,1,4]
# >> [1,2,3,4,5]
# 2개씩 비교해서 큰거 보내는 작업 * N번
# 2개씩 비교해서 큰거 뒤로 보내기
arr = [5,4,3,2,1]
N = len(arr)
for j in range(N-1):
    for i in range(N-1-j):
        # i번과 i+1번 비교해서
        # i번이 크면 자리 바꿔주기
        if arr[i] > arr[i+1] :
            # arr[i+1], arr[i] = arr[i], arr[i+1]
            tmp = arr[i]
            arr[i] = arr[i+1]
            arr[i+1] = tmp
            # 자리 바꿔주기
print(arr)






# 카운팅정렬