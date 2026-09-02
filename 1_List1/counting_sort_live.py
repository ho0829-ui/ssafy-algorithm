DATA = [0,4,1,3,1,2,4,1] # 0<=정수<=4, 정렬할 배열
COUNTS = [0] * (4 + 1)
K = max(DATA)
N = len(DATA)
TEMP = [0] * N  # 정렬 결과를 저장할 배열

for x in DATA:
    COUNTS[x] += 1

print(COUNTS)

for i in range(1, K+1):
    COUNTS[i] += COUNTS[i - 1]

print(COUNTS)

# DATA의 마지막 원소부터 TEMP에 넣기
for j in range(N-1, -1, -1):
    COUNTS[DATA[j]] -= 1 # DATA[j]까지의 총 개수 1개 감소
    TEMP[COUNTS[DATA[j]]] = DATA[j]

print(TEMP)