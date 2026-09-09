# data에 길이 M인 회문이 있으면 찾아서 반환하는 함수
def solve(data):
    # 검사할 문장의 시작점 순회
    for i in range(N):  # 모든 행  검사
        for j in range(N-M+1): #열은 M보다 작은 뒤쪽은 검사하지 않음
            # j 열에서 시작하는 길이 M 짜리 회문이 있는지 검사
            is_find = True
            for k in range(M//2):
                # j + k 번이랑 j + M -1 - k번이랑 비교
                if data[i][j+k] != data[i][j+M-1-k]:
                    is_find = False # 회문이 아님!
            #회문이면....회문을 반환해야 한다!
            if is_find: # j번 부터 j+M-1 번까지가 회문이다!
                palindrome = ''
                for l in range(j,j+M):
                    palindrome += data[i][l]
                return palindrome

    for i in range(N):  # 모든 행  검사
        for j in range(N-M+1): #열은 M보다 작은 뒤쪽은 검사하지 않음
            # j 열에서 시작하는 길이 M 짜리 회문이 있는지 검사
            is_find = True
            for k in range(M//2):
                # j + k 번이랑 j + M -1 - k번이랑 비교
                if data[j+k][i] != data[j+M-1-k][i]:
                    is_find = False # 회문이 아님!
            #회문이면....회문을 반환해야 한다!
            if is_find: # j번 부터 j+M-1 번까지가 회문이다!
                palindrome = ''
                for l in range(j,j+M):
                    palindrome += data[l][i]
                return palindrome

T = int(input())
for tc in range(1,T+1):
    N, M = map(int,input().split())
    data = [input().strip() for _ in range(N)]
    result = solve(data)
    print(f'#{tc} {result}')