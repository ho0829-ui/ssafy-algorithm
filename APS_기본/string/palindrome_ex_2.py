target = 'ABABFFAFFC'
N = len(target)
M = 5
# 길이 N인 문장에서 길이 M인 회문 찾기
# 길이 M인 문장의 시작점 순회
for i in range(N-M+1):
    # i : 검사하려는 길이 M짜리 문장의 시작점
    # 첫번째 문자랑 마지막 문자랑 비교
    # i 번    <-------> i+M-1   ???
    # i + 1           i+M-1-1
    # ....
    for j in range(M//2):
        if target[i+j] != target[i+M-1-j]: #회문이 아님!
            break

    else: # 회문이 있으면! 찾았다! 끝내기
        print('회문 있음!!')
        break
else:
    print('회문 없음!')
################################################################
result = False
for i in range(N-M+1):
    is_find = True
    for j in range(M//2):
        if target[i+j] != target[i+M-1-j]: #회문이 아님!
            is_find = False
            break
    if is_find: # 회문 찾았음!
        result = True
if result:
    print('회문 찾음!!!!!!!')
else:
    print('회문 없음!!!!!!!!')

