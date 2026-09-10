# 2단계. 튜플이 들어 있는 리스트 = 지도 위 지점 6개
#         0번은 내 위치, 1~5번은 가게 위치

places = [(30, 40), (60, 80), (None,None), (90, 20), (10, 90), (25, 65)]

print(places[0])        # (30, 40)  ← 내 위치
print(places[1])        # (60, 80)  ← 1번 가게
print(places[0][0])     # 30         ← 내 위치의 x
print(places[0][1])     # 40         ← 내 위치의 y

# 두 줄로 나눠 쓰면 더 읽기 쉽다
me = places[0]
print(me[0], me[1])

# 전부 출력해 보기
for p in places:
    print(p)

# 번호와 같이 출력하기
for i, p in enumerate(places):
    print(i, "번:", p)



