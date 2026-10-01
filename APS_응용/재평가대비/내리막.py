T = int(input())
for tc in range(1,T+1):
    N = int(input())
    numbers = list(map(int,input().split()))
    # i 번이랑 i + 1번이랑 비교
    # 계속 감소하냐???
    is_dec = True
    for i in range(N-1):  # N-1번이 아니라 N-2번까지만 순회
        # 계속 감소하냐?? 
        # 뒤쪽 요소가 작다! >>> 다음거 또 검사
        # 뒤쪽 요소가 크거나 같다! 즉시종료
        if numbers[i] <= numbers[i+1]:
            # 뒤쪽 숫자가 같거나 크므로 더이상 검사필요 X
            is_dec = False
            break
    if is_dec:
        print(f'#{tc}  1')
    else:
        print(f'#{tc}  0')