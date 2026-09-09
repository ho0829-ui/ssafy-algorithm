T = int(input())
# 여러 개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    s = input().strip()
    stack = []

    for char in s:
        # 스택에 문자가 있고, 마지막 문자와 현재 문자가 같으면 제거 (반복문자 소거)
        if stack and stack[-1] == char:
            stack.pop()
        else:
            stack.append(char)

    # 결과 출력 (#테스트케이스번호 남은문자열길이)
    print(f"#{test_case} {len(stack)}")