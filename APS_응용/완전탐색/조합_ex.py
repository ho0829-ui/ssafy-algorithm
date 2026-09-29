# 조합 N개 중에 M개 뽑기
# 사실 이렇게 봐도 무방 (요소가 M개인 부분집합)
# 그래서..부분집합이랑 비슷하게 짜면 됩니다. + 개수 관련 내용만 추가
arr =['A','B','C']
N = len(arr)
bit = [0] * N
M = 2
def comb(idx,cnt):  # 몇 개를 골랐는지 가 중요!
    if cnt == M: # 내가 원하는 개수 만큼 고름!
        print(bit)
        return
    if idx == N: # 인덱스가 끝났는데...위조건에는 안걸림
        # 조합을 만드는데는 실패한 경우
        return

    bit[idx] = 1  # idx 번째 요소를 조합에 넣겠다!
    comb(idx + 1, cnt + 1)  # 선택한 요소 개수 + 1

    bit[idx] = 0    # idx 번째 요소를 조합에 넣지 않겠다!
    comb(idx + 1, cnt) # 선택한 요소 개수 그대로
comb(0,0)

