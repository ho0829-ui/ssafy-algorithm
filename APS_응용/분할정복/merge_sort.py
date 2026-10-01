arr = [6,8,1,3,4,5,9,2,7]

# 병합 정렬
def merge_sort(arr):
    # 비효율적인 코드로 이해를 해봅시다!
    # arr을 정렬하기 위해서
    # 왼쪽, 오른쪽으로 나눠서 각각 정렬
    # 합치기 병합
    length = len(arr)
    if length == 1: # 하나 짜리는 정렬된 상태다
        return arr

    mid  = length//2
    #왼쪽 절반, 오른쪽 절반 나누기
    left_arr = arr[:mid]
    right_arr = arr[mid:]

    #각각 정렬해서
    left_arr = merge_sort(left_arr)
    right_arr = merge_sort(right_arr)

    #합치기
    #0번끼리 비교해서 작은애 붙이기
    sorted_arr = []
    # 둘 다 0번이 있으면 계속 실행
    while left_arr and right_arr:
        if left_arr[0] < right_arr[0]:
            sorted_arr.append(left_arr.pop(0))
        else:
            sorted_arr.append(right_arr.pop(0))
    # 왼쪽 배열이든, 오른쪽이든 요소가 남은 배열이 있으니까
    # 남은거 붙여주기
    sorted_arr += left_arr
    sorted_arr += right_arr
    return sorted_arr

print(merge_sort(arr))























