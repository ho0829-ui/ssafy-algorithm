T = int(input())
for tc in range(1, T + 1):
    arr = list(input().split())
    stack = []
    for i in range(len(arr)):

        # 피연산자 인지 확인
        if arr[i] not in '*+-/.':
            arr[i] = int(arr[i])
        # 피 연산자면 스택에 추가, 아니면(연산자)면 연산
        if type(arr[i]) == int:
            stack.append(arr[i])
        # . 이 나오면 값 출력후 종료
        elif arr[i] == '.':
            if len(stack) == 1:
                num = stack.pop()
                print(f'#{tc} {int(num)}')
            else:
                print(f'#{tc} error')
        # 연산과정
        else:
            # 스택의 길이가 2 이상일떄만 연산 가능
            if len(stack) >= 2:
                a = stack.pop()  # 스택안에 있는값
                b = stack.pop()
                # 곱하기
                if arr[i] == '*':
                    stack.append(b * a)  # 스택에 다시 추가
                # 나누기
                elif arr[i] == '/':
                    if a == 0:
                        print(f'#{tc} error')
                        break
                    else:
                        stack.append(b // a)
                # 더하기
                elif arr[i] == '+':
                    stack.append(b + a)
                # 뺴기
                elif arr[i] == '-':
                    stack.append(b - a)
            # 연산이 불가능할때 error 출력
            else:
                print(f'#{tc} error')
                break
