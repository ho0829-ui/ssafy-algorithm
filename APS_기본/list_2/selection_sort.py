# 선택정렬 : 그 자리에 들어갈 숫자 선택해서 넣어주기..
# 인덱싱 연습 3대장...
arr = [5,7,1,2,3,4,6]
N = len(arr)
#숫자가 들어갈 자리 찾기
for i in range(N-1):
    # i번째에 들어갈 숫자찾기(최소값)
    # 비교 대상은 i번 부터 N-1번
    min_idx = i
    for j in range(i,N):    #최소값 위치 찾기
        if arr[j] < arr[min_idx]:
            min_idx = j
    # i번에 들어갈 숫자 찾는건데..min_idx 번에 들어있음
    arr[i], arr[min_idx] = arr[min_idx], arr[i]

print(arr)