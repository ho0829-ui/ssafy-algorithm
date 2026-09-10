# 4단계. 튜플 두 개로 거리 구하기 → 가장 가까운 가게 찾기
import math

me = (30, 40)
goal = (60, 80)

x1, y1 = me
x2, y2 = goal
dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
print("거리:", dist)     # 50.0

# 여러 가게 중 가장 가까운 가게 찾기
places = [(30, 40), (60, 80), None, (90, 20), (10, 90), (34, 37)]

best_i = -1
best_dist = 99999
for i in range(1, 6):
    if places[i] is None:
        continue
    x2, y2 = places[i]
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    print(i, "번 가게까지 거리:", round(d, 1))
    if d < best_dist:
        best_dist = d
        best_i = i

print("가장 가까운 가게:", best_i, "번", places[best_i])    # 5 번 (34, 37)

# ✏️ 연습: 5번 가게를 None 으로 바꾸면 어떤 가게가 가장 가까워지는지 확인해 보세요


