# 3단계. 조건에 맞는 튜플 고르기
#         None 은 문 닫은 가게 → 갈 수 없다

places = [(30, 40), (60, 80), (None,None), (90, 20), (10, 90), (25, 65)]

# 튜플끼리 바로 비교할 수 있다
print(places[2] is None)    # True
print(places[1] is None)    # False

# 열려 있는 가게 번호만 모으기 (내 위치 0번은 빼고 1번부터)
open_shops = []
for i in range(1, 6):
    if places[i] != (None, None):
        open_shops.append(i)
print("열린 가게 번호:", open_shops)    # [1, 3, 4, 5]

# 그중 첫 번째 가게로 가기로 한다
goal = places[open_shops[0]]
print("목적지:", goal)                 # (60, 80)

# ✏️ 연습: places[1] 도 None 으로 바꾸고 다시 실행하면 목적지가 무엇이 되는지 확인해 보세요


