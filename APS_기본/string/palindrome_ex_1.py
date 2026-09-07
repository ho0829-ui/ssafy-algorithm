
#전체 길이가 M인 문장으로 회문검사하기
target = 'ABCBA'
M = len(target)
# 앞쪽인덱스와 뒤쪽인덱스 비교
# 절반만 비교
# is_palin = True
# for i in range(M//2):
#     # i번 : 앞쪽 인덱스,
#     # M-1-i : 뒤쪽 인덱스
#     # 모두 똑같으면 회문, 하나라도 다르면 회문이 아님!
#     # 똑같은면 계속 비교해야하고.. 다르면 그만두면 되니까 다른지 검사!
#     if target[i] != target[M-1-i]:
#         #회문검사를 할 필요 없음! 이미 회문이 아님!
#         is_palin = False
#         break
#
# if is_palin:
#     print('회문입니다!')
# else:
#     print('회문이 아닙니다!')

for i in range(M//2):
    # i번 : 앞쪽 인덱스,
    # M-1-i : 뒤쪽 인덱스
    # 모두 똑같으면 회문, 하나라도 다르면 회문이 아님!
    # 똑같은면 계속 비교해야하고.. 다르면 그만두면 되니까 다른지 검사!
    if target[i] != target[M-1-i]:
        #회문검사를 할 필요 없음! 이미 회문이 아님!
        print('회문이 아닙니다!')
        break
else: # for문이 도는 동안 break가 한 번도 실행이 안되면 수행되는 코드 (회문인경이 실행되는 코드)
    print('회문입니다!')









