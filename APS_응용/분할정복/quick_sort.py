# 기준점(피봇)보다 작은 값, 큰 값으로 나누기
# 나누다 보면 정렬이 된다...
arr = [6,8,1,3,4,5,9,2,7]
def quick_sort(target):
    l = len(target)
    if l < 1:   # 요소가 1개 보다 작으면 그대로 반환
        return target
    #임의의 값 하나 잡고, 작은애들 큰애들 모으기
    left = []   # 피벗보다 작은 값 들어갈 리스트
    right = [] # 피벗보다 큰 값 들어갈 리스트
    # 큰 값 작은 값 나누기
    pivot = target[0]
    for i in range(1,l):
        if target[i] < pivot: # 작으면 left에 붙이고
            left.append(target[i])
        else: # 크거나 같으면 right에 붙이기
            right.append(target[i])
    #근데 left랑 right가 여전히 정렬이 안 된 상태!
    left = quick_sort(left)
    right = quick_sort(right)
    return left + [pivot] + right

print(quick_sort(arr))