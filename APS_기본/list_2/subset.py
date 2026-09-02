# 부분집합 만들기
# 각 요소의 포함 여부를 표시하는배열
arr =   ['A','B','C']
N = len(arr)
check = [0] * N # 각 요소의 포함 여부를 표시하는배열
for i in range(2):
    check[0] = i
    for j in range(2):
        check[1] = j
        for k in range(2):
            check[2] = k
            print(check)
            for l in range(N): # 부분집합 모양 검사,
                # l번째 요소가 부분집합 포함되는지 확인
                if check[l] == 1:
                    print(arr[l],end=' ')
            print()