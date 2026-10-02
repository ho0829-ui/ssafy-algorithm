arr = [6,8,1,3,4,5,9,2,1,4,2,7]
N = len(arr)
def partition(s,e):
    # 피벗을 기준으로 작은 값과 큰 값을 분리하고
    # 피벗 위치 반환
    pivot = arr[s]
    # 큰값을 찾을 변수
    i = s + 1
    # 작은 값을 찾을 변수
    j = e
    while i <= j:
        # i를 증가 시키면서 pivot보다 큰값 찾기
        while i <= j and arr[i] <= pivot:
            i += 1
        # j를 감소 키시면서 pivot 보다 작은값 찾기
        while i <= j and arr[j] >= pivot:
            j -= 1
        if i < j:
            # 큰 값은 뒤로 보내고, 작은값은 앞으로 보내기
            arr[i], arr[j] = arr[j], arr[i]

    # 피벗 제자리 찾아주기
    arr[s], arr[j] = arr[j], arr[s]
    return j

def quick_sort(s,e):
    if s > e: return
    # 1. 피벗보다 큰 값과 작은값으로 나누기 : partition
    pivot = partition(s,e)  #피벗 위치 반환
    quick_sort(s, pivot-1)
    quick_sort(pivot + 1, e)

quick_sort(0,N-1)
print(arr)







