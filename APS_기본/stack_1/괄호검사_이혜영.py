T = int(input())

for test_case in range(1, T + 1):
    code = input().strip()
    bracket_dict = {
        "}": "{",
        ")": "("
    }
    validity = []

    result = 1
    for letter in code:
        if letter == "{" or letter == "(":
            validity.append(letter)
            # 이미 들어가 있는게 내 짝이냐???
        elif letter == "}" or letter == ")":
            if not validity: # 닫는 괄호가 나왔는데, 여는 괄호가 없었네???
                result = 0
                break
            else:   #닫는 괄호가 나왔고 여는 괄호가 있긴하니까.. .짝맞춰보자...
                if bracket_dict.get(letter) == validity[-1]:
                    validity.pop()
                # 내 짝아니면??
                else:
                    result = 0
                    break
    if result == 1:
        if validity:
            result = 0

    print(f'#{test_case}', result)
