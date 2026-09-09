

num_dict = {
'ZRO':0, 'ONE':1, 'TWO':2, 'THR':3, 'FOR':4, 'FIV':5, 'SIX':6, 'SVN':7, 'EGT':8, 'NIN':9
}
def counting_sort(numbers):
    # 카운팅정렬 : 내 자리찾기(내앞에 몇 개 있냐?)
    # 1. 각 숫자가 몇 번 나왔는지 센다.
    cnt = [0] * 10
    for i in range(N):
        # numbers[i]    ZRO, SIX.....
        # cnt[num_dict[numbers[i]]] += 1
        str_num = numbers[i]
        num = num_dict[str_num]
        cnt[num] += 1
    # 2. 누적합구하기 : 각 숫자 앞에 몇개있는지 자리 찾기
    for i in range(1,10):
        #내 앞 숫자랑 내 숫자랑 더해서 다시 내자리에 넣어주기
        # cnt[i] = cnt[i-1] + cnt[i]
        cnt[i] += cnt[i-1]
    # 3. 자리에 맞게 새로운 배열에 넣어주기
    sorted_arr = [None] * N
    # 원본 배열에 있는 숫자 보면서 자기 자리 찾아서 넣어주기
    for i in range(N):
        cnt[num_dict[numbers[i]]] -= 1  #내 순번이니까 인덱스는 -1
        sorted_arr[cnt[num_dict[numbers[i]]]] = numbers[i]

    return sorted_arr

# 인자로 대상 배열 받아서 정렬한 다음 반환하기
def bubble_sort(numbers):
    #옆에 있는거 끼리 비교해서 큰 거 뒤로 보내기 * N-1번
    for i in range(N-1):
        for j in range(N-1-i):
            # j번이랑 j+1번이랑 비교
            # numbers[j]랑 numbers[j+1]을 비교하는데.. 문자열이라서 비교가 안되니까
            # num_dict를 활용해서 비교
            if num_dict[numbers[j]] > num_dict[numbers[j+1]]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
    return numbers

T = int(input())
for _ in range(T):
    tc, N = input().split()
    N = int(N)
    numbers = input().split()
    numbers = counting_sort(numbers)
    print(tc)
    print(*numbers)








