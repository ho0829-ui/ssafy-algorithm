arr = [6,8,1,3,4,5,9,2,7]
# 전체를 정렬하기 위해서 절반을 각각 정렬해서 합치기
# 정렬할 대상을 인덱스로 정의
def merge_sort(s,e):
    if s == e: #정렬 대상 범위에 요소가 하나인 경우에는 정렬필요 X
        return
    mid =  (s + e) // 2
    #왼쪽 절반정렬
    merge_sort(s,mid)
    #오른쪽 절반정렬
    merge_sort(mid+1,e)

    sorted_arr = []
    i = s
    j = mid + 1

    while i <= mid and j <= e:
        if arr[i] < arr[j]: # 왼쪽이 더 작으면...
            sorted_arr.append(arr[i])
            i += 1
        else:   # 오른쪽이 작거나 같으면..
            sorted_arr.append(arr[j])
            j += 1
    # 남아있으면 붙이기
    while i <= mid:
        sorted_arr.append(arr[i])
        i += 1
    while j <= e:
        sorted_arr.append(arr[j])
        j += 1

    # 원본배열에 임시 저장배열 붙여넣기
    b = 0
    for a in range(s,e+1):
        arr[a] = sorted_arr[b]
        b += 1



N = len(arr)
merge_sort(0,N-1) # 시작은 전체범위
print(arr)